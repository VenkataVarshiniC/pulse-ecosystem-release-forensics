"""Read-only M5.4 reconciliation against the running local API and published DB.

Run after starting the isolated PostgreSQL cluster and FastAPI:
    .venv/Scripts/python.exe scripts/validate_m5_4_live.py

This script issues GETs and opens PostgreSQL with default_transaction_read_only=on.
It prints a compact summary and never writes evidence, reviews, or snapshots.
"""

from __future__ import annotations

import json
import statistics
import time
from collections import Counter
from typing import Any
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from uuid import UUID

from pulse.api.config import Settings
from pulse.api.repository import connect_read

BASE = "http://127.0.0.1:8000/api/v1"
EXPECTED_SNAPSHOTS = {
    "pytest": "08852d5f-9843-5406-a69b-7039ea2ddaa4",
    "urllib3": "bd3a02a5-0c2d-5eec-84fd-8e9b93a238a3",
}
LATENCIES_MS: list[float] = []


def get(path: str, **params: str | int) -> tuple[int, dict[str, Any]]:
    url = BASE + path + ("?" + urlencode(params) if params else "")
    started = time.perf_counter()
    try:
        with urlopen(Request(url, headers={"Accept": "application/json"}), timeout=10) as response:
            status = response.status
            body = json.load(response)
    except HTTPError as error:
        status = error.code
        body = json.load(error)
    LATENCIES_MS.append((time.perf_counter() - started) * 1000)
    return status, body


def success(path: str, **params: str | int) -> dict[str, Any]:
    status, body = get(path, **params)
    assert status == 200, f"GET {path} returned {status}: {body.get('code')}"
    return body


