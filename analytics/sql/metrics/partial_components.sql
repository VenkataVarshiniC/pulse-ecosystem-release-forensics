-- Components are descriptive counts. They are not the governed partial metric rate.
with selected_tasks as (
    select required_flag, terminal_status from analytics.fct_collection_task
    where analysis_snapshot_id = %(snapshot_id)s
), selected_findings as (
    select finding_status, source_sufficiency_status
    from analytics.fct_lifecycle_finding
    where analysis_snapshot_id = %(snapshot_id)s
), components as (
    select 'MET-004'::text as metric_id,
           (select count(*) from selected_tasks
             where required_flag and terminal_status = 'succeeded') as observed_numerator,
           (select count(*) from selected_tasks where required_flag) as observed_denominator,
           'overall required tasks; no stage-source map'::text as component_scope
    union all select 'MET-005',
           (select count(*) from selected_findings
             where source_sufficiency_status = 'SUFFICIENT'),
           (select count(*) from selected_findings),
           'reported assessments; 38 legacy statuses retained'
    union all select 'MET-012',
           (select count(*) from selected_findings where finding_status = 'UNKNOWN'),
           (select count(*) from selected_findings),
           'reported categories; required stakeholder question set absent'
    union all select 'MET-013', null::bigint,
           (select count(*) from selected_findings where finding_status = 'UNKNOWN'),
           'UNKNOWN count only; controlled reason numerator unavailable'
    union all select 'MET-015', null::bigint,
           (select count(*) from selected_findings where finding_status = 'UNKNOWN'),
           'UNKNOWN count only; missing required source attribution unavailable'
    union all select 'MET-019', null::bigint, null::bigint,
           'no documented resumed run in these cases'
    union all select 'MET-020', null::bigint, null::bigint,
           'source replay audit exists but no governed replay mart'
)
select * from components
