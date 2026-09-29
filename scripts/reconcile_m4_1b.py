"""Reconcile the governed replay against its frozen case and metric contracts."""

from __future__ import annotations

import argparse

from run_m4_1b_metric_pack import OUTPUT, canonical_bytes, replay_metrics

from pulse.phase2_postgres.loader import connect
from pulse.phase2_postgres.manifest import ROOT, sha256
from pulse.phase4_replay_db import CASES, REPLAY_SHA, RULE_RELEASE, model_digest

RECONCILIATION = ROOT / "data/validation/m4-1b-reconciliation.json"
MARTS = (
    "bridge_case_repository", "bridge_finding_evidence", "fct_candidate_review",
    "fct_collection_task", "fct_evidence_observation", "fct_lifecycle_finding",
    "fct_repository_investigation",
)


def _one(conn, query: str, params: tuple = ()) -> int:
    return int(conn.execute(query, params).fetchone()[0])


def reconcile(conn) -> dict:
    replay = replay_metrics(conn)
    if canonical_bytes(replay) != OUTPUT.read_bytes():
        raise ValueError("Replay metric output differs from live scoped execution")
    if sha256(ROOT / "data/processed/m4-1/replay.json") != REPLAY_SHA:
        raise ValueError("Pinned replay artifact changed")
    rows = conn.execute(
        """SELECT l.case_id,s.analysis_snapshot_id,s.state,s.model_version,
                  l.mart_model_sha256,l.metric_registry_sha256,l.rule_release_id
           FROM core.replay_snapshot_lineage l
           JOIN core.analysis_snapshot s USING(analysis_snapshot_id)
           ORDER BY l.case_id"""
    ).fetchall()
    if len(rows) != 2 or {row[0] for row in rows} != set(CASES):
        raise ValueError("Expected two separate governed replay case snapshots")
    if any(row[3] != "m4-1b-" + model_digest()[:16]
           or row[4].strip() != model_digest()
           or row[6] != RULE_RELEASE for row in rows):
        raise ValueError("Replay dbt model/rule binding changed")
    if _one(conn, """SELECT count(*) FROM core.analysis_snapshot
                   WHERE rule_version='unrecorded_in_frozen_report'
                     AND state='DRAFT'""") != 2:
        raise ValueError("Historical analytical snapshots changed from DRAFT")
    if _one(conn, "SELECT count(*) FROM core.analysis_snapshot") != 4:
        raise ValueError("Unexpected analytical snapshot population")
    counts = {
        "cases": len(rows),
        "members": _one(conn, """SELECT count(*) FROM analytics.fct_repository_investigation r
            JOIN core.replay_snapshot_lineage l USING(analysis_snapshot_id)"""),
        "selected_artifacts": _one(conn, """SELECT count(*) FROM core.snapshot_artifact a
            JOIN core.replay_snapshot_lineage l USING(analysis_snapshot_id)"""),
        "candidates": _one(conn, "SELECT count(*) FROM core.replay_candidate_lineage"),
        "candidate_artifacts": _one(conn, """SELECT count(DISTINCT c.artifact_id)
            FROM core.candidate c JOIN core.replay_candidate_lineage l USING(candidate_id)"""),
        "inherited_rejects": _one(conn, """SELECT count(*) FROM core.analyst_review r
            JOIN core.replay_candidate_lineage l ON r.review_id=l.replay_review_id
            WHERE r.review_origin='INHERITED' AND r.decision='REJECT'
              AND r.inherited_from_review_id=l.original_review_id"""),
        "sufficient": _one(conn, """SELECT count(*) FROM analytics.fct_lifecycle_finding f
            JOIN core.replay_snapshot_lineage l USING(analysis_snapshot_id)
            WHERE f.source_sufficiency_status='SUFFICIENT'"""),
        "insufficient": _one(conn, """SELECT count(*) FROM analytics.fct_lifecycle_finding f
            JOIN core.replay_snapshot_lineage l USING(analysis_snapshot_id)
            WHERE f.source_sufficiency_status='INSUFFICIENT'"""),
        "findings": _one(conn, """SELECT count(*) FROM analytics.fct_lifecycle_finding f
            JOIN core.replay_snapshot_lineage l USING(analysis_snapshot_id)"""),
        "unknown": _one(conn, """SELECT count(*) FROM analytics.fct_lifecycle_finding f
            JOIN core.replay_snapshot_lineage l USING(analysis_snapshot_id)
            WHERE f.finding_status='UNKNOWN'"""),
        "bounded_no": _one(conn, """SELECT count(*) FROM analytics.fct_lifecycle_finding f
            JOIN core.replay_snapshot_lineage l USING(analysis_snapshot_id)
            WHERE f.finding_status='NO_QUALIFYING_EVIDENCE_FOUND'"""),
        "false_outcomes": _one(conn, """SELECT count(*)
            FROM analytics.fct_repository_investigation f
            JOIN core.replay_snapshot_lineage l USING(analysis_snapshot_id)
            WHERE f.observed_adoption_status<>'UNKNOWN'
               OR f.recovery_signal_status<>'UNKNOWN'"""),
        "metric_outputs": len(replay["results"]),
        "mart_rows": {},
    }
    expected = {
        "cases": 2, "members": 8, "candidates": 2, "candidate_artifacts": 1,
        "inherited_rejects": 2, "sufficient": 2, "insufficient": 38,
        "findings": 40, "unknown": 38, "bounded_no": 2,
        "false_outcomes": 0, "metric_outputs": 46,
    }
    for key, value in expected.items():
        if counts[key] != value:
            raise ValueError(f"Replay reconciliation {key}: {counts[key]} != {value}")
    for mart in MARTS:
        counts["mart_rows"][mart] = _one(conn, f"""SELECT count(*) FROM analytics.{mart} m
            JOIN core.replay_snapshot_lineage l USING(analysis_snapshot_id)""")
    if counts["mart_rows"]["bridge_case_repository"] != 8:
        raise ValueError("Replay bridge member rows are incomplete")
    if counts["mart_rows"]["fct_candidate_review"] != 2:
        raise ValueError("Replay candidate mart rows are incomplete")
    if counts["mart_rows"]["fct_lifecycle_finding"] != 40:
        raise ValueError("Replay finding mart rows are incomplete")
    return {
        "release_id": replay["release_id"],
        "snapshot_ids": replay["snapshot_ids"],
        "snapshot_states": {row[0]: row[2] for row in rows},
        "metric_sha256": sha256(OUTPUT),
        "counts": counts,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    with connect("pulse_dev") as conn:
        payload = reconcile(conn)
    data = canonical_bytes(payload)
    if args.check:
        if RECONCILIATION.read_bytes() != data:
            raise ValueError("Committed replay reconciliation changed")
    else:
        RECONCILIATION.write_bytes(data)
    print(f"PASS: replay reconciliation {payload['counts']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
