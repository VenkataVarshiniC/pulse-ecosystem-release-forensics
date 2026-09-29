-- The reviewed denominator is candidate IDs with selected terminal review, never artifact IDs.
with selected_candidates as (
    select candidate_id, terminal_review_status, has_terminal_review,
           unresolved_indicator
    from analytics.fct_candidate_review
    where analysis_snapshot_id = %(snapshot_id)s and candidate_status = 'EMITTED'
), counts as (
    select count(*) as emitted_count,
           count(*) filter (where has_terminal_review) as reviewed_count,
           count(*) filter (where terminal_review_status = 'ACCEPT') as accepted_count,
           count(*) filter (where terminal_review_status = 'REJECT') as rejected_count,
           count(*) filter (where unresolved_indicator) as unresolved_count
    from selected_candidates
), metrics as (
    select 'MET-009'::text as metric_id, accepted_count as numerator,
           reviewed_count as denominator from counts
    union all select 'MET-010', rejected_count, reviewed_count from counts
    union all select 'MET-011', unresolved_count, emitted_count from counts
)
select metric_id, numerator, denominator,
       numerator::numeric / nullif(denominator, 0) as metric_value
from metrics
