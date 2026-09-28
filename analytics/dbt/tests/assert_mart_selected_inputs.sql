with unselected_task as (
    select 'task' as input_type, t.analysis_snapshot_id, t.collection_task_id as input_id
    from {{ ref('fct_collection_task') }} t
    left join {{ source('pulse_core', 'snapshot_run') }} sr
        on t.analysis_snapshot_id = sr.analysis_snapshot_id
       and t.collection_run_id = sr.collection_run_id
    where sr.collection_run_id is null
), unselected_candidate as (
    select 'candidate' as input_type, c.analysis_snapshot_id, c.candidate_id as input_id
    from {{ ref('fct_candidate_review') }} c
    left join {{ source('pulse_core', 'snapshot_candidate') }} sc
        on c.analysis_snapshot_id = sc.analysis_snapshot_id and c.candidate_id = sc.candidate_id
    where sc.candidate_id is null
), unselected_review as (
    select 'review' as input_type, c.analysis_snapshot_id, c.selected_review_id as input_id
    from {{ ref('fct_candidate_review') }} c
    left join {{ source('pulse_core', 'snapshot_review') }} sr
        on c.analysis_snapshot_id = sr.analysis_snapshot_id
       and c.selected_review_id = sr.review_id
    where c.selected_review_id is not null and sr.review_id is null
), unselected_finding as (
    select 'finding' as input_type, f.analysis_snapshot_id, f.finding_id as input_id
    from {{ ref('fct_lifecycle_finding') }} f
    left join {{ source('pulse_core', 'snapshot_finding') }} sf
        on f.analysis_snapshot_id = sf.analysis_snapshot_id and f.finding_id = sf.finding_id
    where sf.finding_id is null
), unselected_assessment as (
    select 'assessment' as input_type, f.analysis_snapshot_id, f.assessment_id as input_id
    from {{ ref('fct_lifecycle_finding') }} f
    left join {{ source('pulse_core', 'snapshot_assessment') }} sa
        on f.analysis_snapshot_id = sa.analysis_snapshot_id and f.assessment_id = sa.assessment_id
    where sa.assessment_id is null
), unselected_observation_artifact as (
    select 'observation_artifact' as input_type, o.analysis_snapshot_id, o.artifact_id as input_id
    from {{ ref('fct_evidence_observation') }} o
    left join {{ source('pulse_core', 'snapshot_artifact') }} sa
        on o.analysis_snapshot_id = sa.analysis_snapshot_id and o.artifact_id = sa.artifact_id
    where sa.artifact_id is null
)
select * from unselected_task
union all select * from unselected_candidate
union all select * from unselected_review
union all select * from unselected_finding
union all select * from unselected_assessment
union all select * from unselected_observation_artifact
