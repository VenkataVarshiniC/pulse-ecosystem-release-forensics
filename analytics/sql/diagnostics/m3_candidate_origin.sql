-- Candidate IDs, review outcomes, and source origin at candidate grain.
select c.target_package as case_name, r.analysis_snapshot_id,
       r.candidate_id, r.repository_id, r.artifact_id,
       r.candidate_rule_id, r.candidate_rule_version,
       r.source_origin, r.terminal_review_status,
       r.terminal_review_reason, r.capture_method
from analytics.fct_candidate_review r
join analytics.dim_case c on r.case_key = c.case_key
join core.analysis_snapshot s on r.analysis_snapshot_id = s.analysis_snapshot_id
where s.state = 'DRAFT' and c.target_package in ('pytest', 'urllib3')
order by c.target_package, r.candidate_id
