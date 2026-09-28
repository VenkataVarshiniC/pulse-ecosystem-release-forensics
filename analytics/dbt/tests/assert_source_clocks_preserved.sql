select a.artifact_id
from {{ source('pulse_core', 'evidence_artifact') }} a
left join {{ ref('stg_pulse__artifacts') }} s on a.artifact_id = s.artifact_id
where s.artifact_id is null
   or a.source_event_time is distinct from s.source_event_time
   or a.retrieved_at is distinct from s.retrieved_at
   or a.capture_method is distinct from s.capture_method
