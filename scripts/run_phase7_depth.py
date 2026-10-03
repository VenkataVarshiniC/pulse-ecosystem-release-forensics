"""Collect or deterministically replay the frozen Phase 7 evidence-depth experiment."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from pulse.phase7_depth import (
    ROOT,
    collect_phase7,
    evaluate_phase7,
    verify_replay,
    write_evaluation,
)


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser()
    subparsers = result.add_subparsers(dest="command", required=True)
    collect = subparsers.add_parser("collect")
    collect.add_argument("--output-root", type=Path, default=ROOT)
    replay = subparsers.add_parser("replay")
    replay.add_argument("manifest", type=Path)
    replay.add_argument("--output-root", type=Path, default=ROOT)
    replay.add_argument("--expected", type=Path)
    return result


def main() -> int:
    args = parser().parse_args()
    if args.command == "collect":
        manifest = collect_phase7(
            args.output_root,
            token=os.getenv("GITHUB_TOKEN") or None,
        )
        evaluation = evaluate_phase7(manifest, root=args.output_root)
        output = write_evaluation(evaluation, root=args.output_root)
        print(manifest)
        print(output)
        return 0
    if args.expected:
        verify_replay(args.manifest, args.expected, root=args.output_root)
        print("Phase 7 offline replay matches expected evaluation.")
        return 0
    evaluation = evaluate_phase7(args.manifest, root=args.output_root)
    output = write_evaluation(evaluation, root=args.output_root)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
