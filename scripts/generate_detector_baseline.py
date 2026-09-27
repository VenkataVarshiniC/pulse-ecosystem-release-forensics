"""Freeze unchanged PULSE detector output from one live collection run."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

from pulse.collection.manifest import LiveCollectionManifest, TaskOutcomeStatus
from pulse.collection.raw import CaptureMethod, RawSnapshot
from pulse.config.cases import load_case
from pulse.evidence.detectors import detect_transition_candidate
from pulse.history.models import HistoricalRun, PairStatus
from pulse.models.review import ReviewableEvidence
from pulse.pipeline import detect_raw_candidates


def generate(
    case_path: Path, collection_path: Path, history_path: Path, output_dir: Path,
) -> tuple[Path, Path]:
    definition = load_case(case_path)
    collection = LiveCollectionManifest.model_validate_json(
        collection_path.read_text(encoding="utf-8")
    )
    history = HistoricalRun.model_validate_json(history_path.read_text(encoding="utf-8"))
    if collection.case_id != definition.case.case_id or history.case_id != collection.case_id:
        raise ValueError("Case, collection, and history manifests must match")
    snapshots = [
        Path(item.snapshot_path) for item in collection.outcomes
        if item.status in {TaskOutcomeStatus.SUCCEEDED, TaskOutcomeStatus.PARTIAL}
        and item.snapshot_path
    ]
    raw_root = collection_path.parents[4] / "raw" / collection.case_id
    for path in snapshots:
        snapshot = RawSnapshot.model_validate_json(path.read_text(encoding="utf-8"))
        if (
            snapshot.capture_method is not CaptureMethod.COLLECTOR
            or snapshot.run_id != collection.run_id
        ):
            raise ValueError("Baseline requires collector snapshots from the selected run")
        if not path.is_relative_to(raw_root):
            raise ValueError("Snapshot is outside the selected case raw root")
    if set(raw_root.rglob("*.json")) != set(snapshots):
        raise ValueError("The raw case root contains snapshots outside this collection run")
    candidates: dict[str, ReviewableEvidence] = {
        item.candidate_id: item for item in detect_raw_candidates(definition, raw_root)
    }
    for result in history.results:
        if result.pair.status is not PairStatus.PAIRED or result.transition is None:
            continue
        candidate = detect_transition_candidate(definition.case, result.transition)
        if candidate is not None:
            prior = candidates.get(candidate.candidate_id)
            if prior is not None and prior != candidate:
                raise ValueError("Candidate identity collision")
            candidates[candidate.candidate_id] = candidate
    values = sorted(candidates.values(), key=lambda item: item.candidate_id)
    output_dir.mkdir(parents=True, exist_ok=True)
    baseline = output_dir / f"baseline-{collection.case_id}.jsonl"
    with baseline.open("x", encoding="utf-8") as handle:
        for item in values:
            handle.write(item.model_dump_json() + "\n")
    digest = hashlib.sha256(baseline.read_bytes()).hexdigest()
    manifest = output_dir / f"baseline-{collection.case_id}.manifest.json"
    with manifest.open("x", encoding="utf-8") as handle:
        json.dump({
            "case_id": collection.case_id,
            "generated_at": datetime.now(UTC).isoformat(),
            "collection_manifest": str(collection_path),
            "history_manifest": str(history_path),
            "collection_run_id": collection.run_id,
            "history_run_id": history.run_id,
            "candidate_count": len(values),
            "candidate_ids": [item.candidate_id for item in values],
            "baseline_sha256": digest,
            "detector_rules_unchanged_from_commit": "da343d5",
        }, handle, indent=2)
        handle.write("\n")
    return baseline, manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("case", type=Path)
    parser.add_argument("collection_manifest", type=Path)
    parser.add_argument("history_manifest", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    baseline, manifest = generate(
        args.case, args.collection_manifest, args.history_manifest, args.output_dir
    )
    print(baseline)
    print(manifest)


if __name__ == "__main__":
    main()
