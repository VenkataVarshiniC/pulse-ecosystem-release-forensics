"""Run tasks independently, checkpoint results, and resume verified successes."""

from __future__ import annotations

import hashlib
from collections.abc import Callable, Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Protocol
from uuid import uuid4

from pulse.collection.journal import AttemptRecord, RunJournal, case_fingerprint
from pulse.collection.manifest import LiveCollectionManifest, TaskOutcome, TaskOutcomeStatus
from pulse.collection.planner import CollectionPlan, CollectionTask, TaskKind
from pulse.collection.raw import RawSnapshotStore
from pulse.collection.result import CollectionResult
from pulse.collection.telemetry import CollectionStats
from pulse.github.errors import GitHubApiError
from pulse.models.case import CaseDefinition


class Collector(Protocol):
    def supports(self, kind: TaskKind) -> bool: ...

    def collect(self, task: CollectionTask) -> Any: ...


class SnapshotStore(Protocol):
    def save(self, task: CollectionTask, payload: Any, retrieved_at: datetime) -> object: ...


def _record_count(payload: Any) -> int:
    if payload is None:
        return 0
    return len(payload) if isinstance(payload, list) else 1


class CollectionRunner:
    def __init__(
        self, collectors: Sequence[Collector], raw_store: SnapshotStore, *,
        clock: Callable[[], datetime] | None = None,
        journal: RunJournal | None = None,
    ) -> None:
        self.collectors = collectors
        self.raw_store = raw_store
        self.clock = clock or (lambda: datetime.now(UTC))
        self.journal = journal

    def run(
        self, definition: CaseDefinition, plan: CollectionPlan, *, resume: bool = False,
    ) -> LiveCollectionManifest:
        if plan.case_id != definition.case.case_id:
            raise ValueError("Plan and case must match")
        if resume and self.journal is None:
            raise ValueError("Resume requires a run journal")
        previous = self.journal.reusable(definition) if resume and self.journal else {}
        started_at = self.clock()
        run_id = uuid4().hex
        if self.journal:
            self.journal.begin(run_id, definition, plan, started_at.isoformat())
        outcomes = []
        for task in plan.tasks:
            attempt_id = uuid4().hex
            task_started = self.clock()
            prior = previous.get(task.task_id)
            if prior and prior.task == task:
                outcome = TaskOutcome(
                    task_id=task.task_id, status=prior.outcome.status,
                    started_at=task_started, completed_at=self.clock(),
                    record_count=prior.outcome.record_count,
                    snapshot_path=prior.outcome.snapshot_path,
                    error=prior.outcome.error,
                )
                result = CollectionResult(
                    status=prior.outcome.status, failure_kind=prior.failure_kind,
                    stats=CollectionStats(termination="reused"),
                )
                snapshot_hash = prior.snapshot_sha256
            else:
                prior = None
                outcome, result, snapshot_hash = self._attempt(
                    task, task_started, run_id, attempt_id
                )
            outcomes.append(outcome)
            if self.journal:
                self.journal.record(AttemptRecord(
                    run_id=run_id, attempt_id=attempt_id,
                    case_fingerprint=case_fingerprint(definition), task=task,
                    capture_method=(
                        self.raw_store.capture_method
                        if isinstance(self.raw_store, RawSnapshotStore) else None
                    ),
                    observation_window_start=definition.case.observation_window_start.isoformat(),
                    observation_window_end=definition.case.observation_window_end.isoformat(),
                    outcome=outcome, stats=result.stats,
                    matching_records=(
                        prior.matching_records if prior else _record_count(result.payload)
                    ),
                    failure_kind=result.failure_kind,
                    snapshot_sha256=snapshot_hash,
                    reused_from_attempt=prior.attempt_id if prior else None,
                ))
        manifest = LiveCollectionManifest(
            run_id=run_id, case_id=definition.case.case_id,
            started_at=started_at, completed_at=self.clock(),
            observation_window_start=definition.case.observation_window_start.isoformat(),
            observation_window_end=definition.case.observation_window_end.isoformat(),
            outcomes=tuple(outcomes),
            planned_tasks=plan.tasks,
        )
        if self.journal:
            self.journal.finish(manifest)
        return manifest

    def _attempt(
        self, task: CollectionTask, started: datetime, run_id: str, attempt_id: str,
    ) -> tuple[TaskOutcome, CollectionResult, str | None]:
        result = CollectionResult()
        snapshot_path = None
        snapshot_hash = None
        try:
            collector = next(item for item in self.collectors if item.supports(task.kind))
            value = collector.collect(task)
            if isinstance(value, CollectionResult):
                result = value
            else:
                result = CollectionResult(
                    payload=value,
                    stats=CollectionStats(records_examined=_record_count(value)),
                )
            if result.status is TaskOutcomeStatus.SUCCEEDED or result.stats.pages_completed:
                if isinstance(self.raw_store, RawSnapshotStore):
                    path = self.raw_store.save(
                        task, result.payload, self.clock(), run_id=run_id,
                        attempt_id=attempt_id, stats=result.stats,
                    )
                else:
                    path = self.raw_store.save(task, result.payload, self.clock())
                snapshot_path = str(path)
                if self.journal:
                    snapshot_path = str(Path(snapshot_path).resolve())
                    snapshot_hash = hashlib.sha256(Path(snapshot_path).read_bytes()).hexdigest()
        except GitHubApiError as exc:
            result.status = TaskOutcomeStatus(exc.failure_kind)
            result.failure_kind = exc.failure_kind
            result.error = exc.message
        except Exception as exc:  # a single task must not abort the other repositories
            result.status = TaskOutcomeStatus.FAILED
            result.failure_kind = "failed"
            # Do not persist arbitrary exception messages (may contain URLs or credentials).
            result.error = f"Collection task failed ({type(exc).__name__})"
        outcome = TaskOutcome(
            task_id=task.task_id, status=result.status,
            started_at=started, completed_at=self.clock(),
            record_count=_record_count(result.payload) if snapshot_path else 0,
            snapshot_path=snapshot_path, error=result.error,
        )
        return outcome, result, snapshot_hash
