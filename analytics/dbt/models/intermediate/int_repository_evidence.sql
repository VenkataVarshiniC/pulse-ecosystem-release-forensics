with member_tasks as (
    select
        case_version_id,
        repository_id,
        count(*) as planned_member_task_count,
        count(*) filter (where required_flag) as required_member_task_count,
        count(*) filter (where required_flag and terminal_status <> 'succeeded')
            as required_member_task_gap_count,
        count(*) filter (where not required_flag and terminal_status = 'not_found')
            as optional_not_found_count
    from {{ ref('int_collection_task_status') }}
    where repository_id is not null
    group by case_version_id, repository_id
),
upstream_tasks as (
    select
        case_version_id,
        count(*) filter (where required_flag and terminal_status <> 'succeeded')
            as required_upstream_task_gap_count
    from {{ ref('int_collection_task_status') }}
    where repository_id is null
    group by case_version_id
),
historical as (
    select
        case_version_id,
        repository_id,
        count(*) filter (where pair_status = 'PAIRED') as paired_path_count,
        count(*) filter (where pair_status = 'AFTER_ONLY') as after_only_path_count,
        count(*) filter (where pair_status = 'UNRESOLVED') as unresolved_path_count,
        count(*) filter (where pair_status = 'CROSS_FILE_AMBIGUITY')
            as ambiguous_path_count
    from {{ ref('stg_pulse__historical_pairs') }}
    group by case_version_id, repository_id
),
observations as (
    select
        o.case_version_id,
        o.repository_id,
        count(*) filter (where o.observation_type = 'HISTORICAL_DECLARATION')
            as historical_declaration_count,
        count(*) filter (
            where o.observation_type = 'RESOLVED_VERSION'
              and o.resolved_version = c.target_version
        ) as exact_target_resolution_count
    from {{ ref('stg_pulse__dependency_observations') }} o
    join {{ ref('stg_pulse__cases') }} c on o.case_version_id = c.case_version_id
    group by o.case_version_id, o.repository_id
),
artifact_scope as (
    select t.case_version_id, a.repository_id, a.artifact_id, a.artifact_type
    from {{ ref('stg_pulse__artifacts') }} a
    join {{ ref('stg_pulse__collection_tasks') }} t
        on a.collection_task_id = t.collection_task_id
    where a.repository_id is not null and a.capture_method = 'collector'
    union all
    select r.case_version_id, a.repository_id, a.artifact_id, a.artifact_type
    from {{ ref('stg_pulse__artifacts') }} a
    join {{ source('pulse_ingestion', 'collection_run') }} r
        on a.history_run_id = r.collection_run_id
    where a.repository_id is not null and a.capture_method = 'collector'
),
member_artifacts as (
    select
        case_version_id,
        repository_id,
        count(*) filter (where artifact_type = 'raw_capture') as release_capture_count,
        count(*) filter (where artifact_type <> 'raw_capture') as historical_capture_count
    from artifact_scope
    group by case_version_id, repository_id
),
member_candidates as (
    select
        case_version_id,
        repository_id,
        count(*) as candidate_count,
        count(*) filter (where has_terminal_review) as terminal_review_count
    from {{ ref('int_candidate_terminal_review') }}
    group by case_version_id, repository_id
)
select
    spine.case_version_id,
    spine.repository_id,
    spine.case_name,
    coalesce(t.planned_member_task_count, 0) as planned_member_task_count,
    coalesce(t.required_member_task_count, 0) as required_member_task_count,
    coalesce(t.optional_not_found_count, 0) as optional_not_found_count,
    coalesce(t.required_member_task_gap_count, 0) as required_member_task_gap_count,
    coalesce(u.required_upstream_task_gap_count, 0) as required_upstream_task_gap_count,
    coalesce(t.required_member_task_count, 0) > 0
        and coalesce(t.required_member_task_gap_count, 0) = 0
        and coalesce(u.required_upstream_task_gap_count, 0) = 0
        as core_collection_complete,
    coalesce(h.paired_path_count, 0) as paired_path_count,
    coalesce(h.after_only_path_count, 0) as after_only_path_count,
    coalesce(h.unresolved_path_count, 0) as unresolved_path_count,
    coalesce(h.ambiguous_path_count, 0) as ambiguous_path_count,
    coalesce(h.paired_path_count, 0) > 0 as has_paired_pre_release_history,
    coalesce(h.after_only_path_count, 0) > 0 as has_after_only_history,
    coalesce(o.historical_declaration_count, 0) as historical_declaration_count,
    coalesce(o.historical_declaration_count, 0) > 0 as has_historical_declaration,
    coalesce(o.exact_target_resolution_count, 0) > 0
        as has_exact_target_resolution_observation,
    coalesce(a.release_capture_count, 0) as release_capture_count,
    coalesce(a.historical_capture_count, 0) as historical_capture_count,
    coalesce(c.candidate_count, 0) as candidate_count,
    coalesce(c.candidate_count, 0) > 0 as has_candidate,
    coalesce(c.terminal_review_count, 0) as terminal_review_count,
    coalesce(c.terminal_review_count, 0) > 0 as has_terminal_review
from {{ ref('int_case_repository') }} spine
left join member_tasks t
    on spine.case_version_id = t.case_version_id and spine.repository_id = t.repository_id
left join upstream_tasks u on spine.case_version_id = u.case_version_id
left join historical h
    on spine.case_version_id = h.case_version_id and spine.repository_id = h.repository_id
left join observations o
    on spine.case_version_id = o.case_version_id and spine.repository_id = o.repository_id
left join member_artifacts a
    on spine.case_version_id = a.case_version_id and spine.repository_id = a.repository_id
left join member_candidates c
    on spine.case_version_id = c.case_version_id and spine.repository_id = c.repository_id
