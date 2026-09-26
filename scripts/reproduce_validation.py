"""Reproduce the HTTPX Phase 1 validation artifacts from preserved raw snapshots."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from pulse.analysis.forensics import build_forensics
from pulse.collection.manifest import (
    CollectionManifest,
    TaskOutcome,
    TaskOutcomeStatus,
    write_manifest,
)
from pulse.collection.planner import plan_collection
from pulse.config.cases import load_case
from pulse.evidence.review_ledger import write_review_ledger
from pulse.pipeline import apply_review_decisions, detect_raw_candidates, load_review_decisions
from pulse.reporting import write_forensics_json, write_forensics_markdown


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    case_path = root / "cases" / "httpx-0.28.0.yaml"
    definition = load_case(case_path)
    raw_root = root / "data" / "raw" / definition.case.case_id
    interim_root = root / "data" / "interim" / definition.case.case_id
    processed_root = root / "data" / "processed" / definition.case.case_id
    generated_report = root / "docs" / "generated" / "httpx-0.28.0-forensics.md"

    candidates = detect_raw_candidates(definition, raw_root)
    reviewed = apply_review_decisions(
        candidates, load_review_decisions(interim_root / "review-decisions.json")
    )
    write_review_ledger(interim_root / "review-ledger.jsonl", reviewed)

    snapshot_task_ids = {
        path.stem.split("-")[0] for path in raw_root.rglob("*.json")
    }
    planned = plan_collection(definition)
    started = datetime(2026, 9, 24, 14, 0, tzinfo=UTC)
    completed = datetime(2026, 9, 24, 14, 5, tzinfo=UTC)
    outcomes = []
    for task in planned.tasks:
        if task.task_id in snapshot_task_ids:
            outcomes.append(
                TaskOutcome(
                    task_id=task.task_id,
                    status=TaskOutcomeStatus.SUCCEEDED,
                    started_at=started,
                    completed_at=completed,
                    record_count=1,
                    snapshot_path=next(raw_root.rglob(f"{task.task_id}-*.json"))
                    .relative_to(root)
                    .as_posix(),
                )
            )
        else:
            outcomes.append(
                TaskOutcome(
                    task_id=task.task_id,
                    status=TaskOutcomeStatus.FAILED,
                    started_at=started,
                    completed_at=completed,
                    record_count=0,
                    error="Not collected in the connector-assisted validation run.",
                )
            )
    write_manifest(
        CollectionManifest(
            run_id="httpx-0.28.0-validation-20260924",
            case_id=definition.case.case_id,
            started_at=started,
            completed_at=completed,
            observation_window_start=definition.case.observation_window_start.isoformat(),
            observation_window_end=definition.case.observation_window_end.isoformat(),
            outcomes=tuple(outcomes),
        ),
        root / "data" / "interim",
    )

    forensics = build_forensics(
        definition,
        reviewed,
        repositories_with_sufficient_collection=set(),
        recovery_eligible_repositories=None,
    )
    write_forensics_json(forensics, processed_root / "forensics.json")
    write_forensics_markdown(forensics, generated_report)


if __name__ == "__main__":
    main()
