"""Run the pinned dbt CLI with credentials from the ignored local .env."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

from dotenv import dotenv_values

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "analytics" / "dbt"


def main() -> int:
    if len(sys.argv) < 2:
        raise SystemExit("usage: python scripts/run_dbt.py <dbt command and options>")
    values = dotenv_values(ROOT / ".env")
    env = os.environ.copy()
    for key in ("PGHOST", "PGPORT", "PGUSER", "PGPASSWORD"):
        if key not in env and values.get(key):
            env[key] = str(values[key])
        if not env.get(key):
            raise SystemExit(f"Missing local database setting {key}")
    if (env["PGHOST"], env["PGPORT"], env["PGUSER"]) != (
        "127.0.0.1", "55432", "pulse_local"
    ):
        raise SystemExit("dbt may target only the isolated local PULSE cluster")
    executable = shutil.which("dbt")
    if executable is None:
        raise SystemExit("dbt is not installed; run python -m uv sync --locked --all-groups")
    return subprocess.run(
        [executable, *sys.argv[1:], "--project-dir", str(PROJECT),
         "--profiles-dir", str(PROJECT)],
        cwd=ROOT, env=env, check=False,
    ).returncode


if __name__ == "__main__":
    raise SystemExit(main())
