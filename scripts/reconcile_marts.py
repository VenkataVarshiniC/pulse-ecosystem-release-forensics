"""Reconcile snapshot-scoped analytics marts to the frozen M2.2/M2.3 baseline."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from psycopg import sql

from pulse.phase2_postgres.loader import connect

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "validation" / "m2-4-mart-reconciliation.json"
MARTS = (
    "dim_case", "dim_repository", "dim_release", "dim_evidence_source",
    "bridge_case_repository", "bridge_finding_evidence", "fct_collection_task",
    "fct_repository_investigation", "fct_candidate_review", "fct_lifecycle_finding",
    "fct_evidence_observation",
)


def main() -> int:
    checks: list[dict[str, Any]] = []
    with connect("pulse_dev") as conn:

        def check(check_id: str, expected: int, query: str | sql.Composable, model: str,
                  params: tuple[Any, ...] = ()) -> None:
            actual = int(conn.execute(query, params).fetchone()[0])
            checks.append({
                "check_id": check_id, "expected": expected, "actual": actual,
                "status": "PASS" if actual == expected else "FAIL", "source_model": model,
            })

        for model, expected in (
            ("dim_case", 2), ("dim_repository", 8), ("dim_release", 2),
            ("bridge_case_repository", 8), ("bridge_finding_evidence", 0),
            ("fct_collection_task", 54), ("fct_repository_investigation", 8),
            ("fct_candidate_review", 2), ("fct_lifecycle_finding", 40),
            ("fct_evidence_observation", 11),
        ):
            check(f"rows.{model}", expected,
                  sql.SQL("SELECT count(*) FROM analytics.{}").format(
                      sql.Identifier(model)), model)
        check("source_definitions_represented", 9,
              "SELECT count(*) FROM analytics.dim_evidence_source", "dim_evidence_source")
        for case, members, required, optional_not_found, paired in (
            ("pytest-8.0.0", 2, 11, 1, 1),
            ("urllib3-2.0.0", 6, 27, 5, 0),
        ):
            check(f"{case}.members", members, """SELECT count(*)
                FROM analytics.bridge_case_repository b
                JOIN analytics.dim_case c ON b.case_key = c.case_key
                WHERE c.case_name=%s""", "bridge_case_repository", (case,))
            check(f"{case}.required_succeeded", required, """SELECT count(*)
                FROM analytics.fct_collection_task t
                JOIN analytics.dim_case c ON t.case_key = c.case_key
                WHERE c.case_name=%s AND t.required_flag AND t.terminal_status='succeeded'""",
                  "fct_collection_task", (case,))
            check(f"{case}.optional_not_found", optional_not_found, """SELECT count(*)
                FROM analytics.fct_collection_task t
                JOIN analytics.dim_case c ON t.case_key = c.case_key
                WHERE c.case_name=%s AND t.optional_not_found""",
                  "fct_collection_task", (case,))
            check(f"{case}.paired", paired, """SELECT count(*)
                FROM analytics.fct_repository_investigation r
                JOIN analytics.dim_case c ON r.case_key = c.case_key
                WHERE c.case_name=%s AND r.has_paired_pre_release_history""",
                  "fct_repository_investigation", (case,))
        for field, expected in (("paired_path_count", 1), ("after_only_path_count", 6),
                                ("unresolved_path_count", 9)):
            check(f"history.{field}", expected,
                  f"SELECT sum({field}) FROM analytics.fct_repository_investigation",
                  "fct_repository_investigation")
        check("candidate_emitting_repositories", 1, """SELECT count(*)
            FROM analytics.fct_repository_investigation WHERE candidate_count > 0""",
              "fct_repository_investigation")
        check("shared_candidate_artifacts", 1, """SELECT count(DISTINCT artifact_id)
            FROM analytics.fct_candidate_review""", "fct_candidate_review")
        for decision, expected in (("ACCEPT", 0), ("REJECT", 2)):
            check(f"reviews.{decision}", expected, """SELECT count(*)
                FROM analytics.fct_candidate_review WHERE terminal_review_status=%s""",
                  "fct_candidate_review", (decision,))
        for status, expected in (("SUFFICIENT", 2), ("LEGACY_UNCLASSIFIED", 38)):
            check(f"sufficiency.{status}", expected, """SELECT count(*)
                FROM analytics.fct_lifecycle_finding WHERE source_sufficiency_status=%s""",
                  "fct_lifecycle_finding", (status,))
        for status, expected in (("UNKNOWN", 38), ("NO_QUALIFYING_EVIDENCE_FOUND", 2)):
            check(f"findings.{status}", expected, """SELECT count(*)
                FROM analytics.fct_lifecycle_finding WHERE finding_status=%s""",
                  "fct_lifecycle_finding", (status,))
        for field in ("observed_adoption_status", "recovery_signal_status"):
            check(f"{field}.unknown", 8, f"""SELECT count(*)
                FROM analytics.fct_repository_investigation WHERE {field}='UNKNOWN'""",
                  "fct_repository_investigation")
        check("zero_candidate_denominator", 2, """SELECT count(*)
            FROM analytics.fct_repository_investigation r
            JOIN analytics.dim_case c ON r.case_key=c.case_key
            WHERE c.case_name='pytest-8.0.0' AND r.terminal_review_denominator=0
              AND NOT r.reviewed_acceptance_available""", "fct_repository_investigation")
        check("fixture_mart_rows", 0, """SELECT
            (SELECT count(*) FROM analytics.fct_candidate_review WHERE capture_method='fixture')
          + (SELECT count(*) FROM analytics.fct_evidence_observation
             WHERE capture_method='fixture')""", "fct_candidate_review/fct_evidence_observation")
        check("snapshot_manifest_mismatches", 0, """SELECT count(*)
            FROM analytics.bridge_case_repository b
            JOIN core.analysis_snapshot s ON b.analysis_snapshot_id=s.analysis_snapshot_id
            WHERE b.input_manifest_sha256<>s.manifest_sha256
               OR b.snapshot_state<>s.state OR b.case_version_id<>s.case_version_id""",
              "bridge_case_repository")
        check("draft_snapshots", 2, """SELECT count(*)
            FROM core.analysis_snapshot WHERE state='DRAFT'""", "core.analysis_snapshot")
        check("published_snapshots", 0, """SELECT count(*)
            FROM core.analysis_snapshot WHERE state='PUBLISHED'""", "core.analysis_snapshot")
        check("snapshot_artifact_digest_mismatches", 0, """SELECT sum(
            artifact_digest_mismatch_count) FROM dbt_intermediate.int_analysis_snapshot""",
              "int_analysis_snapshot")
        check("mart_grain_duplicates", 0, """SELECT count(*) FROM (
            SELECT analysis_snapshot_id, case_version_id, repository_id
            FROM analytics.fct_repository_investigation
            GROUP BY 1,2,3 HAVING count(*) > 1
        ) d""", "fct_repository_investigation")
        check("orphan_repository_keys", 0, """SELECT count(*)
            FROM analytics.fct_repository_investigation f
            LEFT JOIN analytics.dim_repository d ON f.repository_key=d.repository_key
            WHERE d.repository_key IS NULL""", "fct_repository_investigation")
        model_row_counts = {}
        for model in MARTS:
            query = sql.SQL("SELECT count(*) FROM analytics.{}").format(sql.Identifier(model))
            model_row_counts[model] = int(conn.execute(query).fetchone()[0])
        snapshots = [{
            "analysis_snapshot_id": str(row[0]), "case_version_id": str(row[1]),
            "state": row[2], "input_manifest_sha256": row[3],
            "source_rule_version": row[4], "source_metric_definition_version": row[5],
            "source_model_version": row[6],
        } for row in conn.execute("""SELECT analysis_snapshot_id, case_version_id, state,
            manifest_sha256, rule_version, metric_definition_version, model_version
            FROM core.analysis_snapshot ORDER BY analysis_snapshot_id""")]

    blockers = sorted({
        reason
        for snapshot in snapshots
        for reason, blocked in (
            ("INPUT_SNAPSHOT_DRAFT", snapshot["state"] == "DRAFT"),
            ("RULE_VERSION_UNRECORDED",
             snapshot["source_rule_version"] == "unrecorded_in_frozen_report"),
            ("METRIC_VERSION_UNMODELED",
             snapshot["source_metric_definition_version"] == "not_yet_modeled"),
            ("MART_MODEL_VERSION_NOT_IN_INPUT_MANIFEST",
             snapshot["source_model_version"] != "m2-4-validation-v1"),
        ) if blocked
    })
    result = {
        "version": "m2-4-mart-reconciliation-v1",
        "status": "PASS" if all(c["status"] == "PASS" for c in checks) else "FAIL",
        "check_count": len(checks), "checks": checks,
        "mart_row_counts": model_row_counts,
        "snapshot_publication": {
            "published_count": sum(s["state"] == "PUBLISHED" for s in snapshots),
            "blocker_codes": blockers,
            "status": "NOT_PUBLISHED" if not any(
                s["state"] == "PUBLISHED" for s in snapshots
            ) else "PUBLISHED",
        },
        "snapshots": snapshots,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"{result['status']}: {len(checks)} mart/M2.2 checks across {len(MARTS)} marts")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
