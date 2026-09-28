select
    case_version_id as case_key,
    case_version_id,
    case_id,
    case_version,
    case_name,
    target_release_id as release_key,
    target_package,
    target_version,
    release_time,
    window_start,
    window_end,
    source_plan_version,
    rule_version,
    question_set_version,
    case_status
from {{ ref('stg_pulse__cases') }}
