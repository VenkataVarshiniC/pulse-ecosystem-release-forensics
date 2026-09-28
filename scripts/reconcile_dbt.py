"""Compare dbt staging/intermediate rows with the frozen M2.2 golden values."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from psycopg import sql

from pulse.phase2_postgres.loader import connect

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "validation" / "m2-3-dbt-reconciliation.json"
MODELS = {
    "stg_pulse__cases": "dbt_staging",
    "stg_pulse__memberships": "dbt_staging",
    "stg_pulse__collection_tasks": "dbt_staging",
    "stg_pulse__artifacts": "dbt_staging",
    "stg_pulse__dependency_observations": "dbt_staging",
    "stg_pulse__historical_pairs": "dbt_staging",
    "stg_pulse__candidates": "dbt_staging",
    "stg_pulse__reviews": "dbt_staging",
    "stg_pulse__sufficiency": "dbt_staging",
    "stg_pulse__findings": "dbt_staging",
    "stg_pulse__finding_support": "dbt_staging",
    "stg_pulse__snapshots": "dbt_staging",
    "int_case_repository": "dbt_intermediate",
    "int_collection_task_status": "dbt_intermediate",
    "int_repository_evidence": "dbt_intermediate",
    "int_candidate_terminal_review": "dbt_intermediate",
    "int_stage_sufficiency": "dbt_intermediate",
    "int_finding_evidence": "dbt_intermediate",
    "int_analysis_snapshot": "dbt_intermediate",
}


def main() -> int:
    checks: list[dict[str, Any]] = []
    with connect("pulse_dev") as conn:
        def check(check_id: str, expected: int, query: str, model: str,
                  params: tuple[Any, ...] = ()) -> None:
            actual = int(conn.execute(query, params).fetchone()[0])
            checks.append({
                "check_id": check_id, "expected": expected, "actual": actual,
                "status": "PASS" if actual == expected else "FAIL",
                "source_model": model,
            })

        check("cases", 2, "SELECT count(*) FROM dbt_staging.stg_pulse__cases",
              "stg_pulse__cases")
        check("members", 8, "SELECT count(*) FROM dbt_intermediate.int_case_repository",
              "int_case_repository")
        check("planned_release_tasks", 54,
              "SELECT count(*) FROM dbt_intermediate.int_collection_task_status",
              "int_collection_task_status")
        check("retries", 0,
              "SELECT sum(retry_count) FROM dbt_intermediate.int_collection_task_status",
              "int_collection_task_status")
        for case, members, required, optional, optional_404, paired in (
            ("pytest-8.0.0", 2, 11, 4, 1, 1),
            ("urllib3-2.0.0", 6, 27, 12, 5, 0),
        ):
            check(f"{case}.members", members, """SELECT count(*)
                FROM dbt_intermediate.int_case_repository WHERE case_name=%s""",
                "int_case_repository", (case,))
            check(f"{case}.core_collection_complete", members, """SELECT count(*)
                FROM dbt_intermediate.int_repository_evidence
                WHERE case_name=%s AND core_collection_complete""",
                "int_repository_evidence", (case,))
            check(f"{case}.required_tasks", required, """SELECT count(*)
                FROM dbt_intermediate.int_collection_task_status t
                JOIN dbt_staging.stg_pulse__cases c USING (case_version_id)
                WHERE c.case_name=%s AND t.required_flag""",
                "int_collection_task_status", (case,))
            check(f"{case}.required_succeeded", required, """SELECT count(*)
                FROM dbt_intermediate.int_collection_task_status t
                JOIN dbt_staging.stg_pulse__cases c USING (case_version_id)
                WHERE c.case_name=%s AND t.required_flag
                  AND t.terminal_status='succeeded'""",
                "int_collection_task_status", (case,))
            check(f"{case}.optional_tasks", optional, """SELECT count(*)
                FROM dbt_intermediate.int_collection_task_status t
                JOIN dbt_staging.stg_pulse__cases c USING (case_version_id)
                WHERE c.case_name=%s AND NOT t.required_flag""",
                "int_collection_task_status", (case,))
            check(f"{case}.optional_not_found", optional_404, """SELECT count(*)
                FROM dbt_intermediate.int_collection_task_status t
                JOIN dbt_staging.stg_pulse__cases c USING (case_version_id)
                WHERE c.case_name=%s AND NOT t.required_flag
                  AND t.terminal_status='not_found'""",
                "int_collection_task_status", (case,))
            check(f"{case}.paired_members", paired, """SELECT count(*)
                FROM dbt_intermediate.int_repository_evidence
                WHERE case_name=%s AND has_paired_pre_release_history""",
                "int_repository_evidence", (case,))
        for status, expected in (("PAIRED", 1), ("AFTER_ONLY", 6), ("UNRESOLVED", 9)):
            check(f"historical_pair.{status}", expected, """SELECT count(*)
                FROM dbt_staging.stg_pulse__historical_pairs WHERE pair_status=%s""",
                "stg_pulse__historical_pairs", (status,))
        check("candidates", 2,
              "SELECT count(*) FROM dbt_intermediate.int_candidate_terminal_review",
              "int_candidate_terminal_review")
        check("candidate_emitting_repositories", 1, """SELECT count(*)
            FROM dbt_intermediate.int_repository_evidence WHERE has_candidate""",
            "int_repository_evidence")
        check("shared_candidate_artifacts", 1, """SELECT count(DISTINCT artifact_id)
            FROM dbt_intermediate.int_candidate_terminal_review""",
            "int_candidate_terminal_review")
        for decision, expected in (("ACCEPT", 0), ("REJECT", 2)):
            check(f"reviews.{decision}", expected, """SELECT count(*)
                FROM dbt_intermediate.int_candidate_terminal_review
                WHERE latest_review_decision=%s""", "int_candidate_terminal_review",
                (decision,))
        for status, expected in (("SUFFICIENT", 2), ("LEGACY_UNCLASSIFIED", 38)):
            check(f"sufficiency.{status}", expected, """SELECT count(*)
                FROM dbt_intermediate.int_stage_sufficiency
                WHERE source_sufficiency_status=%s""", "int_stage_sufficiency",
                (status,))
        check("findings", 40,
              "SELECT count(*) FROM dbt_intermediate.int_finding_evidence",
              "int_finding_evidence")
        for status, expected in (("UNKNOWN", 38), ("NO_QUALIFYING_EVIDENCE_FOUND", 2)):
            check(f"findings.{status}", expected, """SELECT count(*)
                FROM dbt_intermediate.int_finding_evidence WHERE finding_status=%s""",
                "int_finding_evidence", (status,))
        for category in ("observed_adoption", "recovery_signal"):
            check(f"{category}.unknown", 8, """SELECT count(*)
                FROM dbt_intermediate.int_finding_evidence
                WHERE lifecycle_category=%s AND finding_status='UNKNOWN'""",
                "int_finding_evidence", (category,))
        check("draft_snapshots", 2, """SELECT count(*)
            FROM dbt_intermediate.int_analysis_snapshot WHERE snapshot_state='DRAFT'""",
            "int_analysis_snapshot")
        check("snapshot_artifact_digest_mismatches", 0, """SELECT sum(
            artifact_digest_mismatch_count) FROM dbt_intermediate.int_analysis_snapshot""",
            "int_analysis_snapshot")
        check("fixtures_in_source_captures", 0, """SELECT count(*)
            FROM dbt_staging.stg_pulse__artifacts WHERE capture_method='fixture'""",
            "stg_pulse__artifacts")
        check("noncollector_source_captures", 0, """SELECT count(*)
            FROM dbt_staging.stg_pulse__artifacts WHERE capture_method<>'collector'""",
            "stg_pulse__artifacts")
        row_counts = {}
        for model, schema in sorted(MODELS.items()):
            query = sql.SQL("SELECT count(*) FROM {}.{}").format(
                sql.Identifier(schema), sql.Identifier(model)
            )
            row_counts[model] = int(conn.execute(query).fetchone()[0])

    result = {
        "version": "m2-3-dbt-reconciliation-v1",
        "status": "PASS" if all(c["status"] == "PASS" for c in checks) else "FAIL",
        "checks": checks,
        "check_count": len(checks),
        "model_row_counts": row_counts,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"{result['status']}: {len(checks)} dbt/M2.2 checks across {len(row_counts)} models")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
