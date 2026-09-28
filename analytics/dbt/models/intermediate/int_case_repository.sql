select
    m.case_version_id,
    m.repository_id,
    c.case_id,
    c.case_version,
    c.case_name,
    c.case_status,
    c.target_release_id,
    c.target_package,
    c.target_version,
    c.release_time,
    c.window_start,
    c.window_end,
    c.source_plan_version,
    c.rule_version,
    m.repository_provider,
    m.provider_repository_id,
    m.repository_name,
    m.identity_status,
    m.selection_method,
    m.eligibility_status,
    m.selection_rationale,
    m.included_at
from {{ ref('stg_pulse__memberships') }} m
join {{ ref('stg_pulse__cases') }} c
    on m.case_version_id = c.case_version_id
