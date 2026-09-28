select s.assessment_id
from {{ source('pulse_core', 'sufficiency_assessment') }} s
left join {{ ref('int_stage_sufficiency') }} i on s.assessment_id = i.assessment_id
where i.assessment_id is null
   or s.sufficiency_status is distinct from i.source_sufficiency_status
   or s.assessed_at is distinct from i.assessed_at
   or (s.sufficiency_status = 'LEGACY_UNCLASSIFIED'
       and i.analytical_status_family <> 'UNRESOLVED_LEGACY')
