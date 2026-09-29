with selected_candidates as (
    select sc.analysis_snapshot_id, c.case_version_id, c.repository_id,
           count(*) as candidate_count
    from {{ source('pulse_core', 'snapshot_candidate') }} sc
    join {{ source('pulse_core', 'candidate') }} c on sc.candidate_id = c.candidate_id
    group by 1, 2, 3
)
select e.analysis_snapshot_id, e.case_version_id, e.repository_id
from {{ ref('fct_repository_investigation') }} e
left join selected_candidates c
    on e.analysis_snapshot_id = c.analysis_snapshot_id
   and e.case_version_id = c.case_version_id and e.repository_id = c.repository_id
where e.candidate_count <> coalesce(c.candidate_count, 0)
   or e.has_candidate <> (coalesce(c.candidate_count, 0) > 0)