def main() -> None:
    health = success("/health")
    assert health["database_reachable"] is True
    investigations = success("/investigations")["items"]
    assert len(investigations) == 2
    by_package = {item["package_name"]: item for item in investigations}
    assert {
        name: item["scope"]["analysis_snapshot_id"] for name, item in by_package.items()
    } == EXPECTED_SNAPSHOTS
    assert {name: item["member_count"] for name, item in by_package.items()} == {
        "pytest": 2,
        "urllib3": 6,
    }

    counts: Counter[str] = Counter()
    finding_rows: list[tuple[UUID, UUID, UUID, str, str, str, str]] = []
    candidate_rows: list[tuple[UUID, UUID, UUID, str, str]] = []
    candidate_artifacts: set[str] = set()
    pair_states: Counter[str] = Counter()
    event_present = event_missing = source_unavailable = page_transitions = 0
    zero_candidate_members = 0
    for investigation in investigations:
        scope = investigation["scope"]
        case = scope["case_version_id"]
        snapshot = scope["analysis_snapshot_id"]
        root = f"/investigations/{case}"
        detail = success(root, snapshot_id=snapshot)
        assert detail["investigation"]["scope"] == scope
        assert len(detail["members"]) == investigation["member_count"]
        counts["members"] += len(detail["members"])
        for member in detail["members"]:
            repo = member["repository_id"]
            base = f"{root}/repositories/{repo}"
            record = success(base, snapshot_id=snapshot)
            assert record["scope"] == scope and record["member"]["repository_id"] == repo
            pair_states.update(pair["pair_status"] for pair in record["historical_pairs"])
            source_unavailable += sum(
                state["terminal_status"] == "SOURCE_UNAVAILABLE"
                for state in record["source_states"]
            )
            findings = success(base + "/findings", snapshot_id=snapshot)["items"]
            assert findings == record["findings"] and len(findings) == 5
            for finding in findings:
                fid = finding["finding_id"]
                assert success(base + f"/findings/{fid}", snapshot_id=snapshot) == finding
                counts[finding["finding_status"]] += 1
                counts[finding["sufficiency_status"]] += 1
                finding_rows.append(
                    (
                        UUID(snapshot),
                        UUID(case),
                        UUID(repo),
                        fid,
                        finding["finding_status"],
                        finding["reason_code"],
                        finding["sufficiency_status"],
                    )
                )
                if finding["finding_status"] == "UNKNOWN":
                    assert finding["sufficiency_status"] != "SUFFICIENT"
                if finding["finding_status"] == "NO_QUALIFYING_EVIDENCE_FOUND":
                    assert finding["sufficiency_status"] == "SUFFICIENT"
            candidates = success(base + "/candidates", snapshot_id=snapshot)["items"]
            assert len(candidates) == record["candidate_count"] == member["candidate_count"]
            counts["candidates"] += len(candidates)
            if not candidates:
                zero_candidate_members += 1
            for candidate in candidates:
                cid = candidate["candidate_id"]
                assert success(base + f"/candidates/{cid}", snapshot_id=snapshot) == candidate
                assert candidate["review_write_enabled"] is False
                assert candidate["review"]["decision"] == "REJECT"
                assert candidate["review"]["review_origin"] == "INHERITED"
                assert (
                    candidate["original_review_id"]
                    == candidate["review"]["inherited_from_review_id"]
                )
                counts["inherited_reject"] += 1
                candidate_rows.append(
                    (UUID(snapshot), UUID(case), UUID(repo), cid, candidate["artifact_id"])
                )
                candidate_artifacts.add(candidate["artifact_id"])
                artifact = success(
                    base + f"/artifacts/{candidate['artifact_id']}", snapshot_id=snapshot
                )
                assert artifact["scope"] == scope and artifact["repository_id"] == repo
                assert cid in artifact["linked_candidate_ids"]
                assert artifact["capture_method"] in {"collector", "connector_assisted", "fixture"}
                assert len(artifact["content_sha256"]) == 64
                assert "raw_snapshot_uri" not in artifact

            # A page size of two exercises real keyset pagination without changing data.
            ids: list[str] = []
            cursor: str | None = None
            while True:
                args: dict[str, str | int] = {"snapshot_id": snapshot, "limit": 2}
                if cursor:
                    args["cursor"] = cursor
                page = success(base + "/evidence", **args)
                assert page["scope"] == scope and page["repository_id"] == repo
                ids.extend(item["artifact_id"] for item in page["items"])
                for item in page["items"]:
                    event_present += item["source_event_time"] is not None
                    event_missing += item["source_event_time"] is None
                    assert item["retrieved_at"] is not None
                cursor = page["next_cursor"]
                if cursor is None:
                    break
                page_transitions += 1
            assert ids == sorted(set(ids)), f"Cursor duplication/order error for {repo}"
            all_page = success(base + "/evidence", snapshot_id=snapshot, limit=100)
            assert ids == [item["artifact_id"] for item in all_page["items"]]
            if all_page["items"]:
                source = all_page["items"][0]["source_type"]
                filtered_ids: list[str] = []
                cursor = None
                while True:
                    args = {"snapshot_id": snapshot, "limit": 1, "source_type": source}
                    if cursor:
                        args["cursor"] = cursor
                    page = success(base + "/evidence", **args)
                    filtered_ids.extend(item["artifact_id"] for item in page["items"])
                    cursor = page["next_cursor"]
                    if cursor is None:
                        break
                assert filtered_ids == [
                    item["artifact_id"]
                    for item in all_page["items"]
                    if item["source_type"] == source
                ]

    assert counts == Counter(
        {
            "members": 8,
            "UNKNOWN": 38,
            "NO_QUALIFYING_EVIDENCE_FOUND": 2,
            "INSUFFICIENT": 38,
            "SUFFICIENT": 2,
            "candidates": 2,
            "inherited_reject": 2,
        }
    )
    assert sum(counts[status] for status in ("UNKNOWN", "NO_QUALIFYING_EVIDENCE_FOUND")) == 40
    positive_findings = sum(
        status not in {"UNKNOWN", "NO_QUALIFYING_EVIDENCE_FOUND"}
        for _, _, _, _, status, _, _ in finding_rows
    )
    assert positive_findings == 0
    assert len(candidate_artifacts) == 1 and zero_candidate_members == 7
    assert event_present > 0 and event_missing > 0 and page_transitions > 0
    assert (
        pair_states["PAIRED"] > 0
        and pair_states["AFTER_ONLY"] > 0
        and pair_states["UNRESOLVED"] > 0
    )

    # Independently reconcile API finding/candidate identity and states to read-only DB rows.
    with connect_read(Settings.from_environment()) as conn:
        for snapshot, case, repo, fid, status, reason, sufficiency in finding_rows:
            row = conn.execute(
                """SELECT f.finding_status, f.reason_code, a.sufficiency_status
                   FROM core.snapshot_finding sf
                   JOIN core.lifecycle_finding f USING (finding_id)
                   JOIN core.snapshot_assessment sa ON sa.assessment_id=f.sufficiency_assessment_id
                        AND sa.analysis_snapshot_id=sf.analysis_snapshot_id
                   JOIN core.sufficiency_assessment a ON a.assessment_id=sa.assessment_id
                   WHERE sf.analysis_snapshot_id=%s AND f.case_version_id=%s
                     AND f.repository_id=%s AND f.finding_id=%s""",
                (snapshot, case, repo, UUID(fid)),
            ).fetchone()
            assert row and (
                row["finding_status"],
                row["reason_code"],
                row["sufficiency_status"],
            ) == (status, reason, sufficiency)
        for snapshot, case, repo, cid, artifact_id in candidate_rows:
            row = conn.execute(
                """SELECT c.artifact_id, ar.decision, ar.review_origin
                   FROM core.snapshot_candidate sc JOIN core.candidate c USING (candidate_id)
                   JOIN core.snapshot_review sr ON sr.analysis_snapshot_id=sc.analysis_snapshot_id
                   JOIN core.analyst_review ar ON ar.review_id=sr.review_id
                     AND ar.candidate_id=c.candidate_id
                   WHERE sc.analysis_snapshot_id=%s AND c.case_version_id=%s
                     AND c.repository_id=%s AND c.candidate_id=%s""",
                (snapshot, case, repo, UUID(cid)),
            ).fetchone()
            assert row and row["artifact_id"] == UUID(artifact_id)
            assert row["decision"] == "REJECT" and row["review_origin"] == "INHERITED"

    pytest_case = by_package["pytest"]["scope"]["case_version_id"]
    pytest_snapshot = EXPECTED_SNAPSHOTS["pytest"]
    urllib_snapshot = EXPECTED_SNAPSHOTS["urllib3"]
    urllib_member = success(
        f"/investigations/{by_package['urllib3']['scope']['case_version_id']}",
        snapshot_id=urllib_snapshot,
    )["members"][0]["repository_id"]
    status, body = get(f"/investigations/{pytest_case}", snapshot_id=urllib_snapshot)
    assert status == 404 and body["code"] == "INVALID_SNAPSHOT"
    status, body = get(
        f"/investigations/{pytest_case}/repositories/{urllib_member}", snapshot_id=pytest_snapshot
    )
    assert status == 404 and body["code"] == "NOT_FOUND_IN_SELECTED_COHORT"

    print(
        json.dumps(
            {
                "classification": "read_only_live_reconciliation_pass",
                "published_investigations": len(investigations),
                "snapshots": EXPECTED_SNAPSHOTS,
                "counts": dict(sorted(counts.items())),
                "positive_findings": positive_findings,
                "zero_candidate_members": zero_candidate_members,
                "shared_candidate_artifacts": len(candidate_artifacts),
                "historical_pair_states": dict(sorted(pair_states.items())),
                "source_unavailable_tasks": source_unavailable,
                "evidence_event_time_present": event_present,
                "evidence_event_time_missing": event_missing,
                "evidence_page_transitions": page_transitions,
                "api_requests": len(LATENCIES_MS),
                "api_latency_ms_median": round(statistics.median(LATENCIES_MS), 1),
                "api_latency_ms_max": round(max(LATENCIES_MS), 1),
                "scope_errors": ["INVALID_SNAPSHOT", "NOT_FOUND_IN_SELECTED_COHORT"],
                "database_rows_reconciled": {
                    "findings": len(finding_rows),
                    "candidates": len(candidate_rows),
                },
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
