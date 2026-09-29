-- Required success, optional 404 and actual retries use three different task denominators.
with selected_tasks as (
    select collection_task_id, required_flag, terminal_status,
           actual_attempt_count, retry_count
    from analytics.fct_collection_task
    where analysis_snapshot_id = %(snapshot_id)s
), counts as (
    select count(*) filter (where required_flag) as required_count,
           count(*) filter (where required_flag and terminal_status = 'succeeded'
                                     and actual_attempt_count > 0) as required_succeeded,
           count(*) filter (where not required_flag and actual_attempt_count > 0
                             and terminal_status <> 'pending') as optional_terminal_count,
           count(*) filter (where not required_flag and terminal_status = 'not_found'
                                     and actual_attempt_count > 0) as optional_not_found,
           count(*) filter (where actual_attempt_count > 0) as attempted_count,
           count(*) filter (where actual_attempt_count > 0 and retry_count > 0)
               as retried_count
    from selected_tasks
), metrics as (
    select 'MET-016'::text as metric_id, required_succeeded as numerator,
           required_count as denominator from counts
    union all select 'MET-017', optional_not_found, optional_terminal_count from counts
    union all select 'MET-018', retried_count, attempted_count from counts
)
select metric_id, numerator, denominator,
       numerator::numeric / nullif(denominator, 0) as metric_value
from metrics
