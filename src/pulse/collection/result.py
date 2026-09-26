"""Collector result separates preserved payload from completion status."""

from dataclasses import dataclass, field
from typing import Any

from pulse.collection.manifest import TaskOutcomeStatus
from pulse.collection.telemetry import CollectionStats


@dataclass
class CollectionResult:
    payload: Any = None
    status: TaskOutcomeStatus = TaskOutcomeStatus.SUCCEEDED
    stats: CollectionStats = field(default_factory=CollectionStats)
    failure_kind: str | None = None
    error: str | None = None
