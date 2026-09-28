select
    t.collection_task_id
from {{ source('pulse_ingestion', 'collection_task') }} t
left join {{ ref('int_collection_task_status') }} i
    on t.collection_task_id = i.collection_task_id
where i.collection_task_id is null
   or t.required_flag is distinct from i.required_flag
   or t.terminal_status is distinct from i.terminal_status
   or t.repository_id is distinct from i.repository_id
   or t.attempt_count is distinct from i.actual_attempt_count
   or i.retry_count <> greatest(i.actual_attempt_count - 1, 0)
