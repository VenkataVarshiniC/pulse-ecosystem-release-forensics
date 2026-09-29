"""Export or verify the deterministic PULSE application OpenAPI contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from pulse.api.app import app

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data/validation/m5-2-openapi.json"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Compare with the committed export")
    args = parser.parse_args()
    generated = json.dumps(app.openapi(), indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != generated:
            raise SystemExit("OpenAPI export differs; regenerate it")
        print("OpenAPI export matches the application contract")
    else:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(generated, encoding="utf-8")
        print(f"Wrote {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
