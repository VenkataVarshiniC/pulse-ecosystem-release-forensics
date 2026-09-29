"""Load the pinned replay into new DRAFT snapshots; never rewrite legacy data."""

from __future__ import annotations

import argparse
import json
import subprocess

from pulse.phase4_replay_db import load_replay


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-commit", required=True)
    args = parser.parse_args()
    source_commit = args.source_commit
    if len(source_commit) != 40 or any(c not in "0123456789abcdef" for c in source_commit):
        raise ValueError("Source commit must be a full lowercase SHA-1")
    subprocess.run(["git", "cat-file", "-e", f"{source_commit}^{{commit}}"], check=True)
    snapshots = load_replay(source_commit=source_commit)
    print(json.dumps(snapshots, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
