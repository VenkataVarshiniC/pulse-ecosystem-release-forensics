"""Direct SQL checks against the predeclared Phase 2 golden values."""

from __future__ import annotations

from typing import Any

import psycopg

from pulse.phase2_postgres.loader import identity

EXPECTED = {
    "pytest-8.0.0": {
        "members": 2, "core_collection": 2, "tasks": 15,
        "required_tasks": 11, "required_succeeded": 11,
        "optional_tasks": 4, "optional_not_found": 1,
        "attempts": 15, "retries": 0, "historical_declaration_members": 1,
        "paired_pre_release": 1, "candidates": 0,
        "candidate_emitting_members": 0, "reviews_accepted": 0,
        "reviews_rejected": 0, "replay_matches": 2,
        "artifacts": 21, "observations": 5, "historical_pairs": 4,
        "assessments": 10, "findings": 10,
        "observed_adoption_unknown": 2, "recovery_unknown": 2,
    },
    "urllib3-2.0.0": {
        "members": 6, "core_collection": 6, "tasks": 39,
        "required_tasks": 27, "required_succeeded": 27,
        "optional_tasks": 12, "optional_not_found": 5,
        "attempts": 39, "retries": 0, "historical_declaration_members": 1,
        "paired_pre_release": 0, "candidates": 2,
        "candidate_emitting_members": 1, "reviews_accepted": 0,
        "reviews_rejected": 2, "replay_matches": 2,
        "artifacts": 51, "observations": 6, "historical_pairs": 12,
        "assessments": 30, "findings": 30,
        "observed_adoption_unknown": 6, "recovery_unknown": 6,
    },
}

COUNT_TABLES = (
    "ingestion.source_registry", "core.dependency_release", "core.repository",
    "core.repository_alias", "core.investigation_case", "core.cohort_membership",
    "ingestion.collection_run", "ingestion.collection_task", "ingestion.task_attempt",
    "core.evidence_artifact", "core.external_evidence_reference",
    "core.dependency_observation", "core.historical_pair", "core.candidate",
    "core.analyst_review", "core.sufficiency_assessment",
    "core.assessment_source_reason", "core.lifecycle_finding",
    "core.finding_artifact_support", "core.finding_observation_support",
    "core.finding_review_support", "ingestion.replay_attempt",
    "core.analysis_snapshot", "core.snapshot_run", "core.snapshot_artifact",
    "core.snapshot_candidate", "core.snapshot_review",
    "core.snapshot_assessment", "core.snapshot_finding", "ingestion.load_audit",
)


def _count(conn: psycopg.Connection[Any], sql: str, *parameters: Any) -> int:
    return int(conn.execute(sql, parameters).fetchone()[0])


