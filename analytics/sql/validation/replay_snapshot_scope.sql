-- Each core snapshot belongs to one case. The release groups the two replay cases.
select c.target_package as case_name, s.case_version_id, s.analysis_snapshot_id,
       s.state as snapshot_state, s.rule_version, l.case_id, l.release_id,
       l.replay_artifact_sha256, l.metric_contract_version, l.metric_registry_sha256
from core.replay_snapshot_lineage l
join core.analysis_snapshot s using (analysis_snapshot_id)
join analytics.dim_case c on s.case_version_id = c.case_key
where l.rule_release_id = 'rule-replay-b2b638bb97c8-e10fb03f467e267f'
order by l.case_id
