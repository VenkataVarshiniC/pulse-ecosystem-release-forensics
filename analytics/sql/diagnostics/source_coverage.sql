-- Actual selected captures, not mere source-dimension presence or task planning.
with selected_captures as (
    select s.analysis_snapshot_id, s.case_version_id,
           a.artifact_id, a.source_id, a.repository_id, a.capture_method
    from core.analysis_snapshot s
    join core.snapshot_artifact sa on s.analysis_snapshot_id = sa.analysis_snapshot_id
    join dbt_staging.stg_pulse__artifacts a on sa.artifact_id = a.artifact_id
    where s.analysis_snapshot_id = %(snapshot_id)s
      and a.capture_method <> 'fixture'
)
select c.case_name, sc.analysis_snapshot_id, d.source_id,
       d.provider, d.source_type, d.source_version,
       count(*) as selected_capture_count,
       count(*) filter (where sc.capture_method = 'collector') as collector_count,
       count(*) filter (where sc.capture_method = 'connector_assisted')
           as connector_assisted_count,
       count(distinct sc.repository_id) as repository_count
from selected_captures sc
join analytics.dim_case c on sc.case_version_id = c.case_key
join analytics.dim_evidence_source d on sc.source_id = d.source_key
group by c.case_name, sc.analysis_snapshot_id, d.source_id,
         d.provider, d.source_type, d.source_version
order by d.provider, d.source_type, d.source_id
