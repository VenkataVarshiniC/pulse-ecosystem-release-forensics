with ranked_selected_reviews as (
    select
        sr.analysis_snapshot_id,
        r.*,
        row_number() over (
            partition by sr.analysis_snapshot_id, r.candidate_id
            order by r.review_cycle desc, r.review_sequence desc, r.reviewed_at desc, r.review_id desc
        ) as selected_rank
    from {{ source('pulse_core', 'snapshot_review') }} sr
    join {{ ref('stg_pulse__reviews') }} r on sr.review_id = r.review_id
)
select
    s.analysis_snapshot_id,
    s.snapshot_state,
    s.manifest_sha256 as input_manifest_sha256,
    c.case_version_id as case_key,
    c.repository_id as repository_key,
    a.source_id as source_key,
    c.candidate_id,
    c.case_version_id,
    c.repository_id,
    c.artifact_id,
    a.capture_method,
    c.baseline_version,
    c.candidate_rule_id,
    c.candidate_rule_version,
    c.lifecycle_category,
    c.source_origin,
    c.candidate_status,
    c.emitted_at,
    r.review_id as selected_review_id,
    r.review_cycle,
    r.decision as terminal_review_status,
    r.reason_code as terminal_review_reason,
    r.reviewed_at,
    r.decision in ('ACCEPT', 'REJECT') as has_terminal_review,
    r.decision = 'ACCEPT' as accepted_indicator,
    r.decision = 'REJECT' as rejected_indicator,
    r.review_id is null or r.decision = 'NEEDS_EVIDENCE' as unresolved_indicator
from {{ ref('int_analysis_snapshot') }} s
join {{ source('pulse_core', 'snapshot_candidate') }} sc
    on s.analysis_snapshot_id = sc.analysis_snapshot_id
join {{ ref('stg_pulse__candidates') }} c on sc.candidate_id = c.candidate_id
    and s.case_version_id = c.case_version_id
join {{ source('pulse_core', 'snapshot_artifact') }} sa
    on s.analysis_snapshot_id = sa.analysis_snapshot_id and c.artifact_id = sa.artifact_id
join {{ ref('stg_pulse__artifacts') }} a on c.artifact_id = a.artifact_id
left join ranked_selected_reviews r
    on s.analysis_snapshot_id = r.analysis_snapshot_id
   and c.candidate_id = r.candidate_id and r.selected_rank = 1
where a.capture_method <> 'fixture'
