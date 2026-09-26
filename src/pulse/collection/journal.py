"""Immutable run/task checkpoints and verified whole-task resume."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict

from pulse.collection.manifest import CollectionManifest, TaskOutcome, TaskOutcomeStatus
from pulse.collection.planner import CollectionPlan, CollectionTask, TaskKind, TaskRequirement
from pulse.collection.raw import CaptureMethod, RawSnapshot
from pulse.collection.telemetry import CollectionStats
from pulse.models.case import CaseDefinition


def case_fingerprint(definition: CaseDefinition) -> str:
    return hashlib.sha256(definition.model_dump_json().encode()).hexdigest()


class AttemptRecord(BaseModel):
    model_config = ConfigDict(frozen=True)

    run_id: str
    attempt_id: str
    case_fingerprint: str
    task: CollectionTask
    capture_method: CaptureMethod | None = None
    observation_window_start: str
    observation_window_end: str
    outcome: TaskOutcome
    stats: CollectionStats
    matching_records: int
    failure_kind: str | None = None
    snapshot_sha256: str | None = None
    reused_from_attempt: str | None = None


class RunJournal:
    def __init__(self, root: Path) -> None:
        self.root = root

    def directory(self, case_id: str, run_id: str) -> Path:
        return self.root / case_id / "runs" / run_id

    def begin(
        self, run_id: str, definition: CaseDefinition, plan: CollectionPlan, started_at: str,
    ) -> None:
        path = self.directory(definition.case.case_id, run_id)
        path.mkdir(parents=True, exist_ok=False)
        _write(path / "run.json", {
            "run_id": run_id, "started_at": started_at,
            "case_fingerprint": case_fingerprint(definition),
            "definition": definition.model_dump(mode="json"),
            "plan": plan.model_dump(mode="json"),
        })

    def record(self, record: AttemptRecord) -> None:
        path = self.directory(record.task.case_id, record.run_id)
        with (path / f"{record.attempt_id}.attempt.json").open("x", encoding="utf-8") as handle:
            handle.write(record.model_dump_json(indent=2))

    def finish(self, manifest: CollectionManifest) -> Path:
        path = self.directory(manifest.case_id, manifest.run_id) / "manifest.json"
        with path.open("x", encoding="utf-8") as handle:
            handle.write(manifest.model_dump_json(indent=2))
        return path

    def successful(self, definition: CaseDefinition) -> dict[str, AttemptRecord]:
        """Return verified successful snapshots for callers needing payloads."""
        return {
            task_id: record for task_id, record in self.reusable(definition).items()
            if record.outcome.status is TaskOutcomeStatus.SUCCEEDED
        }

    def reusable(self, definition: CaseDefinition) -> dict[str, AttemptRecord]:
        """Reuse verified snapshots or terminal optional current-path 404 probes."""
        fingerprint = case_fingerprint(definition)
        records = []
        for path in sorted((self.root / definition.case.case_id / "runs").glob("*/*.attempt.json")):
            # Corrupt journals fail visibly; never silently infer success.
            record = AttemptRecord.model_validate_json(path.read_text(encoding="utf-8"))
            if record.case_fingerprint != fingerprint or record.reused_from_attempt:
                continue
            run_path = path.parent / "run.json"
            if not run_path.is_file():
                continue
            run = json.loads(run_path.read_text(encoding="utf-8"))
            plan = CollectionPlan.model_validate(run["plan"])
            if (
                run["run_id"] != record.run_id
                or run["case_fingerprint"] != fingerprint
                or record.task not in plan.tasks
                or record.outcome.task_id != record.task.task_id
            ):
                continue
            if not (_verified_snapshot(record, definition) or _verified_optional_not_found(record)):
                continue
            records.append(record)
        records.sort(key=lambda item: (item.outcome.completed_at, item.attempt_id))
        return {item.task.task_id: item for item in records}


def _verified_snapshot(record: AttemptRecord, definition: CaseDefinition) -> bool:
    if record.outcome.status is not TaskOutcomeStatus.SUCCEEDED:
        return False
    if not record.outcome.snapshot_path:
        return False
    snapshot_path = Path(record.outcome.snapshot_path)
    if not snapshot_path.is_file():
        return False
    raw = snapshot_path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != record.snapshot_sha256:
        return False
    snapshot = RawSnapshot.model_validate_json(raw)
    return (
        snapshot.capture_method is CaptureMethod.COLLECTOR
        and snapshot.task_id == record.task.task_id
        and snapshot.case_id == definition.case.case_id
        and snapshot.attempt_id == record.attempt_id
        and snapshot.run_id == record.run_id
        and snapshot.query == {"kind": record.task.kind.value, **record.task.parameters}
    )


def _verified_optional_not_found(record: AttemptRecord) -> bool:
    return (
        record.capture_method is CaptureMethod.COLLECTOR
        and record.task.requirement is TaskRequirement.OPTIONAL_PROBE
        and record.task.kind is TaskKind.GITHUB_FILE
        and record.outcome.status is TaskOutcomeStatus.NOT_FOUND
        and record.failure_kind == "not_found"
        and record.outcome.snapshot_path is None
        and record.snapshot_sha256 is None
        and record.outcome.record_count == 0
        and record.matching_records == 0
        and record.stats.pages_requested == 1
        and record.stats.pages_completed == 0
        and record.stats.retry_count == 0
        and record.stats.termination == "not_found"
        and len(record.stats.requests) == 1
        and record.stats.requests[0].status_code == 404
    )


def _write(path: Path, payload: dict[str, Any]) -> None:
    with path.open("x", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, indent=2))
