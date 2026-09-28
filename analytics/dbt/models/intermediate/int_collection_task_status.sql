with attempts as (
    select
        collection_task_id,
        count(*) as actual_attempt_count,
        count(*) filter (where attempt_number > 1) as retry_count,
        max(attempt_number) as max_attempt_number
    from {{ source('pulse_ingestion', 'task_attempt') }}
    group by collection_task_id
),
captures as (
    select
        collection_task_id,
        count(*) as capture_count
    from {{ ref('stg_pulse__artifacts') }}
    where collection_task_id is not null
    group by collection_task_id
)
select
    t.*,
    coalesce(a.actual_attempt_count, 0) as actual_attempt_count,
    coalesce(a.retry_count, 0) as retry_count,
    a.max_attempt_number,
    coalesce(c.capture_count, 0) as capture_count,
    coalesce(c.capture_count, 0) > 0 as has_capture
from {{ ref('stg_pulse__collection_tasks') }} t
left join attempts a on t.collection_task_id = a.collection_task_id
left join captures c on t.collection_task_id = c.collection_task_id
