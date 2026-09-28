"""Compare all dbt model rows across repeated builds."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from psycopg import sql
from reconcile_dbt import MODELS
from reconcile_marts import MARTS

from pulse.phase2_postgres.loader import connect

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / ".local" / "m2-3-model-fingerprint.json"


def fingerprint() -> dict[str, str]:
    result = {}
    with connect("pulse_dev") as conn:
        models = MODELS | {model: "analytics" for model in MARTS}
        for model, schema in sorted(models.items()):
            query = sql.SQL("SELECT to_jsonb(t)::text FROM {}.{} t").format(
                sql.Identifier(schema), sql.Identifier(model)
            )
            rows = sorted(row[0] for row in conn.execute(query))
            digest = hashlib.sha256()
            for row in rows:
                digest.update(row.encode("utf-8"))
                digest.update(b"\n")
            result[model] = digest.hexdigest()
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("record", "compare"))
    mode = parser.parse_args().mode
    current = fingerprint()
    if mode == "record":
        STATE.parent.mkdir(parents=True, exist_ok=True)
        STATE.write_text(json.dumps(current, sort_keys=True, indent=2), encoding="utf-8")
        print(f"Recorded {len(current)} dbt model fingerprints in ignored .local")
        return 0
    expected = json.loads(STATE.read_text(encoding="utf-8"))
    changed = [model for model in current if current[model] != expected.get(model)]
    if changed:
        print(f"FAIL: dbt model rows changed: {', '.join(changed)}")
        return 1
    print(f"PASS: {len(current)} dbt model row sets are byte-identical")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
