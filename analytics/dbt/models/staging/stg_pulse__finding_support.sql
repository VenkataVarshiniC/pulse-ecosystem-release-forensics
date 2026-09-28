select
    finding_id,
    'artifact'::text as support_type,
    artifact_id::text as support_id,
    support_role
from {{ source('pulse_core', 'finding_artifact_support') }}
union all
select
    finding_id,
    'observation'::text as support_type,
    observation_id::text as support_id,
    support_role
from {{ source('pulse_core', 'finding_observation_support') }}
union all
select
    finding_id,
    'review'::text as support_type,
    review_id::text as support_id,
    support_role
from {{ source('pulse_core', 'finding_review_support') }}
