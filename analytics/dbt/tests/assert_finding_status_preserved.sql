select f.finding_id
from {{ source('pulse_core', 'lifecycle_finding') }} f
left join {{ ref('int_finding_evidence') }} i on f.finding_id = i.finding_id
where i.finding_id is null
   or f.finding_status is distinct from i.finding_status
   or f.sufficiency_assessment_id is distinct from i.sufficiency_assessment_id
   or f.created_at is distinct from i.created_at
