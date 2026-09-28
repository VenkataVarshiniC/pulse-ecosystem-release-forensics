with support_counts as (
    select
        finding_id,
        count(*) filter (where support_type = 'artifact') as support_artifact_count,
        count(*) filter (where support_type = 'observation') as support_observation_count,
        count(*) filter (where support_type = 'review') as support_review_count
    from {{ ref('stg_pulse__finding_support') }}
    group by finding_id
)
select
    f.finding_id,
    f.case_version_id,
    f.repository_id,
    f.lifecycle_category,
    f.question_id,
    f.finding_version,
    f.finding_status,
    f.sufficiency_assessment_id,
    s.source_sufficiency_status,
    f.rule_version,
    f.reason_code,
    f.confidence_level,
    f.created_at,
    coalesce(sc.support_artifact_count, 0) as support_artifact_count,
    coalesce(sc.support_observation_count, 0) as support_observation_count,
    coalesce(sc.support_review_count, 0) as support_review_count,
    case
        when f.finding_status <> 'QUALIFYING_EVIDENCE'
            then 'NO_POSITIVE_SUPPORT_CLAIMED'
        when coalesce(sc.support_artifact_count, 0)
           + coalesce(sc.support_observation_count, 0)
           + coalesce(sc.support_review_count, 0) = 0
            then 'MISSING_TYPED_SUPPORT'
        else 'TYPED_SUPPORT_RECORDED_UNVERIFIED'
    end as provenance_status
from {{ ref('stg_pulse__findings') }} f
join {{ ref('int_stage_sufficiency') }} s
    on f.sufficiency_assessment_id = s.assessment_id
left join support_counts sc on f.finding_id = sc.finding_id
