select
    f.analysis_snapshot_id,
    f.snapshot_state,
    f.input_manifest_sha256,
    f.case_version_id as case_key,
    f.repository_id as repository_key,
    f.finding_id,
    e.support_type,
    e.support_id,
    e.support_role,
    case when e.support_type = 'artifact' then e.support_id::uuid end as artifact_id,
    case when e.support_type = 'observation' then e.support_id::uuid end as observation_id,
    case when e.support_type = 'review' then e.support_id::uuid end as review_id
from {{ ref('fct_lifecycle_finding') }} f
join {{ ref('stg_pulse__finding_support') }} e on f.finding_id = e.finding_id
where (e.support_type = 'artifact' and exists (
        select 1 from {{ source('pulse_core', 'snapshot_artifact') }} sa
        where sa.analysis_snapshot_id = f.analysis_snapshot_id
          and sa.artifact_id = e.support_id::uuid
    ))
   or (e.support_type = 'observation' and exists (
        select 1 from {{ ref('fct_evidence_observation') }} o
        where o.analysis_snapshot_id = f.analysis_snapshot_id
          and o.observation_id = e.support_id::uuid
    ))
   or (e.support_type = 'review' and exists (
        select 1 from {{ source('pulse_core', 'snapshot_review') }} sr
        where sr.analysis_snapshot_id = f.analysis_snapshot_id
          and sr.review_id = e.support_id::uuid
    ))
