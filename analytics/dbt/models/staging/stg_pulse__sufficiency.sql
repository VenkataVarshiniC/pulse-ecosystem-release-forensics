select
    assessment_id,
    case_version_id,
    repository_id,
    lifecycle_category,
    question_id,
    assessment_version,
    sufficiency_status,
    reason_code,
    required_source_set_version,
    rule_version,
    assessed_at
from {{ source('pulse_core', 'sufficiency_assessment') }}
