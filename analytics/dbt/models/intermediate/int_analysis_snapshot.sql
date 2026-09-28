with run_inputs as (
    select analysis_snapshot_id, count(*) as selected_run_count
    from {{ source('pulse_core', 'snapshot_run') }} group by analysis_snapshot_id
),
artifact_inputs as (
    select
        sa.analysis_snapshot_id,
        count(*) as selected_artifact_count,
        count(*) filter (where a.artifact_id is null or sa.expected_sha256 <> a.content_sha256)
            as artifact_digest_mismatch_count
    from {{ source('pulse_core', 'snapshot_artifact') }} sa
    left join {{ ref('stg_pulse__artifacts') }} a on sa.artifact_id = a.artifact_id
    group by sa.analysis_snapshot_id
),
candidate_inputs as (
    select analysis_snapshot_id, count(*) as selected_candidate_count
    from {{ source('pulse_core', 'snapshot_candidate') }} group by analysis_snapshot_id
),
review_inputs as (
    select analysis_snapshot_id, count(*) as selected_review_count
    from {{ source('pulse_core', 'snapshot_review') }} group by analysis_snapshot_id
),
assessment_inputs as (
    select analysis_snapshot_id, count(*) as selected_assessment_count
    from {{ source('pulse_core', 'snapshot_assessment') }} group by analysis_snapshot_id
),
finding_inputs as (
    select analysis_snapshot_id, count(*) as selected_finding_count
    from {{ source('pulse_core', 'snapshot_finding') }} group by analysis_snapshot_id
)
select
    s.*,
    coalesce(r.selected_run_count, 0) as selected_run_count,
    coalesce(a.selected_artifact_count, 0) as selected_artifact_count,
    coalesce(a.artifact_digest_mismatch_count, 0) as artifact_digest_mismatch_count,
    coalesce(c.selected_candidate_count, 0) as selected_candidate_count,
    coalesce(v.selected_review_count, 0) as selected_review_count,
    coalesce(q.selected_assessment_count, 0) as selected_assessment_count,
    coalesce(f.selected_finding_count, 0) as selected_finding_count
from {{ ref('stg_pulse__snapshots') }} s
left join run_inputs r on s.analysis_snapshot_id = r.analysis_snapshot_id
left join artifact_inputs a on s.analysis_snapshot_id = a.analysis_snapshot_id
left join candidate_inputs c on s.analysis_snapshot_id = c.analysis_snapshot_id
left join review_inputs v on s.analysis_snapshot_id = v.analysis_snapshot_id
left join assessment_inputs q on s.analysis_snapshot_id = q.analysis_snapshot_id
left join finding_inputs f on s.analysis_snapshot_id = f.analysis_snapshot_id
