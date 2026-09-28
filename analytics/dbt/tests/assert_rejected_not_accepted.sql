select candidate_id::text as failed_identity
from {{ ref('int_candidate_terminal_review') }}
where latest_review_decision in ('REJECT', 'NEEDS_EVIDENCE')
  and has_accepted_review
union all
select f.finding_id::text as failed_identity
from {{ source('pulse_core', 'finding_review_support') }} s
join {{ source('pulse_core', 'analyst_review') }} r on s.review_id = r.review_id
join {{ ref('int_finding_evidence') }} f on s.finding_id = f.finding_id
where f.finding_status = 'QUALIFYING_EVIDENCE' and r.decision <> 'ACCEPT'
