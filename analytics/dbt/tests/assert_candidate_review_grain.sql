with source_shape as (
    select c.candidate_rule_version, count(*) as candidate_count,
           count(distinct c.artifact_id) as artifact_count,
           count(distinct c.repository_id) as repository_count,
           count(r.review_id) as review_count,
           count(r.review_id) filter (where r.decision = 'REJECT') as rejected_count
    from {{ source('pulse_core', 'candidate') }} c
    left join {{ source('pulse_core', 'analyst_review') }} r
        on c.candidate_id = r.candidate_id
    group by c.candidate_rule_version
), intermediate_shape as (
    select candidate_rule_version, count(*) as candidate_count,
           count(distinct artifact_id) as artifact_count,
           count(distinct repository_id) as repository_count,
           count(selected_review_id) as review_count,
           count(selected_review_id) filter (where latest_review_decision = 'REJECT')
               as rejected_count
    from {{ ref('int_candidate_terminal_review') }}
    group by candidate_rule_version
)
select r.candidate_rule_version as failure from source_shape r
full join intermediate_shape i using (candidate_rule_version)
where (r.candidate_count,r.artifact_count,r.repository_count,r.review_count,r.rejected_count)
      is distinct from
      (i.candidate_count,i.artifact_count,i.repository_count,i.review_count,i.rejected_count)
   or r.candidate_count <> 2 or r.artifact_count <> 1 or r.repository_count <> 1
   or r.review_count <> 2 or r.rejected_count <> 2
