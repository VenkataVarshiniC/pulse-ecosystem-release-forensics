select distinct
    target_release_id as release_key,
    target_release_id as release_id,
    package_ecosystem,
    target_package as package_name,
    target_version as version,
    release_time,
    release_source_id,
    release_artifact_id
from {{ ref('stg_pulse__cases') }}
