"""Record the bounded M2.5 validation release without publishing DRAFT snapshots."""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from importlib.metadata import version
from pathlib import Path

from psycopg.rows import dict_row

from pulse.phase2_postgres.loader import connect

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "data/manifests/analytics-release-manifest.json"
SOURCE_COMMIT = "831121996a8fb674bee3a0bd4aeeb0e5dfb428b7"


def digest_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def model_digest() -> str:
    root = ROOT / "analytics/dbt"
    files = sorted([*root.glob("models/**/*.sql"), *root.glob("models/**/*.yml"),
                    *root.glob("macros/**/*.sql"), root / "dbt_project.yml"])
    sha = hashlib.sha256()
    for path in files:
        sha.update(path.relative_to(root).as_posix().encode())
        sha.update(b"\0")
        sha.update(path.read_bytes())
        sha.update(b"\0")
    return sha.hexdigest()


def main() -> int:
    with connect("pulse_dev") as conn, conn.cursor(row_factory=dict_row) as cur:
        cur.execute("""select s.analysis_snapshot_id, c.target_package as case_name,
                              s.state, s.manifest_sha256, s.rule_version,
                              s.metric_definition_version, s.model_version
                       from core.analysis_snapshot s
                       join analytics.dim_case c on s.case_version_id = c.case_key
                       order by c.target_package""")
        snapshots = [{k: str(v) for k, v in row.items()} for row in cur.fetchall()]
        cur.execute("show server_version_num")
        postgres_major = int(cur.fetchone()["server_version_num"]) // 10000
    assert len(snapshots) == 2
    assert all(s["state"] == "DRAFT" for s in snapshots)
    assert all(s["rule_version"] == "unrecorded_in_frozen_report" for s in snapshots)
    registry = ROOT / "analytics/metrics/metric_registry.yml"
    model_sha = model_digest()
    payload = {
        "manifest_schema": "m2-5-analytics-release-v1",
        "source_commit": SOURCE_COMMIT,
        "source_input_manifest_sha256": digest_file(
            ROOT / "data/manifests/phase2-postgres-load-manifest.json"
        ),
        "snapshots": snapshots,
        "rule_version": "UNRESOLVED: unrecorded_in_frozen_report; frozen rule identity untraceable",
        "metric_contract_version": "m2-5-metric-registry-v1",
        "metric_registry_sha256": digest_file(registry),
        "mart_model_version": f"m2-4-{SOURCE_COMMIT[:12]}-{model_sha[:12]}",
        "mart_model_sha256": model_sha,
        "dbt_version": version("dbt-core"),
        "postgresql_major_version": postgres_major,
        "metric_baseline_sha256": digest_file(
            ROOT / "data/validation/m2-5-metric-baseline.json"
        ),
        "sql_diagnostics_sha256": digest_file(
            ROOT / "data/validation/m2-5-sql-diagnostics.json"
        ),
        "publication_scope": (
            "bounded two-case frozen validation dataset; not representative ecosystem data"
        ),
        "publication_decision": "HOLD_DRAFT",
        "power_bi_gate": "BLOCKED_NO_PUBLISHED_SNAPSHOT",
        "known_limitations": [
            "Frozen Phase 2 case/finding and candidate-rule version is unrecorded.",
            "Snapshot metric/model version fields predate M2.5 governance.",
            "38 legacy sufficiency assessments and 38 UNKNOWN findings remain unresolved.",
            "No qualified observed adoption, recovery, or stakeholder-approved outcome metric.",
            "Two release cases and eight members support validation only, not ecosystem inference.",
        ],
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["analytical_release_id"] = "m2-5-" + hashlib.sha256(canonical).hexdigest()[:20]
    if DEST.exists():
        old = json.loads(DEST.read_text(encoding="utf-8"))
        payload["generated_at_utc"] = (
            old["generated_at_utc"] if old.get("analytical_release_id")
            == payload["analytical_release_id"] else datetime.now(UTC).isoformat()
        )
    else:
        payload["generated_at_utc"] = datetime.now(UTC).isoformat()
    DEST.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Validation manifest {payload['analytical_release_id']}; publication HOLD_DRAFT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
