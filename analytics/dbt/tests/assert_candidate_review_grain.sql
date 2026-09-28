with source_shape as (
    select
        count(*) as candidate_count,
        count(distinct c.artifact_id) as artifact_count,
        count(distinct c.repository_id) as emitting_repository_count,
        count(r.review_id) as review_count,
        count(r.review_id) filter (where r.decision = 'REJECT') as rejected_count
    from {{ source('pulse_core', 'candidate') }} c
    left join {{ source('pulse_core', 'analyst_review') }} r
        on c.candidate_id = r.candidate_id
),
intermediate_shape as (
    select
        count(*) as candidate_count,
        count(distinct artifact_id) as artifact_count,
        count(distinct repository_id) as emitting_repository_count,
        count(selected_review_id) as review_count,
        count(selected_review_id) filter (where latest_review_decision = 'REJECT')
            as rejected_count
    from {{ ref('int_candidate_terminal_review') }}
)
select 'frozen_candidate_shape' as failure
from source_shape s cross join intermediate_shape i
where s.candidate_count <> 2 or s.artifact_count <> 1
   or s.emitting_repository_count <> 1 or s.review_count <> 2 or s.rejected_count <> 2
   or i.candidate_count <> s.candidate_count or i.artifact_count <> s.artifact_count
   or i.emitting_repository_count <> s.emitting_repository_count
   or i.review_count <> s.review_count or i.rejected_count <> s.rejected_count
