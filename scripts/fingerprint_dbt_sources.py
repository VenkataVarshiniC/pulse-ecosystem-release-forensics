"""Compare all governed ingestion/core source rows before and after a dbt build."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from psycopg import sql

from pulse.phase2_postgres.loader import connect
from pulse.phase2_postgres.reconcile import COUNT_TABLES

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / ".local" / "m2-3-source-fingerprint.json"


def fingerprint() -> dict[str, str]:
    result = {}
    with connect("pulse_dev") as conn:
        for table in COUNT_TABLES:
            schema, name = table.split(".")
            query = sql.SQL("SELECT to_jsonb(t)::text FROM {}.{} t").format(
                sql.Identifier(schema), sql.Identifier(name)
            )
            rows = sorted(row[0] for row in conn.execute(query))
            digest = hashlib.sha256()
            for row in rows:
                digest.update(row.encode("utf-8"))
                digest.update(b"\n")
            result[table] = digest.hexdigest()
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("record", "compare"))
    mode = parser.parse_args().mode
    current = fingerprint()
    if mode == "record":
        STATE.parent.mkdir(parents=True, exist_ok=True)
        STATE.write_text(json.dumps(current, sort_keys=True, indent=2), encoding="utf-8")
        print(f"Recorded {len(current)} source-table fingerprints in ignored .local")
        return 0
    expected = json.loads(STATE.read_text(encoding="utf-8"))
    changed = [table for table in current if current[table] != expected.get(table)]
    if changed:
        print(f"FAIL: source tables changed: {', '.join(changed)}")
        return 1
    print(f"PASS: {len(current)} ingestion/core source tables unchanged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
