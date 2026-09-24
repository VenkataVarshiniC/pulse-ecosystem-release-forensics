"""Run collection tasks independently and preserve partial results."""

from __future__ import annotations

import hashlib
from collections.abc import Callable, Sequence
from datetime import UTC, datetime
from typing import Any, Protocol

from pulse.collection.manifest import CollectionManifest, TaskOutcome, TaskOutcomeStatus
from pulse.collection.planner import CollectionPlan, CollectionTask, TaskKind
from pulse.models.case import CaseDefinition


class Collector(Protocol):
    def supports(self, kind: TaskKind) -> bool: ...

    def collect(self, task: CollectionTask) -> Any: ...


class SnapshotStore(Protocol):
    def save(self, task: CollectionTask, payload: Any, retrieved_at: datetime) -> object: ...


def _record_count(payload: Any) -> int:
    return len(payload) if isinstance(payload, list) else 1


class CollectionRunner:
    def __init__(
        self,
        collectors: Sequence[Collector],
        raw_store: SnapshotStore,
        *,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        self.collectors = collectors
        self.raw_store = raw_store
        self.clock = clock or (lambda: datetime.now(UTC))

    def run(self, definition: CaseDefinition, plan: CollectionPlan) -> CollectionManifest:
        started_at = self.clock()
        outcomes = []
        for task in plan.tasks:
            task_started = self.clock()
            try:
                collector = next(item for item in self.collectors if item.supports(task.kind))
                payload = collector.collect(task)
                completed_at = self.clock()
                path = self.raw_store.save(task, payload, completed_at)
                outcomes.append(
                    TaskOutcome(
                        task_id=task.task_id,
                        status=TaskOutcomeStatus.SUCCEEDED,
                        started_at=task_started,
                        completed_at=completed_at,
                        record_count=_record_count(payload),
                        snapshot_path=str(path),
                    )
                )
            except Exception as exc:  # noqa: BLE001 - one failed source must not abort a run
                outcomes.append(
                    TaskOutcome(
                        task_id=task.task_id,
                        status=TaskOutcomeStatus.FAILED,
                        started_at=task_started,
                        completed_at=self.clock(),
                        record_count=0,
                        error=f"{type(exc).__name__}: {exc}",
                    )
                )
        completed_at = self.clock()
        run_key = f"{definition.case.case_id}:{started_at.isoformat()}"
        run_id = hashlib.sha256(run_key.encode()).hexdigest()[:20]
        return CollectionManifest(
            run_id=run_id,
            case_id=definition.case.case_id,
            started_at=started_at,
            completed_at=completed_at,
            observation_window_start=definition.case.observation_window_start.isoformat(),
            observation_window_end=definition.case.observation_window_end.isoformat(),
            outcomes=tuple(outcomes),
        )
