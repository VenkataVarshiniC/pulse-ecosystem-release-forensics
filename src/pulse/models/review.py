"""Auditable collection attempts and evidence-review state."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, model_validator

from pulse.models.case import SourceSystem
from pulse.models.evidence import Confidence, DownstreamEventType, EvidenceReference, LifecycleStage


class CollectionStatus(StrEnum):
    SUCCEEDED = "succeeded"
    INCOMPLETE = "incomplete"
    FAILED = "failed"
    RATE_LIMITED = "rate_limited"
    NOT_FOUND = "not_found"


class CollectionObservation(BaseModel):
    model_config = ConfigDict(frozen=True)

    observation_id: str = Field(min_length=12)
    case_id: str
    repository: str | None = None
    source: SourceSystem
    query_type: str
    query: str
    started_at: datetime
    completed_at: datetime
    records_examined: int = Field(ge=0)
    matching_records: int = Field(ge=0)
    status: CollectionStatus
    notes: str | None = None

    @model_validator(mode="after")
    def validate_counts_and_times(self) -> CollectionObservation:
        if self.completed_at < self.started_at:
            raise ValueError("collection completion cannot precede start")
        if self.matching_records > self.records_examined:
            raise ValueError("matching records cannot exceed examined records")
        return self


class EvidenceStatus(StrEnum):
    CANDIDATE = "candidate"
    NEEDS_REVIEW = "needs_review"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class ReviewableEvidence(BaseModel):
    model_config = ConfigDict(frozen=True)

    candidate_id: str = Field(min_length=12)
    case_id: str
    repository: HttpUrl
    occurred_at: datetime
    lifecycle_stage: LifecycleStage
    event_type: DownstreamEventType
    title: str
    target_package: str
    target_release: str
    evidence: tuple[EvidenceReference, ...] = Field(min_length=1)
    classification_rule: str = Field(min_length=3)
    classification_reason: str = Field(min_length=20)
    confidence: Confidence
    status: EvidenceStatus = EvidenceStatus.CANDIDATE
    reviewer_note: str | None = None
    reviewed_at: datetime | None = None

    @model_validator(mode="after")
    def validate_review_state(self) -> ReviewableEvidence:
        terminal = self.status in {EvidenceStatus.ACCEPTED, EvidenceStatus.REJECTED}
        if terminal and (not self.reviewer_note or self.reviewed_at is None):
            raise ValueError("accepted or rejected evidence requires a review note and timestamp")
        if self.confidence is Confidence.HIGH and self.classification_rule == "keyword_match":
            raise ValueError("keyword matches alone cannot receive high confidence")
        return self

    def transition(
        self,
        status: EvidenceStatus,
        *,
        note: str | None = None,
        reviewed_at: datetime | None = None,
    ) -> ReviewableEvidence:
        allowed = {
            EvidenceStatus.CANDIDATE: {
                EvidenceStatus.NEEDS_REVIEW,
                EvidenceStatus.ACCEPTED,
                EvidenceStatus.REJECTED,
            },
            EvidenceStatus.NEEDS_REVIEW: {EvidenceStatus.ACCEPTED, EvidenceStatus.REJECTED},
            EvidenceStatus.ACCEPTED: set(),
            EvidenceStatus.REJECTED: set(),
        }
        if status not in allowed[self.status]:
            raise ValueError(f"invalid evidence transition: {self.status} -> {status}")
        values = self.model_dump()
        values.update(status=status, reviewer_note=note, reviewed_at=reviewed_at)
        return ReviewableEvidence.model_validate(values)
