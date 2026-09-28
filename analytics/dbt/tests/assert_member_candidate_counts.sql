with source_candidates as (
    select case_version_id, repository_id, count(*) as candidate_count
    from {{ source('pulse_core', 'candidate') }}
    group by 1, 2
)
select e.case_version_id, e.repository_id
from {{ ref('int_repository_evidence') }} e
left join source_candidates c
    on e.case_version_id = c.case_version_id and e.repository_id = c.repository_id
where e.candidate_count <> coalesce(c.candidate_count, 0)
   or e.has_candidate <> (coalesce(c.candidate_count, 0) > 0)
