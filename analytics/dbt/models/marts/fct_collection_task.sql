select
    s.analysis_snapshot_id,
    s.snapshot_state,
    s.manifest_sha256 as input_manifest_sha256,
    t.case_version_id as case_key,
    t.repository_id as repository_key,
    t.source_id as source_key,
    t.collection_task_id,
    t.collection_run_id,
    t.case_version_id,
    t.repository_id,
    t.source_id,
    t.plan_task_key,
    t.task_type,
    t.required_flag,
    t.terminal_status,
    t.actual_attempt_count,
    t.retry_count,
    t.capture_count,
    t.has_capture,
    not t.required_flag and t.terminal_status = 'not_found' as optional_not_found,
    t.source_plan_version
from {{ ref('int_analysis_snapshot') }} s
join {{ source('pulse_core', 'snapshot_run') }} sr
    on s.analysis_snapshot_id = sr.analysis_snapshot_id
join {{ ref('int_collection_task_status') }} t
    on sr.collection_run_id = t.collection_run_id
   and s.case_version_id = t.case_version_id
where t.run_kind = 'release_collection'
