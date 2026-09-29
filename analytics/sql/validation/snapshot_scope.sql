-- The two selected DRAFT snapshots are the only governed M2.5 validation scope.
select c.target_package as case_name, s.case_version_id, s.analysis_snapshot_id,
       s.state as snapshot_state, s.manifest_sha256,
       s.rule_version, s.metric_definition_version, s.model_version
from core.analysis_snapshot s
join analytics.dim_case c on s.case_version_id = c.case_key
where c.target_package in ('pytest', 'urllib3')
order by c.target_package, s.analysis_snapshot_id
