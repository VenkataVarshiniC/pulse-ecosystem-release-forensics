"""A valid DRAFT review is exercised only in pulse_test and rolled back."""

from __future__ import annotations

import hashlib
import os
from dataclasses import replace
from uuid import UUID, uuid4

import psycopg
import pytest
from psycopg.rows import dict_row

from pulse.api.config import Settings
from pulse.api.errors import ApiError
from pulse.api.review import ReviewPolicy, ReviewWriter
from pulse.api.schemas import ReviewSubmission


class RollbackFixture(Exception):
    pass


def _digest(value: UUID) -> str:
    return hashlib.sha256(value.bytes).hexdigest()


def _seed(conn: psycopg.Connection) -> dict[str, UUID]:
    ids = {
        name: uuid4()
        for name in (
            "source",
            "release",
            "repository",
            "case_version",
            "case",
            "artifact",
            "candidate",
            "snapshot",
        )
    }
    conn.execute(
        """INSERT INTO ingestion.source_registry
           (source_id,provider,source_type,source_version,access_class)
           VALUES (%s,'fixture','api_review','v1','public')""",
        (ids["source"],),
    )
    conn.execute(
        """INSERT INTO core.dependency_release
           (release_id,package_ecosystem,package_name_normalized,version,
            release_time,release_source_id)
           VALUES (%s,'pypi','fixture-review','1.0',now(),%s)""",
        (ids["release"], ids["source"]),
    )
    conn.execute(
        """INSERT INTO core.repository
           (repository_id,provider,provider_repository_id,canonical_full_name,identity_status)
           VALUES (%s,'fixture',%s,'fixture/review','verified')""",
        (ids["repository"], str(ids["repository"])),
    )
    conn.execute(
        """INSERT INTO core.investigation_case
           (case_version_id,case_id,case_version,case_name,target_release_id,
            window_start,window_end,source_plan_version,rule_version,status)
           VALUES (%s,%s,1,'fixture review case',%s,now(),now(),'fixture','fixture','DRAFT')""",
        (ids["case_version"], ids["case"], ids["release"]),
    )
    conn.execute(
        """INSERT INTO core.cohort_membership
           (case_version_id,repository_id,selection_method,eligibility_status,included_at)
           VALUES (%s,%s,'fixture','included',now())""",
        (ids["case_version"], ids["repository"]),
    )
    content_digest = _digest(ids["artifact"])
    conn.execute(
        """INSERT INTO core.evidence_artifact
           (artifact_id,capture_fingerprint,source_id,repository_id,artifact_type,
            source_locator,retrieved_at,capture_method,content_sha256,raw_snapshot_uri,media_type)
           VALUES (%s,%s,%s,%s,'fixture','fixture://source',now(),'fixture',%s,
                   'fixture://raw','application/json')""",
        (ids["artifact"], _digest(ids["source"]), ids["source"], ids["repository"], content_digest),
    )
    conn.execute(
        """INSERT INTO core.candidate
           (candidate_id,candidate_fingerprint,case_version_id,repository_id,
            artifact_id,baseline_version,candidate_rule_id,candidate_rule_version,
            lifecycle_category,source_origin,candidate_status,candidate_reason,span_ref)
           VALUES (%s,%s,%s,%s,%s,'fixture','fixture-rule','v1',
                   'friction','LOCAL_DOWNSTREAM','EMITTED','fixture','span:1')""",
        (
            ids["candidate"],
            _digest(ids["candidate"]),
            ids["case_version"],
            ids["repository"],
            ids["artifact"],
        ),
    )
    conn.execute(
        """INSERT INTO core.analysis_snapshot
           (analysis_snapshot_id,case_version_id,source_plan_version,rule_version,
            metric_definition_version,model_version,loader_version,generated_at,
            state,manifest_sha256)
           VALUES (%s,%s,'fixture','fixture','fixture','fixture','fixture',now(),
                   'DRAFT',%s)""",
        (ids["snapshot"], ids["case_version"], _digest(ids["snapshot"])),
    )
    conn.execute(
        """INSERT INTO core.snapshot_artifact
           (analysis_snapshot_id,artifact_id,expected_sha256,sort_ordinal)
           VALUES (%s,%s,%s,0)""",
        (ids["snapshot"], ids["artifact"], content_digest),
    )
    conn.execute(
        """INSERT INTO core.snapshot_candidate (analysis_snapshot_id,candidate_id)
           VALUES (%s,%s)""",
        (ids["snapshot"], ids["candidate"]),
    )
    return ids


