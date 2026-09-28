select
    c.case_version_id,
    c.case_id,
    c.case_version,
    c.case_name,
    c.target_release_id,
    r.package_ecosystem,
    r.package_name_normalized as target_package,
    r.version as target_version,
    r.release_time,
    r.release_source_id,
    r.release_artifact_id,
    c.window_start,
    c.window_end,
    c.source_plan_version,
    c.rule_version,
    c.question_set_version,
    c.status as case_status,
    c.created_at as case_created_at
from {{ source('pulse_core', 'investigation_case') }} c
join {{ source('pulse_core', 'dependency_release') }} r
    on c.target_release_id = r.release_id
