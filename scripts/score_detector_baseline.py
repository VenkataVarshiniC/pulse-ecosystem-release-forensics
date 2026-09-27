"""Validate analyst decisions and score the immutable first-pass candidates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from pulse.config.cases import load_case
from pulse.detector_evaluation import (
    AnalystDecision,
    aggregate,
    apply_analyst_decisions,
    load_verified_baseline,
)
from pulse.history.models import HistoricalRun

CASE_IDS = ("pytest-8.0.0", "urllib3-2.0.0")


def score(data_dir: Path) -> tuple[Path, Path]:
    definitions = tuple(load_case(Path("cases") / f"{case_id}.yaml") for case_id in CASE_IDS)
    candidates = []
    histories = {}
    collections = {}
    for case_id in CASE_IDS:
        manifest_path = data_dir / f"baseline-{case_id}.manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        candidates.extend(load_verified_baseline(
            data_dir / f"baseline-{case_id}.jsonl", manifest_path
        ))
        histories[case_id] = HistoricalRun.model_validate_json(
            Path(manifest["history_manifest"]).read_text(encoding="utf-8")
        )
        collections[case_id] = Path(manifest["collection_manifest"])
    decisions = tuple(
        AnalystDecision.model_validate(item)
        for item in json.loads((data_dir / "review-decisions.json").read_text(encoding="utf-8"))
    )
    reviewed = apply_analyst_decisions(tuple(candidates), decisions)
    metrics = aggregate(definitions, reviewed, histories, collections)
    ledger_path = data_dir / "review-ledger.jsonl"
    with ledger_path.open("x", encoding="utf-8") as handle:
        for item in reviewed:
            handle.write(item.model_dump_json() + "\n")
    metric_path = data_dir / "metrics.json"
    with metric_path.open("x", encoding="utf-8") as handle:
        json.dump(metrics, handle, indent=2)
        handle.write("\n")
    return ledger_path, metric_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=Path("docs/phase-2/evaluation-data"))
    args = parser.parse_args()
    ledger, metrics = score(args.data_dir)
    print(ledger)
    print(metrics)


if __name__ == "__main__":
    main()
