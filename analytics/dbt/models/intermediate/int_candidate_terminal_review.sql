with ranked_review as (
    select
        r.*,
        row_number() over (
            partition by candidate_id
            order by review_cycle desc, review_sequence desc, reviewed_at desc, review_id desc
        ) as review_rank
    from {{ ref('stg_pulse__reviews') }} r
)
select
    c.candidate_id,
    c.case_version_id,
    c.repository_id,
    c.artifact_id,
    c.candidate_rule_id,
    c.candidate_rule_version,
    c.lifecycle_category,
    c.source_origin,
    c.emitted_at,
    c.candidate_status,
    r.review_id as selected_review_id,
    r.review_cycle,
    r.review_sequence,
    r.decision as latest_review_decision,
    r.reason_code as latest_review_reason_code,
    r.reviewed_at,
    r.decision in ('ACCEPT', 'REJECT') as has_terminal_review,
    r.decision = 'ACCEPT' as has_accepted_review
from {{ ref('stg_pulse__candidates') }} c
left join ranked_review r
    on c.candidate_id = r.candidate_id and r.review_rank = 1
