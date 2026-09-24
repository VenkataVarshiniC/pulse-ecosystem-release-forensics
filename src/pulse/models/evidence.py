"""Normalized evidence records that retain provenance and uncertainty."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, model_validator


class Confidence(StrEnum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class LifecycleStage(StrEnum):
    RELEASE = "release"
    ADOPTION_READINESS = "adoption_readiness"
    OBSERVED_ADOPTION = "observed_adoption"
    MIGRATION_FRICTION = "migration_friction"
    REMEDIATION = "remediation"
    RECOVERY_SIGNAL = "recovery_signal"


class TimestampPrecision(StrEnum):
    SECOND = "second"
    DAY = "day"


class DownstreamEventType(StrEnum):
    RELEASE_PUBLISHED = "release_published"
    COMPATIBILITY_DECLARATION = "compatibility_declaration"
    COMPATIBILITY_TEST = "compatibility_test"
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


class EvidenceEvent(BaseModel):
    model_config = ConfigDict(frozen=True)

    case_id: str = Field(min_length=1)
    repository: HttpUrl
    occurred_at: datetime
    timestamp_precision: TimestampPrecision = TimestampPrecision.SECOND
    lifecycle_stage: LifecycleStage
    event_type: DownstreamEventType
    title: str
    text: str | None = None
    target_package: str
    target_release: str
    evidence: tuple[EvidenceReference, ...] = Field(min_length=1)
    confidence: Confidence
    evidence_reason: str = Field(min_length=10)

    @model_validator(mode="after")
    def reject_unexplained_high_confidence(self) -> EvidenceEvent:
        if self.confidence is Confidence.HIGH and len(self.evidence_reason.strip()) < 25:
            raise ValueError("high-confidence evidence requires a specific rationale")
        return self


# Kept as a public alias while existing collectors migrate to the broader ledger model.
DownstreamEvent = EvidenceEvent
