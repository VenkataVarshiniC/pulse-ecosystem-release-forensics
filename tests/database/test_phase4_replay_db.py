"""M4.1B replay is additive, case-scoped, and inherits only verified reviews."""

from __future__ import annotations

import os

import psycopg
import pytest

from pulse.phase2_postgres.loader import connect, load_case_into
from pulse.phase2_postgres.manifest import ROOT, sha256
from pulse.phase4_replay_db import load_replay_into, model_digest, verified_replay


class _Rollback(Exception):
    pass


def _test_connection():
    try:
        return connect("pulse_test")
    except Exception as error:
        if os.environ.get("PULSE_REQUIRE_DB_TESTS") == "1":
            pytest.fail(f"pulse_test unavailable: {error}")
        pytest.skip(f"pulse_test unavailable: {error}")


def test_replay_load_is_idempotent_and_does_not_rewrite_legacy() -> None:
    replay, inputs, _ = verified_replay()
    metric_sha = sha256(ROOT / "analytics/metrics/metric_registry.yml")
    with _test_connection() as conn:
        try:
            with conn.transaction():
                for case in ("pytest-8.0.0", "urllib3-2.0.0"):
                    assert load_case_into(conn, inputs, case) == "loaded"
                original = conn.execute(
                    """SELECT analysis_snapshot_id,rule_version,state,manifest_sha256
                       FROM core.analysis_snapshot ORDER BY analysis_snapshot_id"""
                ).fetchall()
                assert len(original) == 2
                first = load_replay_into(
                    conn, replay, inputs, "0" * 40, model_digest(), metric_sha
                )
                second = load_replay_into(
                    conn, replay, inputs, "0" * 40, model_digest(), metric_sha
                )
                assert first == second
                assert len(set(first.values())) == 2
                assert conn.execute(
                    """SELECT analysis_snapshot_id,rule_version,state,manifest_sha256
                       FROM core.analysis_snapshot
                       WHERE rule_version='unrecorded_in_frozen_report'
                       ORDER BY analysis_snapshot_id"""
                ).fetchall() == original
                assert conn.execute(
                    "SELECT count(*) FROM core.analysis_snapshot"
                ).fetchone()[0] == 4
                assert conn.execute("""SELECT count(*),count(DISTINCT artifact_id)
                    FROM core.candidate c JOIN core.replay_candidate_lineage l
                    ON c.candidate_id=l.candidate_id""").fetchone() == (2, 1)
                assert conn.execute("""SELECT count(*) FROM core.analyst_review
                    WHERE review_origin='INHERITED' AND decision='REJECT'
                    AND inherited_from_review_id IS NOT NULL""").fetchone()[0] == 2
                assert conn.execute("""SELECT sufficiency_status,count(*)
                    FROM core.sufficiency_assessment WHERE assessment_version=2
                    GROUP BY 1 ORDER BY 1""").fetchall() == [
                        ("INSUFFICIENT", 38), ("SUFFICIENT", 2)
                    ]
                assert conn.execute("""SELECT finding_status,count(*)
                    FROM core.lifecycle_finding WHERE finding_version=2
                    GROUP BY 1 ORDER BY 1""").fetchall() == [
                        ("NO_QUALIFYING_EVIDENCE_FOUND", 2), ("UNKNOWN", 38)
                    ]
                assert conn.execute("""SELECT count(*) FROM core.snapshot_candidate sc
                    JOIN core.replay_candidate_lineage l ON sc.candidate_id=l.candidate_id
                    WHERE sc.analysis_snapshot_id<>l.analysis_snapshot_id""").fetchone()[0] == 0
                assert conn.execute("""SELECT count(*) FROM core.replay_candidate_lineage l
                    JOIN core.candidate c ON l.candidate_id=c.candidate_id
                    JOIN core.analyst_review inherited ON l.replay_review_id=inherited.review_id
                    JOIN core.analyst_review original ON l.original_review_id=original.review_id
                    WHERE c.candidate_rule_version<>'rule-replay-b2b638bb97c8-e10fb03f467e267f'
                       OR inherited.reviewed_at<>original.reviewed_at
                       OR inherited.inherited_from_review_id<>original.review_id
                       OR l.equivalence<>'EXACT_EQUIVALENT'""").fetchone()[0] == 0
                assert conn.execute("""SELECT count(*) FROM core.snapshot_assessment sa
                    JOIN core.sufficiency_assessment a ON sa.assessment_id=a.assessment_id
                    JOIN core.analysis_snapshot s ON sa.analysis_snapshot_id=s.analysis_snapshot_id
                    WHERE (a.assessment_version=1) <>
                        (s.rule_version='unrecorded_in_frozen_report')""").fetchone()[0] == 0
                raise _Rollback
        except _Rollback:
            pass


def test_published_replay_snapshot_and_selected_rows_are_immutable() -> None:
    replay, inputs, _ = verified_replay()
    metric_sha = sha256(ROOT / "analytics/metrics/metric_registry.yml")
    with _test_connection() as conn:
        try:
            with conn.transaction():
                for case in ("pytest-8.0.0", "urllib3-2.0.0"):
                    load_case_into(conn, inputs, case)
                ids = load_replay_into(conn, replay, inputs, "0" * 40,
                                       model_digest(), metric_sha)
                snapshot_id = ids["urllib3-2.0.0"]
                now = conn.execute("SELECT now()").fetchone()[0]
                conn.execute(
                    """INSERT INTO core.publication_record
                       (analysis_snapshot_id,publication_manifest_sha256,
                        publication_fingerprint,metric_output_sha256,mart_output_sha256,
                        metric_output,mart_row_fingerprints,published_at)
                       VALUES (%s,%s,%s,%s,%s,'[]','{}',%s)""",
                    (snapshot_id, "1" * 64, "2" * 64, "3" * 64, "4" * 64, now),
                )
                conn.execute(
                    """UPDATE core.analysis_snapshot
                       SET state='PUBLISHED_VALIDATION',publication_manifest_sha256=%s,
                           publication_fingerprint=%s,published_at=%s
                       WHERE analysis_snapshot_id=%s""",
                    ("1" * 64, "2" * 64, now, snapshot_id),
                )
                candidate_id = conn.execute(
                    """SELECT candidate_id FROM core.snapshot_candidate
                       WHERE analysis_snapshot_id=%s LIMIT 1""", (snapshot_id,)
                ).fetchone()[0]
                finding_id = conn.execute(
                    """SELECT finding_id FROM core.snapshot_finding
                       WHERE analysis_snapshot_id=%s LIMIT 1""", (snapshot_id,)
                ).fetchone()[0]
                for statement, params in (
                    ("UPDATE core.analysis_snapshot SET state='DRAFT' "
                     "WHERE analysis_snapshot_id=%s", (snapshot_id,)),
                    ("DELETE FROM core.snapshot_candidate WHERE analysis_snapshot_id=%s "
                     "AND candidate_id=%s", (snapshot_id, candidate_id)),
                    ("UPDATE core.candidate SET candidate_status='WITHDRAWN' "
                     "WHERE candidate_id=%s", (candidate_id,)),
                    ("DELETE FROM core.lifecycle_finding WHERE finding_id=%s",
                     (finding_id,)),
                    ("DELETE FROM core.publication_record WHERE analysis_snapshot_id=%s",
                     (snapshot_id,)),
                ):
                    with pytest.raises(psycopg.Error), conn.transaction():
                        conn.execute(statement, params)
                raise _Rollback
        except _Rollback:
            pass
