select
    candidate_id,
    candidate_fingerprint,
    case_version_id,
    repository_id,
    artifact_id,
    baseline_version,
    candidate_rule_id,
    candidate_rule_version,
    lifecycle_category,
    source_origin,
    emitted_at,
    candidate_status,
    candidate_reason,
    span_ref,
    candidate_payload_ref
from {{ source('pulse_core', 'candidate') }}
