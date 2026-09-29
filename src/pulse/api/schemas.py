"""Typed application read and guarded review contracts."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, Field


class SnapshotState(StrEnum):
    PUBLISHED_VALIDATION = "PUBLISHED_VALIDATION"


class FindingStatus(StrEnum):
    UNKNOWN = "UNKNOWN"
    NO_QUALIFYING_EVIDENCE_FOUND = "NO_QUALIFYING_EVIDENCE_FOUND"
    QUALIFYING_EVIDENCE = "QUALIFYING_EVIDENCE"


class SufficiencyStatus(StrEnum):
    SUFFICIENT = "SUFFICIENT"
    INSUFFICIENT = "INSUFFICIENT"
    SOURCE_UNAVAILABLE = "SOURCE_UNAVAILABLE"
    CONFLICTING = "CONFLICTING"


class ReviewDecision(StrEnum):
    ACCEPT = "ACCEPT"
    REJECT = "REJECT"
    NEEDS_EVIDENCE = "NEEDS_EVIDENCE"


class CaptureMethod(StrEnum):
    COLLECTOR = "collector"
    CONNECTOR_ASSISTED = "connector_assisted"
    FIXTURE = "fixture"


class Scope(BaseModel):
    case_id: UUID
    case_version_id: UUID
    case_version: int
    analysis_snapshot_id: UUID
    snapshot_state: SnapshotState
    rule_version: str
    metric_definition_version: str
    model_version: str


class InvestigationSummary(BaseModel):
    scope: Scope
    case_name: str
    package_name: str
    package_ecosystem: str
    release_version: str
    window_start: datetime
    window_end: datetime
    member_count: int


class InvestigationList(BaseModel):
    items: list[InvestigationSummary]


class Member(BaseModel):
    repository_id: UUID
    repository_name: str
    identity_status: str
    selection_method: str
    eligibility_status: str
    candidate_count: int
    unknown_count: int
    bounded_no_count: int
    qualifying_count: int


class InvestigationDetail(BaseModel):
    investigation: InvestigationSummary
    members: list[Member]


class SourceState(BaseModel):
    collection_task_id: UUID
    source_type: str
    task_type: str
    required: bool
    terminal_status: str
    error_class: str | None = None


class Observation(BaseModel):
    observation_id: UUID
    artifact_id: UUID
    observation_type: str
    declared_constraint: str | None = None
    resolved_version: str | None = None
    repository_ref: str | None = None
    path_ref: str | None = None
    observation_time: datetime | None = None
    historical_position: str | None = None
    quality_status: str


class HistoricalPair(BaseModel):
    historical_pair_id: UUID
    pair_status: str
    path_ref: str
    before_observation_id: UUID | None = None
    after_observation_id: UUID | None = None
    reason: str
    method_version: str


class SourceReason(BaseModel):
    source_type: str
    reason_code: str
    required: bool


class Finding(BaseModel):
    finding_id: UUID
    lifecycle_category: str
    question_id: str
    finding_status: FindingStatus
    reason_code: str
    confidence_level: str | None = None
    sufficiency_status: SufficiencyStatus
    sufficiency_reason_code: str
    required_source_set_version: str
    rule_version: str
    source_reasons: list[SourceReason]
    artifact_support_ids: list[UUID]
    observation_support_ids: list[UUID]
    review_support_ids: list[UUID]


class FindingsResponse(BaseModel):
    scope: Scope
    repository_id: UUID
    items: list[Finding]


class RepositoryDetail(BaseModel):
    scope: Scope
    member: Member
    source_states: list[SourceState]
    observations: list[Observation]
    historical_pairs: list[HistoricalPair]
    findings: list[Finding]
    candidate_count: int


class ArtifactEvidence(BaseModel):
    artifact_id: UUID
    artifact_type: str
    source_type: str
    capture_method: CaptureMethod
    repository_ref: str | None = None
    source_event_time: datetime | None = None
    retrieved_at: datetime
    content_sha256: str
    observations: list[Observation]


class EvidencePage(BaseModel):
    scope: Scope
    repository_id: UUID
    items: list[ArtifactEvidence]
    next_cursor: UUID | None = None


class Provenance(BaseModel):
    scope: Scope
    repository_id: UUID
    artifact_id: UUID
    artifact_type: str
    source_type: str
    source_provider: str
    capture_method: CaptureMethod
    public_locator: str | None = None
    repository_ref: str | None = None
    source_event_time: datetime | None = None
    retrieved_at: datetime
    content_sha256: str
    collection_task_id: UUID | None = None
    collection_run_id: UUID | None = None
    collection_run_kind: str | None = None
    task_status: str | None = None
    run_status: str | None = None
    linked_candidate_ids: list[UUID]
    linked_finding_ids: list[UUID]
    external_public_locators: list[str]


class ReviewRead(BaseModel):
    review_id: UUID
    decision: ReviewDecision
    reason_code: str
    review_note: str | None = None
    reviewed_at: datetime
    review_origin: str
    inherited_from_review_id: UUID | None = None
    reviewer_identity: str | None = None


class Candidate(BaseModel):
    candidate_id: UUID
    artifact_id: UUID
    candidate_fingerprint: str
    lifecycle_category: str
    candidate_rule_id: str
    candidate_rule_version: str
    source_origin: str
    candidate_status: str
    candidate_reason: str
    span_ref: str
    review: ReviewRead | None = None
    original_candidate_id: UUID | None = None
    original_review_id: UUID | None = None
    review_write_enabled: bool = False


class CandidatesResponse(BaseModel):
    scope: Scope
    repository_id: UUID
    items: list[Candidate]


class ReviewSubmission(BaseModel):
    decision: ReviewDecision
    reason_code: str
    review_note: str | None = None
    expected_review_id: UUID | None = None
    idempotency_key: str = Field(min_length=8, max_length=128)


class ReviewReceipt(BaseModel):
    review_id: UUID
    candidate_id: UUID
    decision: ReviewDecision
    reason_code: str
    reviewed_at: datetime
    idempotent_replay: bool
