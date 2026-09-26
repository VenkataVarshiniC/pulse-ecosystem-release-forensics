"""Machine-readable collection-run outcomes."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, computed_field, model_validator

from pulse.collection.planner import CollectionTask, TaskKind, TaskRequirement


class TaskOutcomeStatus(StrEnum):
    SUCCEEDED = "succeeded"
    PARTIAL = "partial"
    RATE_LIMITED = "rate_limited"
    NOT_FOUND = "not_found"
    UNAUTHORIZED = "unauthorized"
    FAILED = "failed"


class TaskOutcome(BaseModel):
    model_config = ConfigDict(frozen=True)

    task_id: str
    status: TaskOutcomeStatus
    started_at: datetime
    completed_at: datetime
    record_count: int = Field(ge=0)
    snapshot_path: str | None = None
    error: str | None = None


class CollectionManifest(BaseModel):
    model_config = ConfigDict(frozen=True)

    run_id: str
    case_id: str
    started_at: datetime
    completed_at: datetime
    observation_window_start: str
    observation_window_end: str
    outcomes: tuple[TaskOutcome, ...]

    @computed_field
    @property
    def status(self) -> str:
        return self._operational_status()

    def _operational_status(self) -> str:
        """Legacy Phase 1 status calculation for historical replay."""
        failures = self.failures
        if failures == 0:
            return "complete"
        if failures == len(self.outcomes) and not any(
            item.status is TaskOutcomeStatus.PARTIAL for item in self.outcomes
        ):
            return "failed"
        return "incomplete"

    @computed_field
    @property
    def successes(self) -> int:
        return sum(item.status is TaskOutcomeStatus.SUCCEEDED for item in self.outcomes)

    @computed_field
    @property
    def failures(self) -> int:
        return sum(item.status is not TaskOutcomeStatus.SUCCEEDED for item in self.outcomes)


class FileProbeAvailability(StrEnum):
    AVAILABLE = "available"
    NONE_FOUND = "none_found"
    INCOMPLETE = "incomplete"
    NOT_PROBED = "not_probed"


class LiveCollectionManifest(CollectionManifest):
    """Operational completion and current-path availability for live runs."""

    planned_tasks: tuple[CollectionTask, ...]

    @model_validator(mode="after")
    def every_planned_task_has_one_outcome(self) -> LiveCollectionManifest:
        planned_ids = [task.task_id for task in self.planned_tasks]
        outcome_ids = [outcome.task_id for outcome in self.outcomes]
        if (
            len(set(planned_ids)) != len(planned_ids)
            or len(set(outcome_ids)) != len(outcome_ids)
            or set(planned_ids) != set(outcome_ids)
        ):
            raise ValueError("Live manifest requires one outcome per planned task")
        return self

    def _operational_status(self) -> str:
        requirements = {task.task_id: task.requirement for task in self.planned_tasks}
        required = [
            outcome for outcome in self.outcomes
            if requirements[outcome.task_id] is TaskRequirement.REQUIRED
        ]
        blockers = [
            outcome for outcome in self.outcomes
            if outcome.status is not TaskOutcomeStatus.SUCCEEDED
            and not (
                requirements[outcome.task_id] is TaskRequirement.OPTIONAL_PROBE
                and outcome.status is TaskOutcomeStatus.NOT_FOUND
            )
        ]
        if not blockers:
            return "complete"
        if required and all(
            item.status not in {TaskOutcomeStatus.SUCCEEDED, TaskOutcomeStatus.PARTIAL}
            for item in required
        ):
            return "failed"
        return "incomplete"

    @computed_field
    @property
    def outcome_breakdown(self) -> dict[str, int]:
        counts = {status.value: 0 for status in TaskOutcomeStatus}
        requirements = {task.task_id: task.requirement for task in self.planned_tasks}
        optional_not_found = 0
        required_failures = 0
        for outcome in self.outcomes:
            counts[outcome.status.value] += 1
            if (
                requirements[outcome.task_id] is TaskRequirement.OPTIONAL_PROBE
                and outcome.status is TaskOutcomeStatus.NOT_FOUND
            ):
                optional_not_found += 1
            if (
                requirements[outcome.task_id] is TaskRequirement.REQUIRED
                and outcome.status is not TaskOutcomeStatus.SUCCEEDED
            ):
                required_failures += 1
        return {
            **counts,
            "optional_not_found": optional_not_found,
            "required_failures": required_failures,
        }

    @computed_field
    @property
    def file_probe_availability(self) -> FileProbeAvailability:
        file_ids = {
            task.task_id for task in self.planned_tasks if task.kind is TaskKind.GITHUB_FILE
        }
        if not file_ids:
            return FileProbeAvailability.NOT_PROBED
        statuses = {
            outcome.status for outcome in self.outcomes if outcome.task_id in file_ids
        }
        if statuses - {TaskOutcomeStatus.SUCCEEDED, TaskOutcomeStatus.NOT_FOUND}:
            return FileProbeAvailability.INCOMPLETE
        if TaskOutcomeStatus.SUCCEEDED in statuses:
            return FileProbeAvailability.AVAILABLE
        return FileProbeAvailability.NONE_FOUND

    @computed_field
    @property
    def dependency_analysis_sufficiency(self) -> str:
        return "not_assessed"


def write_manifest(manifest: CollectionManifest, root: Path) -> Path:
    path = root / manifest.case_id / "collection-manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(manifest.model_dump_json(indent=2), encoding="utf-8")
    return path
