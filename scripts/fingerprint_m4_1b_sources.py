"""Prove every pre-replay source row survives byte-identically after additive load."""

from __future__ import annotations

import argparse
import hashlib
import json

from psycopg import sql

from pulse.phase2_postgres.loader import connect
from pulse.phase2_postgres.manifest import ROOT
from pulse.phase2_postgres.reconcile import COUNT_TABLES

STATE = ROOT / ".local/m4-1b-source-rows.json"
ADDITIVE = {
    "ingestion.load_audit",
    "core.candidate", "core.analyst_review", "core.sufficiency_assessment",
    "core.lifecycle_finding", "core.analysis_snapshot", "core.snapshot_run",
    "core.snapshot_artifact", "core.snapshot_candidate", "core.snapshot_review",
    "core.snapshot_assessment", "core.snapshot_finding",
}


def fingerprints() -> dict[str, list[str]]:
    result = {}
    with connect() as conn:
        for table in COUNT_TABLES:
            schema, name = table.split(".")
            # V005 adds governance columns to existing tables without changing
            # original row values. Remove them for a pre/post migration comparison.
            projection = "to_jsonb(t)"
            if table == "core.analysis_snapshot":
                projection += (
                    " - 'publication_manifest_sha256'"
                    " - 'publication_fingerprint' - 'published_at'"
                )
            elif table == "core.analyst_review":
                projection += " - 'review_origin' - 'inherited_from_review_id'"
            query = sql.SQL("SELECT (" + projection + ")::text FROM {}.{} t").format(
                sql.Identifier(schema), sql.Identifier(name)
            )
            result[table] = sorted(
                hashlib.sha256(row[0].encode()).hexdigest()
                for row in conn.execute(query)
            )
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("record", "compare"))
    args = parser.parse_args()
    current = fingerprints()
    if args.mode == "record":
        if STATE.exists():
            raise SystemExit("M4.1B pre-load fingerprint already exists; do not overwrite")
        STATE.parent.mkdir(parents=True, exist_ok=True)
        STATE.write_text(json.dumps(current, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"Recorded original rows in {len(current)} ingestion/core tables")
        return 0
    before = json.loads(STATE.read_text(encoding="utf-8"))
    if before.keys() != current.keys():
        raise ValueError("Source table inventory changed")
    for table, prior in before.items():
        old = set(prior)
        new = set(current[table])
        if not old.issubset(new):
            raise ValueError(f"Original source rows changed or disappeared: {table}")
        if table not in ADDITIVE and old != new:
            raise ValueError(f"Original evidence table received unexpected new rows: {table}")
    print(f"PASS: all original rows preserved; non-derived source tables unchanged ({len(before)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