def test_fixture_draft_review_is_atomic_idempotent_and_rolled_back() -> None:
    try:
        base = Settings.from_environment()
        settings = replace(base, database="pulse_test", environment="test")
        conn = psycopg.connect(
            host=settings.host,
            port=settings.port,
            dbname=settings.database,
            user=settings.user,
            password=settings.password,
            connect_timeout=3,
            autocommit=True,
            row_factory=dict_row,
        )
    except Exception as error:
        if os.environ.get("PULSE_REQUIRE_DB_TESTS") == "1":
            pytest.fail(f"pulse_test unavailable: {error}")
        pytest.skip(f"pulse_test unavailable: {error}")
    with conn:
        ids: dict[str, UUID] = {}
        try:
            with conn.transaction():
                ids = _seed(conn)
                writer = ReviewWriter(
                    settings, ReviewPolicy("fixture-human", frozenset({ids["snapshot"]}))
                )
                submission = ReviewSubmission(
                    decision="REJECT",
                    reason_code="fixture copied text",
                    idempotency_key="fixture-attempt-1",
                )
                args = (
                    ids["case_version"],
                    ids["snapshot"],
                    ids["repository"],
                    ids["candidate"],
                    submission,
                )
                conn.execute(
                    """DELETE FROM core.snapshot_artifact
                       WHERE analysis_snapshot_id=%s AND artifact_id=%s""",
                    (ids["snapshot"], ids["artifact"]),
                )
                with pytest.raises(ApiError) as mismatch:
                    writer.submit_in_connection(conn, *args)
                assert mismatch.value.code == "PROVENANCE_MISMATCH"
                conn.execute(
                    """INSERT INTO core.snapshot_artifact
                       (analysis_snapshot_id,artifact_id,expected_sha256,sort_ordinal)
                       VALUES (%s,%s,%s,0)""",
                    (ids["snapshot"], ids["artifact"], _digest(ids["artifact"])),
                )
                with pytest.raises(ApiError) as out_of_cohort:
                    writer.submit_in_connection(
                        conn,
                        ids["case_version"],
                        ids["snapshot"],
                        uuid4(),
                        ids["candidate"],
                        submission,
                    )
                assert out_of_cohort.value.code == "NOT_FOUND_IN_SELECTED_COHORT"
                first = writer.submit_in_connection(conn, *args)
                assert first.idempotent_replay is False
                assert writer.submit_in_connection(conn, *args).idempotent_replay is True
                assert (
                    conn.execute(
                        "SELECT count(*) FROM core.analyst_review WHERE candidate_id=%s",
                        (ids["candidate"],),
                    ).fetchone()["count"]
                    == 1
                )
                with pytest.raises(ApiError) as stale:
                    writer.submit_in_connection(
                        conn,
                        *args[:-1],
                        submission.model_copy(update={"idempotency_key": "fixture-attempt-2"}),
                    )
                assert stale.value.code == "STALE_REVIEW"
                with pytest.raises(ApiError) as collision:
                    writer.submit_in_connection(
                        conn, *args[:-1], submission.model_copy(update={"reason_code": "changed"})
                    )
                assert collision.value.code == "IDEMPOTENCY_CONFLICT"
                with pytest.raises(ApiError) as unauthorized:
                    ReviewWriter(settings, ReviewPolicy()).submit_in_connection(conn, *args)
                assert unauthorized.value.code == "REVIEWER_NOT_AUTHORIZED"
                raise RollbackFixture
        except RollbackFixture:
            pass
        assert (
            conn.execute(
                "SELECT count(*) FROM core.analyst_review WHERE candidate_id=%s",
                (ids["candidate"],),
            ).fetchone()["count"]
            == 0
        )
