select
    a.artifact_id,
    a.capture_fingerprint,
    a.source_id,
    s.provider as source_provider,
    s.source_type,
    s.source_version,
    a.repository_id,
    a.collection_task_id,
    a.history_run_id,
    a.source_task_key,
    a.source_attempt_key,
    a.artifact_type,
    a.source_locator,
    a.repository_ref,
    a.source_event_time,
    a.retrieved_at,
    a.capture_method,
    a.content_sha256,
    a.raw_snapshot_uri,
    a.media_type,
    a.parser_version
from {{ source('pulse_core', 'evidence_artifact') }} a
join {{ source('pulse_ingestion', 'source_registry') }} s
    on a.source_id = s.source_id
