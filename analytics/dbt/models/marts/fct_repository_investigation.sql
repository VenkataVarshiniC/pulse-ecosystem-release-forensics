with candidates as (
    select
        analysis_snapshot_id,
        case_version_id,
        repository_id,
        count(*) as selected_candidate_count,
        count(*) filter (where has_terminal_review) as terminal_review_count,
        count(*) filter (where accepted_indicator) as accepted_review_count,
        count(*) filter (where rejected_indicator) as rejected_review_count
    from {{ ref('fct_candidate_review') }}
    group by analysis_snapshot_id, case_version_id, repository_id
), findings as (
    select
        analysis_snapshot_id,
        case_version_id,
        repository_id,
        count(*) as selected_finding_count,
        count(*) filter (where finding_status = 'UNKNOWN') as unknown_finding_count,
        count(*) filter (where finding_status = 'NO_QUALIFYING_EVIDENCE_FOUND')
            as bounded_no_finding_count,
        count(*) filter (where source_sufficiency_status = 'LEGACY_UNCLASSIFIED')
            as legacy_unclassified_count,
        max(finding_status) filter (where lifecycle_category = 'observed_adoption')
            as observed_adoption_status,
        max(finding_status) filter (where lifecycle_category = 'recovery_signal')
            as recovery_signal_status
    from {{ ref('fct_lifecycle_finding') }}
    group by analysis_snapshot_id, case_version_id, repository_id
), observations as (
    select
        analysis_snapshot_id,
        case_version_id,
        repository_id,
        count(*) as selected_observation_count
    from {{ ref('fct_evidence_observation') }}
    group by analysis_snapshot_id, case_version_id, repository_id
)
select
    b.analysis_snapshot_id,
    b.snapshot_state,
    b.input_manifest_sha256,
    b.case_key,
    b.repository_key,
    b.case_version_id,
    b.repository_id,
    e.core_collection_complete,
    e.planned_member_task_count,
    e.required_member_task_count,
    e.optional_not_found_count,
    e.required_member_task_gap_count,
    e.required_upstream_task_gap_count,
    e.paired_path_count,
    e.after_only_path_count,
    e.unresolved_path_count,
    e.ambiguous_path_count,
    e.has_paired_pre_release_history,
    e.has_after_only_history,
    e.historical_declaration_count,
    e.has_historical_declaration,
    e.has_exact_target_resolution_observation,
    e.release_capture_count,
    e.historical_capture_count,
    coalesce(c.selected_candidate_count, 0) as candidate_count,
    coalesce(c.selected_candidate_count, 0) > 0 as has_candidate,
    coalesce(c.terminal_review_count, 0) as terminal_review_count,
    coalesce(c.accepted_review_count, 0) as accepted_review_numerator,
    coalesce(c.terminal_review_count, 0) as terminal_review_denominator,
    coalesce(c.rejected_review_count, 0) as rejected_review_count,
    coalesce(c.terminal_review_count, 0) > 0 as reviewed_acceptance_available,
    coalesce(f.selected_finding_count, 0) as finding_count,
    coalesce(f.unknown_finding_count, 0) as unknown_finding_count,
    coalesce(f.bounded_no_finding_count, 0) as bounded_no_finding_count,
    coalesce(f.legacy_unclassified_count, 0) as legacy_unclassified_count,
    coalesce(o.selected_observation_count, 0) as observation_count,
    f.observed_adoption_status,
    f.recovery_signal_status
from {{ ref('bridge_case_repository') }} b
join {{ ref('int_repository_evidence') }} e
    on b.case_version_id = e.case_version_id and b.repository_id = e.repository_id
left join candidates c
    on b.analysis_snapshot_id = c.analysis_snapshot_id
   and b.case_version_id = c.case_version_id and b.repository_id = c.repository_id
left join findings f
    on b.analysis_snapshot_id = f.analysis_snapshot_id
   and b.case_version_id = f.case_version_id and b.repository_id = f.repository_id
left join observations o
    on b.analysis_snapshot_id = o.analysis_snapshot_id
   and b.case_version_id = o.case_version_id and b.repository_id = o.repository_id
