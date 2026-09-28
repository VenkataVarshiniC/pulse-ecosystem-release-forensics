with all_rows as (
    select 'bridge' as model_name, analysis_snapshot_id, case_version_id, snapshot_state,
           input_manifest_sha256 from {{ ref('bridge_case_repository') }}
    union all select 'task', analysis_snapshot_id, case_version_id, snapshot_state,
           input_manifest_sha256 from {{ ref('fct_collection_task') }}
    union all select 'repository', analysis_snapshot_id, case_version_id, snapshot_state,
           input_manifest_sha256 from {{ ref('fct_repository_investigation') }}
    union all select 'candidate', analysis_snapshot_id, case_version_id, snapshot_state,
           input_manifest_sha256 from {{ ref('fct_candidate_review') }}
    union all select 'finding', analysis_snapshot_id, case_version_id, snapshot_state,
           input_manifest_sha256 from {{ ref('fct_lifecycle_finding') }}
    union all select 'observation', analysis_snapshot_id, case_version_id, snapshot_state,
           input_manifest_sha256 from {{ ref('fct_evidence_observation') }}
), mismatched as (
    select r.model_name, r.analysis_snapshot_id, r.case_version_id
    from all_rows r
    left join {{ ref('int_analysis_snapshot') }} s
        on r.analysis_snapshot_id = s.analysis_snapshot_id
    where s.analysis_snapshot_id is null
       or r.case_version_id <> s.case_version_id
       or r.snapshot_state <> s.snapshot_state
       or r.input_manifest_sha256 <> s.manifest_sha256
)
select * from mismatched
