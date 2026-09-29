select
    s.analysis_snapshot_id,
    s.snapshot_state,
    s.manifest_sha256 as input_manifest_sha256,
    s.model_version as source_snapshot_model_version,
    s.metric_definition_version as source_metric_definition_version,
    case when s.rule_version = 'unrecorded_in_frozen_report'
         then 'm2-4-validation-v1'::text else s.model_version end as mart_model_version,
    m.case_version_id as case_key,
    m.repository_id as repository_key,
    m.case_version_id,
    m.repository_id,
    m.selection_method,
    m.eligibility_status,
    m.selection_rationale,
    m.included_at
from {{ ref('int_analysis_snapshot') }} s
join {{ ref('int_case_repository') }} m on s.case_version_id = m.case_version_id
