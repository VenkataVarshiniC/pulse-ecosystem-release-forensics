// Explicitly mirrors the M5.2 OpenAPI read models. Nulls and literal states are intentional.
export type UUID = string;
export type SnapshotState = 'PUBLISHED_VALIDATION';
export type FindingStatus = 'UNKNOWN' | 'NO_QUALIFYING_EVIDENCE_FOUND' | 'QUALIFYING_EVIDENCE';
export type SufficiencyStatus =
  | 'SUFFICIENT'
  | 'INSUFFICIENT'
  | 'SOURCE_UNAVAILABLE'
  | 'CONFLICTING';
export type ReviewDecision = 'ACCEPT' | 'REJECT' | 'NEEDS_EVIDENCE';
export type CaptureMethod = 'collector' | 'connector_assisted' | 'fixture';

export interface Scope {
  case_id: UUID;
  case_version_id: UUID;
  case_version: number;
  analysis_snapshot_id: UUID;
  snapshot_state: SnapshotState;
  rule_version: string;
  metric_definition_version: string;
  model_version: string;
}

export interface InvestigationSummary {
  scope: Scope;
  case_name: string;
  package_name: string;
  package_ecosystem: string;
  release_version: string;
  window_start: string;
  window_end: string;
  member_count: number;
}

export interface InvestigationList {
  items: InvestigationSummary[];
}

export interface Member {
  repository_id: UUID;
  repository_name: string;
  identity_status: string;
  selection_method: string;
  eligibility_status: string;
  candidate_count: number;
  unknown_count: number;
  bounded_no_count: number;
  qualifying_count: number;
}

export interface InvestigationDetail {
  investigation: InvestigationSummary;
  members: Member[];
}

export interface SourceState {
  collection_task_id: UUID;
  source_type: string;
  task_type: string;
  required: boolean;
  terminal_status: string;
  error_class: string | null;
}

export interface Observation {
  observation_id: UUID;
  artifact_id: UUID;
  observation_type: string;
  declared_constraint: string | null;
  resolved_version: string | null;
  repository_ref: string | null;
  path_ref: string | null;
  observation_time: string | null;
  historical_position: string | null;
  quality_status: string;
}

export interface HistoricalPair {
  historical_pair_id: UUID;
  pair_status: string;
  path_ref: string;
  before_observation_id: UUID | null;
  after_observation_id: UUID | null;
  reason: string;
  method_version: string;
}

export interface SourceReason {
  source_type: string;
  reason_code: string;
  required: boolean;
}

export interface Finding {
  finding_id: UUID;
  lifecycle_category: string;
  question_id: string;
  finding_status: FindingStatus;
  reason_code: string;
  confidence_level: string | null;
  sufficiency_status: SufficiencyStatus;
  sufficiency_reason_code: string;
  required_source_set_version: string;
  rule_version: string;
  source_reasons: SourceReason[];
  artifact_support_ids: UUID[];
  observation_support_ids: UUID[];
  review_support_ids: UUID[];
}

export interface FindingsResponse {
  scope: Scope;
  repository_id: UUID;
  items: Finding[];
}

export interface RepositoryDetail {
  scope: Scope;
  member: Member;
  source_states: SourceState[];
  observations: Observation[];
  historical_pairs: HistoricalPair[];
  findings: Finding[];
  candidate_count: number;
}

export interface ArtifactEvidence {
  artifact_id: UUID;
  artifact_type: string;
  source_type: string;
  capture_method: CaptureMethod;
  repository_ref: string | null;
  source_event_time: string | null;
  retrieved_at: string;
  content_sha256: string;
  observations: Observation[];
}

export interface EvidencePage {
  scope: Scope;
  repository_id: UUID;
  items: ArtifactEvidence[];
  next_cursor: UUID | null;
}

export interface Provenance {
  scope: Scope;
  repository_id: UUID;
  artifact_id: UUID;
  artifact_type: string;
  source_type: string;
  source_provider: string;
  capture_method: CaptureMethod;
  public_locator: string | null;
  repository_ref: string | null;
  source_event_time: string | null;
  retrieved_at: string;
  content_sha256: string;
  collection_task_id: UUID | null;
  collection_run_id: UUID | null;
  collection_run_kind: string | null;
  task_status: string | null;
  run_status: string | null;
  linked_candidate_ids: UUID[];
  linked_finding_ids: UUID[];
  external_public_locators: string[];
}

export interface ReviewRead {
  review_id: UUID;
  decision: ReviewDecision;
  reason_code: string;
  review_note: string | null;
  reviewed_at: string;
  review_origin: 'DIRECT' | 'INHERITED';
  inherited_from_review_id: UUID | null;
  reviewer_identity: string | null;
}

export interface Candidate {
  candidate_id: UUID;
  artifact_id: UUID;
  candidate_fingerprint: string;
  lifecycle_category: string;
  candidate_rule_id: string;
  candidate_rule_version: string;
  source_origin: 'LOCAL_DOWNSTREAM' | 'COPIED_UPSTREAM' | 'UNRESOLVED';
  candidate_status: 'EMITTED' | 'WITHDRAWN';
  candidate_reason: string;
  span_ref: string;
  review: ReviewRead | null;
  original_candidate_id: UUID | null;
  original_review_id: UUID | null;
  review_write_enabled: boolean;
}

export interface CandidatesResponse {
  scope: Scope;
  repository_id: UUID;
  items: Candidate[];
}
