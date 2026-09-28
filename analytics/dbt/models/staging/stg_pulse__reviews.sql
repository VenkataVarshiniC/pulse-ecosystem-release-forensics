select
    review_id,
    candidate_id,
    review_cycle,
    review_sequence,
    reviewer_identity,
    decision,
    reason_code,
    review_note,
    reviewed_at
from {{ source('pulse_core', 'analyst_review') }}
