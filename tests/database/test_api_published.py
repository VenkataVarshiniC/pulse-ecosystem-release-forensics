"""Read-only golden API checks against the two published local snapshots."""

from __future__ import annotations

import os
from collections import Counter
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from pulse.api.app import app
from pulse.api.config import PUBLISHED_SNAPSHOT_IDS
from pulse.phase2_postgres.loader import connect


@pytest.fixture(scope="module")
def client() -> TestClient:
    try:
        with connect("pulse_dev") as conn:
            count = conn.execute(
                "SELECT count(*) FROM core.analysis_snapshot WHERE state='PUBLISHED_VALIDATION'"
            ).fetchone()[0]
        if count != 2:
            raise RuntimeError("Expected two published validation snapshots")
    except Exception as error:
        if os.environ.get("PULSE_REQUIRE_DB_TESTS") == "1":
            pytest.fail(f"published pulse_dev data unavailable: {error}")
        pytest.skip(f"published pulse_dev data unavailable: {error}")
    return TestClient(app)


def test_list_cohort_and_snapshot_isolation(client: TestClient) -> None:
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "api_version": "v1", "database_reachable": True}
    investigations = client.get("/api/v1/investigations").json()["items"]
    assert len(investigations) == 2
    assert {UUID(x["scope"]["analysis_snapshot_id"]) for x in investigations} == (
        PUBLISHED_SNAPSHOT_IDS
    )
    by_package = {x["package_name"]: x for x in investigations}
    assert {name: x["member_count"] for name, x in by_package.items()} == {
        "pytest": 2,
        "urllib3": 6,
    }
    for item in investigations:
        scope = item["scope"]
        detail = client.get(
            f"/api/v1/investigations/{scope['case_version_id']}",
            params={"snapshot_id": scope["analysis_snapshot_id"]},
        )
        assert detail.status_code == 200
        assert len(detail.json()["members"]) == item["member_count"]
        assert detail.json()["investigation"]["scope"] == scope
    wrong = client.get(
        f"/api/v1/investigations/{by_package['pytest']['scope']['case_version_id']}",
        params={"snapshot_id": by_package["urllib3"]["scope"]["analysis_snapshot_id"]},
    )
    assert wrong.status_code == 404 and wrong.json()["code"] == "INVALID_SNAPSHOT"
    legacy = client.get(
        f"/api/v1/investigations/{by_package['pytest']['scope']['case_version_id']}",
        params={"snapshot_id": "00000000-0000-0000-0000-000000000001"},
    )
    assert legacy.status_code == 404 and legacy.json()["code"] == "INVALID_SNAPSHOT"


