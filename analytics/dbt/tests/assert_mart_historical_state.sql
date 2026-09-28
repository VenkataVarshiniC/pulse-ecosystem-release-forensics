with paths as (
    select sum(paired_path_count) as paired,
           sum(after_only_path_count) as after_only,
           sum(unresolved_path_count) as unresolved
    from {{ ref('fct_repository_investigation') }}
), case_pairs as (
    select c.case_name, sum(f.paired_path_count) as paired
    from {{ ref('fct_repository_investigation') }} f
    join {{ ref('dim_case') }} c on f.case_key = c.case_key
    group by c.case_name
)
select 'historical_status_totals' as failure from paths
where paired <> 1 or after_only <> 6 or unresolved <> 9
union all
select 'pytest_paired' from case_pairs where case_name = 'pytest-8.0.0' and paired <> 1
union all
select 'urllib3_paired' from case_pairs where case_name = 'urllib3-2.0.0' and paired <> 0
union all
select 'after_only_promoted' from {{ ref('fct_repository_investigation') }}
where has_paired_pre_release_history <> (paired_path_count > 0)
   or has_after_only_history <> (after_only_path_count > 0)
