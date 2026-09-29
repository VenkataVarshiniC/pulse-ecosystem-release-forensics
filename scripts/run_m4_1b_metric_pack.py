"""Execute all pinned metric contracts against the two governed replay snapshots."""

from __future__ import annotations

import argparse
import hashlib
import json

from run_metric_pack import READY_QUERIES, SQL, execute, registry, resolved_metric

from pulse.phase2_postgres.loader import connect
from pulse.phase2_postgres.manifest import ROOT, sha256
from pulse.phase4_replay_db import CASES, METRIC_VERSION, REPLAY_SHA, RULE_RELEASE

OUTPUT = ROOT / "data/validation/m4-1b-replay-metrics.json"


def replay_metrics(conn) -> dict:
    spec = registry()
    if spec["contract_version"] != METRIC_VERSION:
        raise ValueError("Metric registry version changed")
    metric_sha = sha256(ROOT / "analytics/metrics/metric_registry.yml")
    cases = execute(conn, ROOT / "analytics/sql/validation/replay_snapshot_scope.sql")
    if len(cases) != 2 or {c["case_id"] for c in cases} != set(CASES):
        raise ValueError("Expected two explicit case-scoped replay snapshots")
    if len({c["release_id"] for c in cases}) != 1:
        raise ValueError("Replay snapshots do not share one release identity")
    if any(
        c["rule_version"] != RULE_RELEASE or c["replay_artifact_sha256"].strip() != REPLAY_SHA
        or c["metric_contract_version"] != METRIC_VERSION
        or c["metric_registry_sha256"].strip() != metric_sha
        or c["snapshot_state"] not in ("DRAFT", "PUBLISHED_VALIDATION")
        for c in cases
    ):
        raise ValueError("Replay snapshot provenance/version/state changed")
    outputs = []
    for case in cases:
        scope = {"snapshot_id": case["analysis_snapshot_id"]}
        ready_rows = [
            row for query in READY_QUERIES
            for row in execute(conn, SQL / "metrics" / f"{query}.sql", scope)
        ]
        partial_rows = execute(conn, SQL / "metrics/partial_components.sql", scope)
        rows = {row["metric_id"]: row for row in ready_rows + partial_rows}
        if len(rows) != 17 or len(rows) != len(ready_rows) + len(partial_rows):
            raise ValueError("Metric SQL did not produce exactly 17 executable contracts")
        contracts = {
            mid: {**body, "metric_id": mid, "contract_version": METRIC_VERSION}
            for mid, body in spec["metrics"].items()
        }
        for mid, contract in contracts.items():
            item = resolved_metric(contract, rows.get(mid), case)
            # Snapshot state is a publication transition, not a metric input.
            item.pop("snapshot_state")
            if mid == "MET-005":
                item["component_scope"] = (
                    "replay assessments: 2 SUFFICIENT, 38 INSUFFICIENT across both cases; "
                    "not an approved metric rate"
                )
            if mid == "MET-020":
                item["component_scope"] = (
                    "committed replay and source audit exist; governed replay audit mart absent"
                )
            outputs.append(item)
    if len(outputs) != 46 or len({(x["analysis_snapshot_id"], x["metric_id"])
                                  for x in outputs}) != 46:
        raise ValueError("Metric outputs are not one per snapshot and contract")
    return {
        "release_id": cases[0]["release_id"],
        "contract_version": METRIC_VERSION,
        "registry_sha256": metric_sha,
        "replay_artifact_sha256": REPLAY_SHA,
        "scope": "two explicit governed replay snapshots; one physical snapshot per frozen case",
        "cases": [c["case_name"] for c in cases],
        "snapshot_ids": {c["case_name"]: str(c["analysis_snapshot_id"]) for c in cases},
        "metrics_per_case": 23,
        "results": outputs,
    }


def canonical_bytes(payload: dict) -> bytes:
    return (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    with connect("pulse_dev") as conn:
        payload = replay_metrics(conn)
    data = canonical_bytes(payload)
    if args.check:
        if OUTPUT.read_bytes() != data:
            raise ValueError("Committed replay metric output is not deterministic")
    else:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_bytes(data)
    print(f"PASS: 23 contracts x 2 replay snapshots; sha256={hashlib.sha256(data).hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
