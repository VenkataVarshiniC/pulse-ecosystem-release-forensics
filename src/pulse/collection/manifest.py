"""Machine-readable collection-run outcomes."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, computed_field


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


def write_manifest(manifest: CollectionManifest, root: Path) -> Path:
    path = root / manifest.case_id / "collection-manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(manifest.model_dump_json(indent=2), encoding="utf-8")
    return path