def actual_case(conn: psycopg.Connection[Any], case: str) -> dict[str, int]:
    case_id = identity("case-version", case, 1)
    result = {
        "members": _count(conn,
            "SELECT count(*) FROM core.cohort_membership WHERE case_version_id=%s", case_id),
        "tasks": _count(conn,
            "SELECT count(*) FROM ingestion.collection_task WHERE case_version_id=%s", case_id),
        "required_tasks": _count(conn,
            """SELECT count(*) FROM ingestion.collection_task
               WHERE case_version_id=%s AND required_flag""",
            case_id),
        "required_succeeded": _count(conn,
            """SELECT count(*) FROM ingestion.collection_task
               WHERE case_version_id=%s AND required_flag AND terminal_status='succeeded'""",
            case_id),
        "optional_tasks": _count(conn,
            """SELECT count(*) FROM ingestion.collection_task
               WHERE case_version_id=%s AND NOT required_flag""",
            case_id),
        "optional_not_found": _count(conn,
            """SELECT count(*) FROM ingestion.collection_task WHERE case_version_id=%s
               AND NOT required_flag AND terminal_status='not_found'""", case_id),
        "attempts": _count(conn,
            """SELECT count(*) FROM ingestion.task_attempt a
               JOIN ingestion.collection_task t USING (collection_task_id)
               WHERE t.case_version_id=%s""", case_id),
        "retries": _count(conn,
            """SELECT count(*) FROM ingestion.task_attempt a
               JOIN ingestion.collection_task t USING (collection_task_id)
               WHERE t.case_version_id=%s AND a.attempt_number>1""", case_id),
        "artifacts": _count(conn,
            """SELECT count(*) FROM core.evidence_artifact a
               JOIN core.snapshot_artifact sa USING (artifact_id)
               JOIN core.analysis_snapshot s USING (analysis_snapshot_id)
               WHERE s.case_version_id=%s""", case_id),
        "observations": _count(conn,
            "SELECT count(*) FROM core.dependency_observation WHERE case_version_id=%s", case_id),
        "historical_declaration_members": _count(conn,
            """SELECT count(DISTINCT repository_id) FROM core.dependency_observation
               WHERE case_version_id=%s AND observation_type='HISTORICAL_DECLARATION'""",
            case_id),
        "historical_pairs": _count(conn,
            "SELECT count(*) FROM core.historical_pair WHERE case_version_id=%s", case_id),
        "paired_pre_release": _count(conn,
            """SELECT count(DISTINCT repository_id) FROM core.historical_pair
               WHERE case_version_id=%s AND pair_status='PAIRED'""", case_id),
        "candidates": _count(conn,
            "SELECT count(*) FROM core.candidate WHERE case_version_id=%s", case_id),
        "candidate_emitting_members": _count(conn,
            "SELECT count(DISTINCT repository_id) FROM core.candidate WHERE case_version_id=%s",
            case_id),
        "reviews_accepted": _count(conn,
            """SELECT count(*) FROM core.analyst_review r
               JOIN core.candidate c USING (candidate_id)
               WHERE c.case_version_id=%s AND r.decision='ACCEPT'""", case_id),
        "reviews_rejected": _count(conn,
            """SELECT count(*) FROM core.analyst_review r
               JOIN core.candidate c USING (candidate_id)
               WHERE c.case_version_id=%s AND r.decision='REJECT'""", case_id),
        "replay_matches": _count(conn,
            """SELECT count(*) FROM ingestion.replay_attempt
               WHERE case_version_id=%s AND matched_frozen_outputs""", case_id),
        "assessments": _count(conn,
            "SELECT count(*) FROM core.sufficiency_assessment WHERE case_version_id=%s", case_id),
        "findings": _count(conn,
            "SELECT count(*) FROM core.lifecycle_finding WHERE case_version_id=%s", case_id),
        "observed_adoption_unknown": _count(conn,
            """SELECT count(*) FROM core.lifecycle_finding WHERE case_version_id=%s
               AND lifecycle_category='observed_adoption' AND finding_status='UNKNOWN'""",
            case_id),
        "recovery_unknown": _count(conn,
            """SELECT count(*) FROM core.lifecycle_finding WHERE case_version_id=%s
               AND lifecycle_category='recovery_signal' AND finding_status='UNKNOWN'""",
            case_id),
    }
    result["core_collection"] = _count(conn,
        """SELECT count(*) FROM core.cohort_membership m
           WHERE m.case_version_id=%s
             AND NOT EXISTS (
               SELECT 1 FROM ingestion.collection_task t
               WHERE t.case_version_id=m.case_version_id AND t.required_flag
                 AND (t.repository_id=m.repository_id OR t.repository_id IS NULL)
                 AND t.terminal_status<>'succeeded')
             AND EXISTS (
               SELECT 1 FROM ingestion.collection_task t
               WHERE t.case_version_id=m.case_version_id AND t.repository_id=m.repository_id
                 AND t.required_flag)""", case_id)
    return result


