"""Materialize or verify the deterministic, offline M4.1 replay artifact."""

from __future__ import annotations

import argparse
import json

from pulse.phase2_postgres.manifest import ROOT, sha256
from pulse.phase4_replay import replay

OUTPUT = ROOT / "data/processed/m4-1/replay.json"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload = (json.dumps(replay(), indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode()
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_bytes() != payload:
            print("FAIL: M4.1 replay differs from committed output")
            return 1
    else:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        if OUTPUT.exists() and OUTPUT.read_bytes() != payload:
            raise SystemExit("Existing replay artifact differs; inspect before overwrite")
        OUTPUT.write_bytes(payload)
    print(f"PASS: offline replay {sha256(OUTPUT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
