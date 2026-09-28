"""Run the bounded M2.2 frozen-evidence verification and load."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from pulse.phase2_postgres.lineage import lineage
from pulse.phase2_postgres.loader import connect, load_case
from pulse.phase2_postgres.manifest import ROOT, verify_inputs
from pulse.phase2_postgres.reconcile import reconcile


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="action", required=True)
    subparsers.add_parser("verify", help="Hash-check every frozen input before any DB write")
    loader = subparsers.add_parser("load", help="Load a case or both cases transactionally")
    group = loader.add_mutually_exclusive_group(required=True)
    group.add_argument("--case", choices=("pytest-8.0.0", "urllib3-2.0.0"))
    group.add_argument("--all", action="store_true")
    loader.add_argument("--database", choices=("pulse_dev", "pulse_test"), default="pulse_dev")
    check = subparsers.add_parser("reconcile", help="Compare database with golden values")
    check.add_argument("--database", choices=("pulse_dev", "pulse_test"), default="pulse_dev")
    trace = subparsers.add_parser("lineage", help="Verify sampled rows against frozen inputs")
    trace.add_argument("--database", choices=("pulse_dev", "pulse_test"), default="pulse_dev")
    args = parser.parse_args()

    if args.action in {"verify", "load"}:
        inputs = verify_inputs()
        print(f"Verified {len(inputs.files)} inputs: {inputs.manifest['manifest_sha256']}")
        if args.action == "verify":
            return 0
        for case in sorted(inputs.manifest["cases"]) if args.all else (args.case,):
            print(f"{case}: {load_case(inputs, case, args.database)}")
        return 0
    inputs = verify_inputs() if args.action == "lineage" else None
    with connect(args.database) as conn:
        result = lineage(conn, inputs) if inputs is not None else reconcile(conn)
    if args.database == "pulse_dev":
        name = ("m2-2-lineage.json" if args.action == "lineage"
                else "m2-2-golden-reconciliation.json")
        path = Path(ROOT / "data/validation" / name)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"{result['status']}: {args.action} checks")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
