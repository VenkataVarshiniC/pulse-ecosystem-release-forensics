"""Normalized evidence records that retain provenance and uncertainty."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, model_validator


class Confidence(StrEnum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class DownstreamEventType(StrEnum):
    DEPENDENCY_UPGRADE = "dependency_upgrade"
    DEPENDENCY_DOWNGRADE = "dependency_downgrade"
    VERSION_PIN = "version_pin"
    MIGRATION_ISSUE = "migration_issue"
    COMPATIBILITY_ISSUE = "compatibility_issue"
    MIGRATION_PR = "migration_pr"
    FIX_COMMIT = "fix_commit"
    WORKAROUND = "workaround"
    REVERT = "revert"
    DOCUMENTATION_CHANGE = "documentation_change"
    HOTFIX = "hotfix"
    UNKNOWN_RELATED_ACTIVITY = "unknown_related_activity"


class EvidenceReference(BaseModel):
    model_config = ConfigDict(frozen=True)

    url: HttpUrl
    observed_at: datetime
    excerpt: str | None = Field(default=None, max_length=1000)
    content_sha256: str | None = Field(default=None, pattern=r"^[a-f0-9]{64}$")


class Release(BaseModel):
    model_config = ConfigDict(frozen=True)

    project: str
    package: str
    version: str
    released_at: datetime
    repository: HttpUrl
    release_notes: HttpUrl | None = None
    migration_documentation: HttpUrl | None = None
    breaking_change_evidence: str | None = None
    sources: tuple[EvidenceReference, ...] = Field(min_length=1)


class DownstreamRepository(BaseModel):
    model_config = ConfigDict(frozen=True)

    repository: HttpUrl
    dependency_relationship: str
    observed_versions: tuple[str, ...] = ()
    evidence: EvidenceReference


class DownstreamEvent(BaseModel):
    model_config = ConfigDict(frozen=True)

    repository: HttpUrl
    occurred_at: datetime
    event_type: DownstreamEventType
    title: str
    text: str | None = None
    target_package: str
    target_release: str
    evidence: tuple[EvidenceReference, ...] = Field(min_length=1)
    confidence: Confidence
    evidence_reason: str = Field(min_length=10)

    @model_validator(mode="after")
    def reject_unexplained_high_confidence(self) -> DownstreamEvent:
        if self.confidence is Confidence.HIGH and len(self.evidence_reason.strip()) < 25:
            raise ValueError("high-confidence evidence requires a specific rationale")
        return self
