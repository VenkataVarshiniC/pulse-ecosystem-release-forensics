select
    finding_id,
    case_version_id,
    repository_id,
    lifecycle_category,
    question_id,
    finding_version,
    finding_status,
    sufficiency_assessment_id,
    rule_version,
    reason_code,
    confidence_level,
    created_at
from {{ source('pulse_core', 'lifecycle_finding') }}
