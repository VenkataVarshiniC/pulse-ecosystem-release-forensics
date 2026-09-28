with task_counts as (
    select analysis_snapshot_id, case_version_id, repository_id, count(*) as task_count
    from {{ ref('fct_collection_task') }} where repository_id is not null
    group by 1, 2, 3
), candidate_counts as (
    select analysis_snapshot_id, case_version_id, repository_id,
           count(*) as candidate_count,
           count(*) filter (where has_terminal_review) as review_count
    from {{ ref('fct_candidate_review') }} group by 1, 2, 3
), finding_counts as (
    select analysis_snapshot_id, case_version_id, repository_id,
           count(*) as finding_count,
           count(*) filter (where finding_status = 'UNKNOWN') as unknown_count
    from {{ ref('fct_lifecycle_finding') }} group by 1, 2, 3
), observation_counts as (
    select analysis_snapshot_id, case_version_id, repository_id,
           count(*) as observation_count
    from {{ ref('fct_evidence_observation') }} group by 1, 2, 3
)
select r.analysis_snapshot_id, r.case_version_id, r.repository_id
from {{ ref('fct_repository_investigation') }} r
left join task_counts t using (analysis_snapshot_id, case_version_id, repository_id)
left join candidate_counts c using (analysis_snapshot_id, case_version_id, repository_id)
left join finding_counts f using (analysis_snapshot_id, case_version_id, repository_id)
left join observation_counts o using (analysis_snapshot_id, case_version_id, repository_id)
where r.planned_member_task_count <> coalesce(t.task_count, 0)
   or r.candidate_count <> coalesce(c.candidate_count, 0)
   or r.terminal_review_count <> coalesce(c.review_count, 0)
   or r.finding_count <> coalesce(f.finding_count, 0)
   or r.unknown_finding_count <> coalesce(f.unknown_count, 0)
   or r.observation_count <> coalesce(o.observation_count, 0)
