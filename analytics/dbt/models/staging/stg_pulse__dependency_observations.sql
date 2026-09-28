select
    observation_id,
    observation_fingerprint,
    case_version_id,
    repository_id,
    artifact_id,
    observation_type,
    package_name,
    declared_constraint,
    resolved_version,
    repository_ref,
    path_ref,
    observation_time,
    historical_position,
    environment_ref,
    parser_version,
    quality_status
from {{ source('pulse_core', 'dependency_observation') }}
