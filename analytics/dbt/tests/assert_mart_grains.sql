with duplicates as (
    select 'bridge_case_repository' as model_name,
           analysis_snapshot_id::text || ':' || case_version_id::text || ':' || repository_id::text as grain_key
    from {{ ref('bridge_case_repository') }} group by 1, 2 having count(*) > 1
    union all
    select 'fct_collection_task', analysis_snapshot_id::text || ':' || collection_task_id::text
    from {{ ref('fct_collection_task') }} group by 1, 2 having count(*) > 1
    union all
    select 'fct_repository_investigation',
           analysis_snapshot_id::text || ':' || case_version_id::text || ':' || repository_id::text
    from {{ ref('fct_repository_investigation') }} group by 1, 2 having count(*) > 1
    union all
    select 'fct_candidate_review', analysis_snapshot_id::text || ':' || candidate_id::text
    from {{ ref('fct_candidate_review') }} group by 1, 2 having count(*) > 1
    union all
    select 'fct_lifecycle_finding', analysis_snapshot_id::text || ':' || finding_id::text
    from {{ ref('fct_lifecycle_finding') }} group by 1, 2 having count(*) > 1
    union all
    select 'fct_evidence_observation', analysis_snapshot_id::text || ':' || observation_id::text
    from {{ ref('fct_evidence_observation') }} group by 1, 2 having count(*) > 1
    union all
    select 'bridge_finding_evidence', analysis_snapshot_id::text || ':' || finding_id::text
        || ':' || support_type || ':' || support_id || ':' || support_role
    from {{ ref('bridge_finding_evidence') }} group by 1, 2 having count(*) > 1
)
select * from duplicates