def reconcile(conn: psycopg.Connection[Any]) -> dict[str, Any]:
    cases: dict[str, Any] = {}
    for case, expected in EXPECTED.items():
        actual = actual_case(conn, case)
        cases[case] = {
            key: {"expected": value, "actual": actual[key],
                  "status": "PASS" if actual[key] == value else "FAIL"}
            for key, value in expected.items()
        }
    global_checks = {
        "two_candidates_one_artifact": (
            1, _count(conn, """SELECT count(*) FROM (
                SELECT artifact_id FROM core.candidate
                GROUP BY artifact_id HAVING count(*)=2) x""")),
        "findings_total": (40, _count(conn, "SELECT count(*) FROM core.lifecycle_finding")),
        "published_snapshots": (0, _count(conn,
            "SELECT count(*) FROM core.analysis_snapshot WHERE state='PUBLISHED'")),
        "fixture_artifacts": (0, _count(conn,
            "SELECT count(*) FROM core.evidence_artifact WHERE capture_method='fixture'")),
        "non_collector_artifacts": (0, _count(conn,
            "SELECT count(*) FROM core.evidence_artifact WHERE capture_method<>'collector'")),
        "candidate_without_artifact": (0, _count(conn, """SELECT count(*) FROM core.candidate c
            LEFT JOIN core.evidence_artifact a USING (artifact_id) WHERE a.artifact_id IS NULL""")),
        "review_without_candidate": (0, _count(conn, """SELECT count(*) FROM core.analyst_review r
            LEFT JOIN core.candidate c USING (candidate_id) WHERE c.candidate_id IS NULL""")),
        "finding_without_assessment": (0, _count(conn, """SELECT count(*)
            FROM core.lifecycle_finding f
            LEFT JOIN core.sufficiency_assessment a
              ON a.assessment_id=f.sufficiency_assessment_id
            WHERE a.assessment_id IS NULL""")),
        "membership_without_repository": (0, _count(conn, """SELECT count(*)
            FROM core.cohort_membership m LEFT JOIN core.repository r USING (repository_id)
            WHERE r.repository_id IS NULL""")),
        "task_without_source": (0, _count(conn, """SELECT count(*)
            FROM ingestion.collection_task t LEFT JOIN ingestion.source_registry s
              USING (source_id) WHERE s.source_id IS NULL""")),
        "artifact_without_collector_provenance": (0, _count(conn, """SELECT count(*)
            FROM core.evidence_artifact WHERE capture_method='collector'
              AND ((collection_task_id IS NOT NULL) = (history_run_id IS NOT NULL))""")),
        "observation_without_artifact": (0, _count(conn, """SELECT count(*)
            FROM core.dependency_observation o LEFT JOIN core.evidence_artifact a
              USING (artifact_id) WHERE a.artifact_id IS NULL""")),
        "assessment_without_member": (0, _count(conn, """SELECT count(*)
            FROM core.sufficiency_assessment a LEFT JOIN core.cohort_membership m
              USING (case_version_id,repository_id) WHERE m.repository_id IS NULL""")),
        "support_edges_without_parent": (0, _count(conn, """SELECT
              (SELECT count(*) FROM core.finding_artifact_support s
                LEFT JOIN core.lifecycle_finding f USING (finding_id)
                LEFT JOIN core.evidence_artifact a USING (artifact_id)
                WHERE f.finding_id IS NULL OR a.artifact_id IS NULL)
            + (SELECT count(*) FROM core.finding_observation_support s
                LEFT JOIN core.lifecycle_finding f USING (finding_id)
                LEFT JOIN core.dependency_observation o USING (observation_id)
                WHERE f.finding_id IS NULL OR o.observation_id IS NULL)
            + (SELECT count(*) FROM core.finding_review_support s
                LEFT JOIN core.lifecycle_finding f USING (finding_id)
                LEFT JOIN core.analyst_review r USING (review_id)
                WHERE f.finding_id IS NULL OR r.review_id IS NULL)""")),
        "duplicate_task_business_keys": (0, _count(conn, """SELECT count(*) FROM (
            SELECT collection_run_id,plan_task_key FROM ingestion.collection_task
            GROUP BY 1,2 HAVING count(*)>1) d""")),
        "duplicate_candidate_source_keys": (0, _count(conn, """SELECT count(*) FROM (
            SELECT candidate_fingerprint FROM core.candidate
            GROUP BY 1 HAVING count(*)>1) d""")),
        "qualifying_findings": (0, _count(conn, """SELECT count(*) FROM core.lifecycle_finding
            WHERE finding_status='QUALIFYING_EVIDENCE'""")),
        "finding_support_edges": (0, _count(conn, """SELECT
            (SELECT count(*) FROM core.finding_artifact_support)
          + (SELECT count(*) FROM core.finding_observation_support)
          + (SELECT count(*) FROM core.finding_review_support)""")),
        "case_population": (2, _count(conn, "SELECT count(*) FROM core.investigation_case")),
        "member_population": (8, _count(conn, "SELECT count(*) FROM core.cohort_membership")),
    }
    global_result = {
        name: {"expected": expected, "actual": actual,
               "status": "PASS" if expected == actual else "FAIL"}
        for name, (expected, actual) in global_checks.items()
    }
    statuses = [v["status"] for case in cases.values() for v in case.values()]
    statuses.extend(v["status"] for v in global_result.values())
    return {
        "version": "m2-2-golden-v1", "cases": cases, "global": global_result,
        "status": "PASS" if all(s == "PASS" for s in statuses) else "FAIL",
        "checks": len(statuses),
        "row_counts": {table: _count(conn, f"SELECT count(*) FROM {table}")
                       for table in COUNT_TABLES},
        "assessment_status_counts": dict(conn.execute("""SELECT sufficiency_status,count(*)
            FROM core.sufficiency_assessment GROUP BY 1 ORDER BY 1""").fetchall()),
        "finding_status_counts": dict(conn.execute("""SELECT finding_status,count(*)
            FROM core.lifecycle_finding GROUP BY 1 ORDER BY 1""").fetchall()),
        "historical_pair_status_counts": dict(conn.execute("""SELECT pair_status,count(*)
            FROM core.historical_pair GROUP BY 1 ORDER BY 1""").fetchall()),
    }
