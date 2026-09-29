select analysis_snapshot_id
from {{ ref('int_analysis_snapshot') }}
where snapshot_state in ('VALIDATED', 'PUBLISHED', 'PUBLISHED_VALIDATION')
  and (rule_version in ('unrecorded_in_frozen_report', 'unknown', '')
       or metric_definition_version in ('not_yet_modeled', 'unknown', '')
       or model_version in ('postgres-core-v4', 'not_yet_modeled', 'unknown', '')
       or artifact_digest_mismatch_count <> 0)
union all
select analysis_snapshot_id
from {{ ref('int_analysis_snapshot') }}
where snapshot_state in ('PUBLISHED', 'PUBLISHED_VALIDATION')
  and (selected_run_count = 0 or selected_artifact_count = 0
       or selected_assessment_count = 0 or selected_finding_count = 0)
