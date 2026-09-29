-- Case-local member denominators start from the frozen bridge, including zero-candidate members.
with member_spine as (
    select b.analysis_snapshot_id, b.case_version_id, b.repository_id,
           r.core_collection_complete, r.has_historical_declaration,
           r.has_candidate, r.candidate_count
    from analytics.bridge_case_repository b
    join analytics.fct_repository_investigation r
      on b.analysis_snapshot_id = r.analysis_snapshot_id
     and b.case_version_id = r.case_version_id
     and b.repository_id = r.repository_id
    where b.analysis_snapshot_id = %(snapshot_id)s
), counts as (
    select count(*) as member_count,
           count(*) filter (where core_collection_complete) as collected_count,
           count(*) filter (where has_historical_declaration) as historical_count,
           count(*) filter (where has_candidate) as emitting_member_count,
           coalesce(sum(candidate_count), 0) as emitted_candidate_count
    from member_spine
), metrics as (
    select 'MET-001'::text as metric_id, collected_count as numerator,
           member_count as denominator from counts
    union all select 'MET-002', historical_count, member_count from counts
    union all select 'MET-008', emitting_member_count, member_count from counts
    union all select 'MET-022', emitted_candidate_count, member_count from counts
)
select metric_id, numerator::bigint as numerator, denominator::bigint as denominator,
       numerator::numeric / nullif(denominator, 0) as metric_value
from metrics
