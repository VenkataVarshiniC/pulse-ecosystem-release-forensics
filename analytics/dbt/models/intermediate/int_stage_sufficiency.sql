with source_reasons as (
    select
        assessment_id,
        count(*) as recorded_source_reason_count,
        count(*) filter (where required_flag) as required_source_reason_count
    from {{ source('pulse_core', 'assessment_source_reason') }}
    group by assessment_id
)
select
    s.assessment_id,
    s.case_version_id,
    s.repository_id,
    s.lifecycle_category,
    s.question_id,
    s.assessment_version,
    s.sufficiency_status as source_sufficiency_status,
    s.reason_code,
    s.required_source_set_version,
    s.rule_version,
    s.assessed_at,
    coalesce(r.recorded_source_reason_count, 0) as recorded_source_reason_count,
    coalesce(r.required_source_reason_count, 0) as required_source_reason_count,
    case
        when s.sufficiency_status = 'LEGACY_UNCLASSIFIED' then 'UNRESOLVED_LEGACY'
        else 'EXPLICIT_SOURCE_STATUS'
    end as analytical_status_family
from {{ ref('stg_pulse__sufficiency') }} s
left join source_reasons r on s.assessment_id = r.assessment_id
