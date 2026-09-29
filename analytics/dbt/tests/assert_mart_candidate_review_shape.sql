with shape as (
    select s.rule_version, count(f.candidate_id) as candidates,
           count(distinct artifact_id) as artifacts,
           count(distinct repository_id) as repositories,
           count(*) filter (where terminal_review_status = 'ACCEPT') as accepted,
           count(*) filter (where terminal_review_status = 'REJECT') as rejected
    from {{ ref('int_analysis_snapshot') }} s
    left join {{ ref('fct_candidate_review') }} f
        on s.analysis_snapshot_id = f.analysis_snapshot_id
    group by s.rule_version
), case_shape as (
    select s.rule_version, c.case_name,
           count(f.candidate_id) as candidate_count,
           count(f.candidate_id) filter (where f.has_terminal_review) as terminal_count
    from {{ ref('int_analysis_snapshot') }} s
    join {{ ref('dim_case') }} c on s.case_version_id = c.case_key
    left join {{ ref('fct_candidate_review') }} f
        on s.analysis_snapshot_id = f.analysis_snapshot_id
    group by s.rule_version,c.case_name
)
select 'candidate_shape' as failure from shape
where candidates <> 2 or artifacts <> 1 or repositories <> 1
   or accepted <> 0 or rejected <> 2
union all
select 'pytest_zero_denominator' from case_shape
where case_name = 'pytest-8.0.0' and (candidate_count <> 0 or terminal_count <> 0)
union all
select 'urllib3_candidate_shape' from case_shape
where case_name = 'urllib3-2.0.0' and (candidate_count <> 2 or terminal_count <> 2)
