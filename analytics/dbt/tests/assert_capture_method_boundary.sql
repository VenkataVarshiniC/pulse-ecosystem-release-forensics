select a.artifact_id
from {{ source('pulse_core', 'snapshot_artifact') }} sa
join {{ ref('stg_pulse__artifacts') }} a on sa.artifact_id = a.artifact_id
where a.capture_method = 'fixture'
union all
select a.artifact_id
from {{ ref('stg_pulse__artifacts') }} a
where a.capture_method <> 'collector'
  and (a.collection_task_id is not null or a.history_run_id is not null)
