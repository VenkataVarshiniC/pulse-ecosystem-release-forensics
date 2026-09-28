with expected as (
    select s.analysis_snapshot_id, m.case_version_id, m.repository_id
    from {{ ref('int_analysis_snapshot') }} s
    join {{ source('pulse_core', 'cohort_membership') }} m
        on s.case_version_id = m.case_version_id
), missing_bridge as (
    select e.* from expected e
    left join {{ ref('bridge_case_repository') }} b
        on e.analysis_snapshot_id = b.analysis_snapshot_id
       and e.case_version_id = b.case_version_id and e.repository_id = b.repository_id
    where b.repository_id is null
), missing_fact as (
    select e.* from expected e
    left join {{ ref('fct_repository_investigation') }} f
        on e.analysis_snapshot_id = f.analysis_snapshot_id
       and e.case_version_id = f.case_version_id and e.repository_id = f.repository_id
    where f.repository_id is null
), extra_bridge as (
    select b.analysis_snapshot_id, b.case_version_id, b.repository_id
    from {{ ref('bridge_case_repository') }} b
    left join expected e
        on b.analysis_snapshot_id = e.analysis_snapshot_id
       and b.case_version_id = e.case_version_id and b.repository_id = e.repository_id
    where e.repository_id is null
), extra_fact as (
    select f.analysis_snapshot_id, f.case_version_id, f.repository_id
    from {{ ref('fct_repository_investigation') }} f
    left join expected e
        on f.analysis_snapshot_id = e.analysis_snapshot_id
       and f.case_version_id = e.case_version_id and f.repository_id = e.repository_id
    where e.repository_id is null
)
select * from missing_bridge
union all select * from missing_fact
union all select * from extra_bridge
union all select * from extra_fact
