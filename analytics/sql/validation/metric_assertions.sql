-- Zero rows means every frozen denominator and evidence-boundary invariant holds.
with member_counts as (
    select case_key, analysis_snapshot_id, count(*) as members,
           count(*) filter (where core_collection_complete) as core_members,
           count(*) filter (where has_historical_declaration) as historical_members,
           count(*) filter (where has_paired_pre_release_history) as paired_members,
           coalesce(sum(after_only_path_count),0) as after_only_paths,
           count(*) filter (where has_candidate) as candidate_members,
           coalesce(sum(candidate_count),0) as candidate_ids,
           coalesce(sum(unknown_finding_count),0) as unknown_findings,
           coalesce(sum(bounded_no_finding_count),0) as bounded_no_findings,
           coalesce(sum(legacy_unclassified_count),0) as legacy_findings,
           count(*) filter (where observed_adoption_status <> 'UNKNOWN'
                              or recovery_signal_status <> 'UNKNOWN') as false_outcomes
    from analytics.fct_repository_investigation
    where analysis_snapshot_id in (
        select analysis_snapshot_id from core.analysis_snapshot
        where rule_version = 'unrecorded_in_frozen_report')
    group by 1,2
), candidate_counts as (
    select case_key, analysis_snapshot_id, count(*) as emitted,
           count(distinct artifact_id) as artifacts,
           count(*) filter (where has_terminal_review) as reviewed,
           count(*) filter (where terminal_review_status = 'ACCEPT') as accepted,
           count(*) filter (where terminal_review_status = 'REJECT') as rejected,
           count(*) filter (where capture_method = 'fixture') as fixtures
    from analytics.fct_candidate_review
    where analysis_snapshot_id in (
        select analysis_snapshot_id from core.analysis_snapshot
        where rule_version = 'unrecorded_in_frozen_report')
    group by 1,2
), task_counts as (
    select case_key, analysis_snapshot_id, count(*) as tasks,
           count(*) filter (where required_flag) as required_tasks,
           count(*) filter (where required_flag and terminal_status = 'succeeded')
               as required_success,
           count(*) filter (where not required_flag) as optional_tasks,
           count(*) filter (where optional_not_found) as optional_not_found,
           count(*) filter (where retry_count > 0) as retried
    from analytics.fct_collection_task
    where analysis_snapshot_id in (
        select analysis_snapshot_id from core.analysis_snapshot
        where rule_version = 'unrecorded_in_frozen_report')
    group by 1,2
), actual as (
    select c.target_package as case_name, m.analysis_snapshot_id, m.members, m.core_members,
           m.historical_members, m.paired_members, m.after_only_paths,
           m.candidate_members, m.candidate_ids, m.unknown_findings,
           m.bounded_no_findings, m.legacy_findings, m.false_outcomes,
           coalesce(v.emitted,0) as emitted, coalesce(v.artifacts,0) as artifacts,
           coalesce(v.reviewed,0) as reviewed, coalesce(v.accepted,0) as accepted,
           coalesce(v.rejected,0) as rejected, coalesce(v.fixtures,0) as fixtures,
           t.tasks, t.required_tasks, t.required_success, t.optional_tasks,
           t.optional_not_found, t.retried
    from member_counts m
    join analytics.dim_case c on m.case_key = c.case_key
    join task_counts t on m.case_key = t.case_key
      and m.analysis_snapshot_id = t.analysis_snapshot_id
    left join candidate_counts v on m.case_key = v.case_key
      and m.analysis_snapshot_id = v.analysis_snapshot_id
), expected as (
    select * from (values
       ('pytest', 2,2,1,1,1,0,0,8,2,8,0,0,0,0,0,0,0,15,11,11,4,1,0),
       ('urllib3',6,6,1,0,5,1,2,30,0,30,0,2,1,2,0,2,0,39,27,27,12,5,0)
    ) as e(case_name,members,core_members,historical_members,paired_members,
       after_only_paths,candidate_members,candidate_ids,unknown_findings,
       bounded_no_findings,legacy_findings,false_outcomes,emitted,artifacts,
       reviewed,accepted,rejected,fixtures,tasks,required_tasks,required_success,
       optional_tasks,optional_not_found,retried)
), comparisons as (
    select e.case_name, a.analysis_snapshot_id,
           row(a.members,a.core_members,a.historical_members,a.paired_members,
               a.after_only_paths,a.candidate_members,a.candidate_ids,a.unknown_findings,
               a.bounded_no_findings,a.legacy_findings,a.false_outcomes,
               a.emitted,a.artifacts,a.reviewed,a.accepted,a.rejected,a.fixtures,
               a.tasks,a.required_tasks,a.required_success,a.optional_tasks,
               a.optional_not_found,a.retried) is distinct from
           row(e.members,e.core_members,e.historical_members,e.paired_members,
               e.after_only_paths,e.candidate_members,e.candidate_ids,e.unknown_findings,
               e.bounded_no_findings,e.legacy_findings,e.false_outcomes,
               e.emitted,e.artifacts,e.reviewed,e.accepted,e.rejected,e.fixtures,
               e.tasks,e.required_tasks,e.required_success,e.optional_tasks,
               e.optional_not_found,e.retried) as mismatch
    from expected e left join actual a on e.case_name = a.case_name
)
select case_name, analysis_snapshot_id, 'frozen count mismatch or missing case' as issue
from comparisons where mismatch or analysis_snapshot_id is null
union all
select a.case_name, a.analysis_snapshot_id, 'unexpected case or duplicate snapshot'
from actual a
where a.case_name not in (select case_name from expected)
   or (select count(*) from actual b where b.case_name = a.case_name) <> 1
union all
select c.target_package, sa.analysis_snapshot_id, 'fixture artifact selected'
from core.snapshot_artifact sa
join core.analysis_snapshot s on sa.analysis_snapshot_id = s.analysis_snapshot_id
join analytics.dim_case c on s.case_version_id = c.case_key
join dbt_staging.stg_pulse__artifacts a on sa.artifact_id = a.artifact_id
where a.capture_method = 'fixture'
union all
select c.target_package, o.analysis_snapshot_id, 'fixture observation in mart'
from analytics.fct_evidence_observation o
join analytics.dim_case c on o.case_key = c.case_key
where o.capture_method = 'fixture'
