select
    s.analysis_snapshot_id,
    s.snapshot_state,
    s.manifest_sha256 as input_manifest_sha256,
    f.case_version_id as case_key,
    f.repository_id as repository_key,
    f.finding_id,
    f.case_version_id,
    f.repository_id,
    f.lifecycle_category,
    f.question_id,
    f.finding_version,
    f.finding_status,
    f.sufficiency_assessment_id as assessment_id,
    f.source_sufficiency_status,
    q.analytical_status_family,
    q.required_source_set_version,
    f.confidence_level,
    f.reason_code,
    f.support_artifact_count,
    f.support_observation_count,
    f.support_review_count,
    f.provenance_status,
    f.rule_version
from {{ ref('int_analysis_snapshot') }} s
join {{ source('pulse_core', 'snapshot_finding') }} sf
    on s.analysis_snapshot_id = sf.analysis_snapshot_id
join {{ ref('int_finding_evidence') }} f
    on sf.finding_id = f.finding_id and s.case_version_id = f.case_version_id
join {{ source('pulse_core', 'snapshot_assessment') }} sa
    on s.analysis_snapshot_id = sa.analysis_snapshot_id
   and f.sufficiency_assessment_id = sa.assessment_id
join {{ ref('int_stage_sufficiency') }} q on f.sufficiency_assessment_id = q.assessment_id