def test_golden_evidence_findings_and_candidates(client: TestClient) -> None:
    counts: Counter[str] = Counter()
    snapshots = client.get("/api/v1/investigations").json()["items"]
    for investigation in snapshots:
        scope = investigation["scope"]
        root = f"/api/v1/investigations/{scope['case_version_id']}"
        params = {"snapshot_id": scope["analysis_snapshot_id"]}
        members = client.get(root, params=params).json()["members"]
        counts["members"] += len(members)
        for member in members:
            repository_id = member["repository_id"]
            base = f"{root}/repositories/{repository_id}"
            detail = client.get(base, params=params)
            assert detail.status_code == 200
            body = detail.json()
            assert body["member"]["repository_id"] == repository_id
            findings = client.get(base + "/findings", params=params).json()["items"]
            assert len(findings) == 5
            assert body["findings"] == findings
            for finding in findings:
                counts[finding["finding_status"]] += 1
                counts[finding["sufficiency_status"]] += 1
                assert (
                    client.get(base + f"/findings/{finding['finding_id']}", params=params).json()
                    == finding
                )
                if finding["finding_status"] == "UNKNOWN":
                    assert finding["artifact_support_ids"] == []
            candidates = client.get(base + "/candidates", params=params).json()["items"]
            assert body["candidate_count"] == member["candidate_count"] == len(candidates)
            counts["candidates"] += len(candidates)
            for candidate in candidates:
                assert candidate["review_write_enabled"] is False
                assert candidate["review"]["decision"] == "REJECT"
                assert candidate["review"]["review_origin"] == "INHERITED"
                assert (
                    candidate["review"]["inherited_from_review_id"]
                    == (candidate["original_review_id"])
                )
                counts["inherited_reject"] += 1
                assert (
                    client.get(
                        base + f"/candidates/{candidate['candidate_id']}", params=params
                    ).json()
                    == candidate
                )
                provenance = client.get(
                    base + f"/artifacts/{candidate['artifact_id']}", params=params
                )
                assert provenance.status_code == 200
                assert candidate["candidate_id"] in provenance.json()["linked_candidate_ids"]
                assert "raw_snapshot_uri" not in provenance.json()
                assert "password" not in provenance.text.lower()
                blocked = client.post(
                    base + f"/candidates/{candidate['candidate_id']}/reviews",
                    params=params,
                    json={
                        "decision": "ACCEPT",
                        "reason_code": "should be blocked",
                        "idempotency_key": "published-replay-test",
                    },
                )
                assert blocked.status_code == 409
                assert blocked.json()["code"] == "PUBLISHED_IMMUTABLE"
                assert (
                    client.get(
                        base + f"/candidates/{candidate['candidate_id']}", params=params
                    ).json()
                    == candidate
                )
            if not candidates:
                counts["zero_candidate_members"] += 1
            first = client.get(base + "/evidence", params={**params, "limit": 3}).json()
            all_ids: list[str] = []
            page = first
            while True:
                all_ids.extend(item["artifact_id"] for item in page["items"])
                assert all(
                    item["source_event_time"] is None
                    or item["source_event_time"] != item["retrieved_at"]
                    for item in page["items"]
                )
                if page["next_cursor"] is None:
                    break
                page = client.get(
                    base + "/evidence",
                    params={**params, "limit": 3, "cursor": page["next_cursor"]},
                ).json()
            assert len(all_ids) == len(set(all_ids))
            assert all_ids == sorted(all_ids)
            assert len(all_ids) >= len(first["items"])
    assert counts == Counter(
        {
            "members": 8,
            "UNKNOWN": 38,
            "NO_QUALIFYING_EVIDENCE_FOUND": 2,
            "INSUFFICIENT": 38,
            "SUFFICIENT": 2,
            "candidates": 2,
            "inherited_reject": 2,
            "zero_candidate_members": 7,
        }
    )


def test_out_of_cohort_and_cross_snapshot_resources_are_hidden(client: TestClient) -> None:
    investigations = client.get("/api/v1/investigations").json()["items"]
    pytest_case, urllib_case = investigations
    p_scope = pytest_case["scope"]
    u_scope = urllib_case["scope"]
    p_base = f"/api/v1/investigations/{p_scope['case_version_id']}"
    p_repo = client.get(p_base, params={"snapshot_id": p_scope["analysis_snapshot_id"]}).json()[
        "members"
    ][0]["repository_id"]
    u_base = f"/api/v1/investigations/{u_scope['case_version_id']}"
    u_repo = client.get(u_base, params={"snapshot_id": u_scope["analysis_snapshot_id"]}).json()[
        "members"
    ][0]["repository_id"]
    wrong_member = client.get(
        p_base + f"/repositories/{u_repo}", params={"snapshot_id": p_scope["analysis_snapshot_id"]}
    )
    assert wrong_member.status_code == 404
    artifact = client.get(
        p_base + f"/repositories/{p_repo}/evidence",
        params={"snapshot_id": p_scope["analysis_snapshot_id"]},
    ).json()["items"][0]["artifact_id"]
    wrong_artifact = client.get(
        u_base + f"/repositories/{u_repo}/artifacts/{artifact}",
        params={"snapshot_id": u_scope["analysis_snapshot_id"]},
    )
    assert wrong_artifact.status_code == 404
    assert wrong_artifact.json()["code"] == "PROVENANCE_MISMATCH"
