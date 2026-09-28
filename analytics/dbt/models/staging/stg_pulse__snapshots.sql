select
    analysis_snapshot_id,
    case_version_id,
    source_plan_version,
    rule_version,
    metric_definition_version,
    model_version,
    loader_version,
    generated_at,
    state as snapshot_state,
    manifest_sha256,
    supersedes_snapshot_id
from {{ source('pulse_core', 'analysis_snapshot') }}
