"""Reproducible samples linking typed rows to the verified frozen source files."""

from __future__ import annotations

from typing import Any

import psycopg

from pulse.phase2_postgres.manifest import VerifiedInputs


def _one(conn: psycopg.Connection[Any], sql: str) -> tuple[Any, ...]:
    row = conn.execute(sql).fetchone()
    if row is None:
        raise ValueError("Required frozen lineage sample is absent")
    return row


def lineage(conn: psycopg.Connection[Any], inputs: VerifiedInputs) -> dict[str, Any]:
    source_hashes = {
        f"{entry['root']}/{entry['path']}": entry["sha256"]
        for entry in inputs.manifest["inputs"]
    }
    member = _one(conn, """SELECT c.case_name,r.canonical_full_name,
        ra.supporting_artifact_id::text,a.raw_snapshot_uri,a.content_sha256
        FROM core.cohort_membership m
        JOIN core.investigation_case c USING (case_version_id)
        JOIN core.repository r USING (repository_id)
        JOIN core.repository_alias ra USING (repository_id)
        JOIN core.evidence_artifact a ON a.artifact_id=ra.supporting_artifact_id
        WHERE c.case_name='pytest-8.0.0'
        ORDER BY r.canonical_full_name LIMIT 1""")
    task = _one(conn, """SELECT t.plan_task_key,t.terminal_status,
        r.canonical_full_name,a.raw_snapshot_uri,a.content_sha256
        FROM ingestion.collection_task t
        JOIN core.investigation_case c USING (case_version_id)
        JOIN core.repository r USING (repository_id)
        JOIN core.evidence_artifact a USING (collection_task_id)
        WHERE c.case_name='pytest-8.0.0'
        ORDER BY t.plan_task_key LIMIT 1""")
    candidates = conn.execute("""SELECT c.candidate_id::text,c.artifact_id::text,
        a.raw_snapshot_uri,a.content_sha256,r.decision,r.reason_code
        FROM core.candidate c
        JOIN core.evidence_artifact a USING (artifact_id)
        JOIN core.analyst_review r USING (candidate_id)
        ORDER BY c.candidate_id""").fetchall()
    historical = _one(conn, """SELECT o.observation_id::text,o.observation_type,
        o.repository_ref,a.raw_snapshot_uri,a.content_sha256
        FROM core.dependency_observation o
        JOIN core.evidence_artifact a USING (artifact_id)
        WHERE o.observation_type='HISTORICAL_DECLARATION'
        ORDER BY o.observation_id LIMIT 1""")
    unknown = _one(conn, """SELECT f.finding_id::text,f.finding_status,
        f.lifecycle_category,s.sufficiency_status,c.case_name,
        count(sf.analysis_snapshot_id)
        FROM core.lifecycle_finding f
        JOIN core.sufficiency_assessment s
          ON s.assessment_id=f.sufficiency_assessment_id
        JOIN core.investigation_case c ON c.case_version_id=f.case_version_id
        LEFT JOIN core.snapshot_finding sf USING (finding_id)
        WHERE f.lifecycle_category='observed_adoption'
        GROUP BY f.finding_id,s.sufficiency_status,c.case_name
        ORDER BY c.case_name,f.finding_id LIMIT 1""")
    checks = {
        "member_alias_capture_hash_matches_manifest": source_hashes.get(member[3]) == member[4],
        "task_capture_hash_matches_manifest": source_hashes.get(task[3]) == task[4],
        "historical_capture_hash_matches_manifest": (
            source_hashes.get(historical[3]) == historical[4]
        ),
        "two_candidates_share_one_artifact": (
            len(candidates) == 2 and len({row[1] for row in candidates}) == 1
        ),
        "candidate_artifact_hash_matches_manifest": all(
            source_hashes.get(row[2]) == row[3] for row in candidates
        ),
        "both_reviews_reject": all(row[4] == "REJECT" for row in candidates),
        "unknown_finding_in_draft_snapshot": (
            unknown[1] == "UNKNOWN" and unknown[5] == 1
        ),
    }
    return {
        "version": "m2-2-lineage-v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "membership": {"case": member[0], "repository": member[1],
                       "supporting_artifact_id": member[2],
                       "raw_snapshot_uri": member[3], "sha256": member[4]},
        "task": {"plan_task_key": task[0], "terminal_status": task[1],
                 "repository": task[2], "raw_snapshot_uri": task[3], "sha256": task[4]},
        "candidates_and_reviews": [
            {"candidate_id": row[0], "artifact_id": row[1],
             "raw_snapshot_uri": row[2], "sha256": row[3],
             "review_decision": row[4], "reason_code": row[5]}
            for row in candidates
        ],
        "historical_observation": {
            "observation_id": historical[0], "type": historical[1],
            "repository_ref": historical[2], "raw_snapshot_uri": historical[3],
            "sha256": historical[4],
        },
        "unknown_finding": {
            "finding_id": unknown[0], "finding_status": unknown[1],
            "category": unknown[2], "sufficiency_status": unknown[3],
            "case": unknown[4], "draft_snapshot_links": unknown[5],
        },
    }
