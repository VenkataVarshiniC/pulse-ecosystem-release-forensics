-- Bounded side-by-side validation; different case frames prohibit population effects.
with member_counts as (
    select case_key, analysis_snapshot_id,
           count(*) as members,
           count(*) filter (where core_collection_complete) as collected_members,
           count(*) filter (where has_historical_declaration) as historical_members,
           count(*) filter (where has_paired_pre_release_history) as paired_members,
           count(*) filter (where has_candidate) as candidate_members,
           sum(unknown_finding_count) as unknown_findings
    from analytics.fct_repository_investigation
    group by 1, 2
), candidate_counts as (
    select case_key, analysis_snapshot_id,
           count(*) as candidates,
           count(distinct artifact_id) as candidate_artifacts,
           count(*) filter (where terminal_review_status = 'ACCEPT') as accepted,
           count(*) filter (where terminal_review_status = 'REJECT') as rejected
    from analytics.fct_candidate_review group by 1, 2
), task_counts as (
    select case_key, analysis_snapshot_id,
           count(*) as planned_tasks,
           count(*) filter (where required_flag and terminal_status = 'succeeded')
               as required_succeeded,
           count(*) filter (where required_flag) as required_tasks,
           count(*) filter (where optional_not_found) as optional_not_found
    from analytics.fct_collection_task group by 1, 2
)
select c.case_name, m.analysis_snapshot_id, m.members,
       m.collected_members, m.collected_members::numeric / nullif(m.members,0)
           as collection_coverage,
       m.historical_members, m.historical_members::numeric / nullif(m.members,0)
           as historical_coverage,
       m.paired_members, m.candidate_members,
       coalesce(v.candidates,0) as candidates,
       coalesce(v.candidate_artifacts,0) as candidate_artifacts,
       coalesce(v.accepted,0) as accepted_reviews,
       coalesce(v.rejected,0) as rejected_reviews,
       t.planned_tasks, t.required_succeeded, t.required_tasks,
       t.optional_not_found, m.unknown_findings
from member_counts m
join analytics.dim_case c on m.case_key = c.case_key
left join candidate_counts v
  on m.analysis_snapshot_id = v.analysis_snapshot_id and m.case_key = v.case_key
join task_counts t
  on m.analysis_snapshot_id = t.analysis_snapshot_id and m.case_key = t.case_key
order by c.case_name
