with shape as (
    select count(*) as candidates,
           count(distinct artifact_id) as artifacts,
           count(distinct repository_id) as repositories,
           count(*) filter (where terminal_review_status = 'ACCEPT') as accepted,
           count(*) filter (where terminal_review_status = 'REJECT') as rejected
    from {{ ref('fct_candidate_review') }}
), case_shape as (
    select c.case_name,
           count(f.candidate_id) as candidate_count,
           count(f.candidate_id) filter (where f.has_terminal_review) as terminal_count
    from {{ ref('dim_case') }} c
    left join {{ ref('fct_candidate_review') }} f on c.case_key = f.case_key
    group by c.case_name
)
select 'frozen_candidate_shape' as failure from shape
where candidates <> 2 or artifacts <> 1 or repositories <> 1
   or accepted <> 0 or rejected <> 2
union all
select 'pytest_zero_denominator' from case_shape
where case_name = 'pytest-8.0.0' and (candidate_count <> 0 or terminal_count <> 0)
union all
select 'urllib3_candidate_shape' from case_shape
where case_name = 'urllib3-2.0.0' and (candidate_count <> 2 or terminal_count <> 2)
