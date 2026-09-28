with source_members as (
    select case_version_id, repository_id
    from {{ source('pulse_core', 'cohort_membership') }}
),
missing as (
    select s.case_version_id, s.repository_id
    from source_members s
    left join {{ ref('int_case_repository') }} c
        on s.case_version_id = c.case_version_id and s.repository_id = c.repository_id
    left join {{ ref('int_repository_evidence') }} e
        on s.case_version_id = e.case_version_id and s.repository_id = e.repository_id
    where c.repository_id is null or e.repository_id is null
),
extra as (
    select c.case_version_id, c.repository_id
    from {{ ref('int_case_repository') }} c
    left join source_members s
        on c.case_version_id = s.case_version_id and c.repository_id = s.repository_id
    where s.repository_id is null
),
duplicate_spine as (
    select case_version_id, repository_id
    from {{ ref('int_case_repository') }}
    group by 1, 2 having count(*) <> 1
),
duplicate_evidence as (
    select case_version_id, repository_id
    from {{ ref('int_repository_evidence') }}
    group by 1, 2 having count(*) <> 1
)
select * from missing
union all select * from extra
union all select * from duplicate_spine
union all select * from duplicate_evidence
