select
    s.analysis_snapshot_id,
    s.snapshot_state,
    s.manifest_sha256 as input_manifest_sha256,
    o.case_version_id as case_key,
    o.repository_id as repository_key,
    a.source_id as source_key,
    o.observation_id,
    o.case_version_id,
    o.repository_id,
    o.artifact_id,
    o.observation_type,
    o.package_name,
    o.declared_constraint,
    o.resolved_version,
    o.repository_ref,
    o.path_ref,
    o.historical_position,
    o.observation_time,
    a.source_event_time,
    a.retrieved_at,
    a.capture_method,
    o.parser_version,
    o.quality_status
from {{ ref('int_analysis_snapshot') }} s
join {{ source('pulse_core', 'snapshot_artifact') }} sa
    on s.analysis_snapshot_id = sa.analysis_snapshot_id
join {{ ref('stg_pulse__artifacts') }} a on sa.artifact_id = a.artifact_id
join {{ ref('stg_pulse__dependency_observations') }} o
    on a.artifact_id = o.artifact_id and s.case_version_id = o.case_version_id
where a.capture_method <> 'fixture'
