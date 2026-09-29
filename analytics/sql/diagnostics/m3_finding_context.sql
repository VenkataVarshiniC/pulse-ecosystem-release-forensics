-- Read-only evidence-state breakdown; one selected finding remains one finding.
select c.target_package as case_name, f.analysis_snapshot_id,
       f.lifecycle_category, f.finding_status,
       f.source_sufficiency_status, f.reason_code,
       count(*)::bigint as finding_count
from analytics.fct_lifecycle_finding f
join analytics.dim_case c on f.case_key = c.case_key
join core.analysis_snapshot s on f.analysis_snapshot_id = s.analysis_snapshot_id
where s.state = 'DRAFT' and c.target_package in ('pytest', 'urllib3')
group by c.target_package, f.analysis_snapshot_id, f.lifecycle_category,
         f.finding_status, f.source_sufficiency_status, f.reason_code
order by c.target_package, f.lifecycle_category, f.finding_status,
         f.source_sufficiency_status, f.reason_code
