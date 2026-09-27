"""Typed refs, bounded pairs, file states, and historical run results."""

from __future__ import annotations

from datetime import date, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, model_validator

from pulse.collection.raw import CaptureMethod
from pulse.collection.telemetry import CollectionStats
from pulse.dependencies.models import DependencyObservation, DependencyTransition
from pulse.models.evidence import Confidence


class AnchorRole(StrEnum):
    PRE_RELEASE = "pre_release"
    FIRST_CHANGE_AFTER_RELEASE = "first_manifest_change_after_release"


class PairStatus(StrEnum):
    PAIRED = "paired"
    MISSING_BEFORE = "missing_before"
    MISSING_AFTER = "missing_after"
    INSUFFICIENT_HISTORY = "insufficient_history"
    FILE_UNAVAILABLE = "file_unavailable"
    MALFORMED = "malformed"
    AMBIGUOUS = "ambiguous"
    COLLECTION_FAILED = "collection_failed"


class ChangeStatus(StrEnum):
    UNKNOWN = "unknown"
    UNCHANGED = "unchanged"
    INTRODUCED = "introduced"
    REMOVED = "removed"
    CONSTRAINT_CHANGED = "constraint_changed"
    TARGET_EXCLUDED = "target_excluded"
    TARGET_ACCEPTED = "target_accepted"


class FileStateStatus(StrEnum):
    PARSED = "parsed"
    NOT_FOUND = "not_found"
    UNAVAILABLE = "unavailable"
    INVALID = "invalid"


class HistoricalRef(BaseModel):
    model_config = ConfigDict(frozen=True)

    repository: str
    path: str
    commit_sha: str = Field(pattern=r"^[0-9a-f]{40}([0-9a-f]{24})?$")
    commit_timestamp: datetime
    role: AnchorRole
    source: HttpUrl
    selection_strategy: str
    reason: str
    confidence: Confidence


class HistoricalRefPair(BaseModel):
    model_config = ConfigDict(frozen=True)

    case_id: str
    repository: str
    manifest_path: str
    before: HistoricalRef | None
    after: HistoricalRef | None
    pairing_strategy: str
    release_timestamp: datetime
    observation_window_start: date
    observation_window_end: date
    confidence: Confidence
    reason: str
    status: PairStatus

    @model_validator(mode="after")
    def paired_requires_both_refs(self) -> HistoricalRefPair:
        if self.status is PairStatus.PAIRED and (self.before is None or self.after is None):
            raise ValueError("A paired result requires both historical refs")
        return self


class HistoricalFileState(BaseModel):
    model_config = ConfigDict(frozen=True)

    repository: str
    path: str
    commit_sha: str
    commit_timestamp: datetime
    status: FileStateStatus
    api_url: HttpUrl
    source_url: HttpUrl
    retrieved_at: datetime
    capture_method: CaptureMethod
    content_sha256: str | None = None
    raw_snapshot_path: str | None = None
    target_observations: tuple[DependencyObservation, ...] = ()
    diagnostics: tuple[str, ...] = ()


class HistoricalPathResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    pair: HistoricalRefPair
    history_snapshot_path: str | None = None
    history_stats: CollectionStats
    before_state: HistoricalFileState | None = None
    after_state: HistoricalFileState | None = None
    transition: DependencyTransition | None = None
    change_status: ChangeStatus = ChangeStatus.UNKNOWN
    notes: tuple[str, ...] = ()


class HistoricalRun(BaseModel):
    model_config = ConfigDict(frozen=True)

    run_id: str
    case_id: str
    started_at: datetime
    completed_at: datetime
    results: tuple[HistoricalPathResult, ...]
