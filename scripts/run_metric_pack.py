"""Execute the governed M2.5 metric and diagnostic SQL against frozen local marts."""

from __future__ import annotations

import hashlib
import json
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from uuid import UUID

import yaml
from psycopg.rows import dict_row

from pulse.phase2_postgres.loader import connect

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "analytics/metrics/metric_registry.yml"
SQL = ROOT / "analytics/sql"
OUTPUT = ROOT / "data/validation/m2-5-metric-baseline.json"
DIAGNOSTICS = ROOT / "data/validation/m2-5-sql-diagnostics.json"
READY_QUERIES = ("member_coverage", "candidate_review", "collection_reliability")
DIAGNOSTIC_QUERIES = (
    "investigation_funnel", "evidence_gaps", "source_coverage",
    "case_comparison", "segment_inventory",
)
ALLOWED = {
    "READY": 10, "PARTIAL_EVIDENCE": 6, "PARTIAL_PLATFORM": 1,
    "UNAVAILABLE_EVIDENCE": 5, "BLOCKED_STAKEHOLDER": 1,
}
FIELDS = {
    "name", "purpose", "grain", "numerator", "denominator", "source_marts",
    "filters", "valid_population", "null_behavior", "status", "evidence_dependency",
    "stakeholder_dependency",
}


def registry() -> dict:
    result = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    metrics = result["metrics"]
    assert set(metrics) == {f"MET-{n:03}" for n in range(1, 24)}
    assert {status: sum(m["status"] == status for m in metrics.values())
            for status in ALLOWED} == ALLOWED
    for metric in metrics.values():
        assert metric.keys() >= FIELDS
        assert metric["source_marts"]
    return result


def serializable(value):
    if isinstance(value, (UUID, date, datetime)):
        return str(value)
    if isinstance(value, Decimal):
        return str(value)
    raise TypeError(type(value).__name__)


def write_json(path: Path, payload: dict) -> str:
    data = (json.dumps(payload, indent=2, sort_keys=True, default=serializable) + "\n").encode()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return hashlib.sha256(data).hexdigest()


def resolved_metric(contract: dict, row: dict | None, case: dict) -> dict:
    status = contract["status"]
    result_status = status
    numerator = denominator = value = None
    reason = None
    component_scope = None
    if status == "READY":
        assert row is not None
        numerator, denominator = row["numerator"], row["denominator"]
        assert numerator is not None and denominator is not None
        if denominator == 0:
            reason = "ZERO_DENOMINATOR: mathematically undefined; no eligible observations"
            result_status = "UNAVAILABLE_ZERO_DENOMINATOR"
        else:
            assert row["metric_value"] is not None
            value = str(row["metric_value"].quantize(Decimal("0.000001")))
    elif status.startswith("PARTIAL"):
        assert row is not None
        numerator = row["observed_numerator"]
        denominator = row["observed_denominator"]
        component_scope = row["component_scope"]
        reason = contract["evidence_dependency"]
    else:
        reason = contract["evidence_dependency"]
    return {
        "metric_id": contract["metric_id"], "name": contract["name"],
        "case": case["case_name"], "case_version_id": str(case["case_version_id"]),
        "analysis_snapshot_id": str(case["analysis_snapshot_id"]),
        "snapshot_state": case["snapshot_state"],
        "numerator": numerator, "denominator": denominator,
        "metric_value": value, "status": result_status, "contract_status": status,
        "unavailable_reason": reason,
        "component_scope": component_scope,
        "source_marts": contract["source_marts"],
        "metric_contract_version": contract["contract_version"],
    }


def execute(conn, filename: Path, params: dict | None = None) -> list[dict]:
    with conn.cursor(row_factory=dict_row) as cursor:
        cursor.execute(filename.read_text(encoding="utf-8"), params)
        return cursor.fetchall()


def main() -> int:
    spec = registry()
    contracts = {
        mid: {**body, "metric_id": mid, "contract_version": spec["contract_version"]}
        for mid, body in spec["metrics"].items()
    }
    with connect("pulse_dev") as conn:
        cases = execute(conn, ROOT / "analytics/sql/validation/snapshot_scope.sql")
        assert len(cases) == 2 and {c["case_name"] for c in cases} == {"pytest", "urllib3"}
        assert all(c["snapshot_state"] == "DRAFT" for c in cases)
        outputs = []
        diagnostics: dict[str, list[dict]] = {}
        for case in cases:
            scope = {"snapshot_id": case["analysis_snapshot_id"]}
            ready_rows = [row for query in READY_QUERIES
                          for row in execute(conn, SQL / "metrics" / f"{query}.sql", scope)]
            partial_rows = execute(conn, SQL / "metrics/partial_components.sql", scope)
            rows = {row["metric_id"]: row for row in ready_rows + partial_rows}
            assert len(rows) == len(ready_rows) + len(partial_rows) == 17
            assert {mid for mid, c in contracts.items() if c["status"] == "READY"} == {
                row["metric_id"] for row in ready_rows
            }
            for mid, contract in contracts.items():
                outputs.append(resolved_metric(contract, rows.get(mid), case))
            for query in DIAGNOSTIC_QUERIES[:3]:
                diagnostics[f"{case['case_name']}/{query}"] = execute(
                    conn, SQL / "diagnostics" / f"{query}.sql", scope
                )
        for query in DIAGNOSTIC_QUERIES[3:]:
            diagnostics[query] = execute(conn, SQL / "diagnostics" / f"{query}.sql")
        failures = execute(conn, SQL / "validation/metric_assertions.sql")
        if failures:
            raise AssertionError(f"Metric assertions failed: {failures}")
    assert len(outputs) == 46
    baseline = {
        "contract_version": spec["contract_version"],
        "registry_sha256": hashlib.sha256(REGISTRY.read_bytes()).hexdigest(),
        "scope": "two frozen Phase 2 validation cases; DRAFT analytical snapshots",
        "metrics_per_case": 23, "cases": [c["case_name"] for c in cases],
        "results": outputs,
    }
    metric_digest = write_json(OUTPUT, baseline)
    diagnostic_digest = write_json(DIAGNOSTICS, diagnostics)
    print(f"PASS: 23 metrics x 2 cases; SQL assertions; baseline sha256={metric_digest}")
    print(f"Diagnostics sha256={diagnostic_digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
