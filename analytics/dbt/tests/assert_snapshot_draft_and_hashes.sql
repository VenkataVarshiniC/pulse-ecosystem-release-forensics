select s.analysis_snapshot_id
from {{ ref('int_analysis_snapshot') }} s
join {{ source('pulse_core', 'analysis_snapshot') }} raw
    on s.analysis_snapshot_id = raw.analysis_snapshot_id
where s.snapshot_state is distinct from raw.state
   or s.snapshot_state <> 'DRAFT'
   or s.artifact_digest_mismatch_count <> 0
   or s.manifest_sha256 is distinct from raw.manifest_sha256
