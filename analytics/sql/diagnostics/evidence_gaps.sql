-- Every declared member remains visible, including those with no candidate or paired path.
select c.case_name, r.analysis_snapshot_id, r.repository_id,
       d.canonical_full_name,
       r.core_collection_complete,
       r.has_historical_declaration,
       r.has_paired_pre_release_history,
       r.after_only_path_count,
       r.unresolved_path_count,
       r.candidate_count,
       r.terminal_review_count,
       r.unknown_finding_count,
       r.bounded_no_finding_count,
       r.legacy_unclassified_count,
       r.observed_adoption_status,
       r.recovery_signal_status
from analytics.bridge_case_repository b
join analytics.fct_repository_investigation r
  on b.analysis_snapshot_id = r.analysis_snapshot_id
 and b.case_version_id = r.case_version_id
 and b.repository_id = r.repository_id
join analytics.dim_case c on b.case_key = c.case_key
join analytics.dim_repository d on b.repository_key = d.repository_key
where b.analysis_snapshot_id = %(snapshot_id)s
order by d.canonical_full_name, r.repository_id
