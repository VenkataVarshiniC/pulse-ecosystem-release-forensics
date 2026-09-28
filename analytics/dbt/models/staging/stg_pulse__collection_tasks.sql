select
    t.collection_task_id,
    t.collection_run_id,
    t.case_version_id,
    t.repository_id,
    t.source_id,
    s.provider as source_provider,
    s.source_type,
    t.plan_task_key,
    t.task_type,
    t.required_flag,
    t.request_locator,
    t.attempt_count as recorded_attempt_count,
    t.terminal_status,
    t.started_at,
    t.completed_at,
    t.error_class,
    r.run_kind,
    r.collector_version,
    r.source_plan_version
from {{ source('pulse_ingestion', 'collection_task') }} t
join {{ source('pulse_ingestion', 'collection_run') }} r
    on t.collection_run_id = r.collection_run_id
join {{ source('pulse_ingestion', 'source_registry') }} s
    on t.source_id = s.source_id
