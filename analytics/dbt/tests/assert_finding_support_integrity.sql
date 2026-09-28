select s.finding_id
from {{ ref('stg_pulse__finding_support') }} s
left join {{ ref('stg_pulse__findings') }} f on s.finding_id = f.finding_id
left join {{ ref('stg_pulse__artifacts') }} a
    on s.support_type = 'artifact' and s.support_id = a.artifact_id::text
left join {{ ref('stg_pulse__dependency_observations') }} o
    on s.support_type = 'observation' and s.support_id = o.observation_id::text
left join {{ ref('stg_pulse__reviews') }} r
    on s.support_type = 'review' and s.support_id = r.review_id::text
where f.finding_id is null
   or (s.support_type = 'artifact' and a.artifact_id is null)
   or (s.support_type = 'observation' and o.observation_id is null)
   or (s.support_type = 'review' and r.review_id is null)
   or s.support_type not in ('artifact', 'observation', 'review')
