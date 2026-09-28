select 'fixture_candidate' as failure, c.artifact_id
from {{ ref('fct_candidate_review') }} c where c.capture_method = 'fixture'
union all
select 'fixture_observation', o.artifact_id
from {{ ref('fct_evidence_observation') }} o where o.capture_method = 'fixture'
union all
select 'source_event_clock_changed', o.artifact_id
from {{ ref('fct_evidence_observation') }} o
join {{ ref('stg_pulse__artifacts') }} a on o.artifact_id = a.artifact_id
where o.source_event_time is distinct from a.source_event_time
   or o.retrieved_at is distinct from a.retrieved_at
