select
    historical_pair_id,
    case_version_id,
    repository_id,
    package_name,
    path_ref,
    before_observation_id,
    after_observation_id,
    pair_status,
    pair_version,
    method_version,
    reason
from {{ source('pulse_core', 'historical_pair') }}
