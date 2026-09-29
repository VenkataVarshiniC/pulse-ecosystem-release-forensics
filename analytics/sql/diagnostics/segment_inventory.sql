-- Inventory only; readiness decisions account for tiny or missing cells in documentation.
with members as (
    select r.analysis_snapshot_id, r.repository_id, c.case_name,
           d.provider, r.has_paired_pre_release_history,
           r.has_after_only_history, r.has_candidate,
           r.core_collection_complete
    from analytics.fct_repository_investigation r
    join analytics.dim_case c on r.case_key = c.case_key
    join analytics.dim_repository d on r.repository_key = d.repository_key
), cells as (
    select 'case'::text as dimension, case_name as segment, count(*) as member_count
    from members group by case_name
    union all select 'repository_provider', provider, count(*) from members group by provider
    union all select 'paired_history', has_paired_pre_release_history::text,
        count(*) from members group by has_paired_pre_release_history
    union all select 'after_only_history', has_after_only_history::text,
        count(*) from members group by has_after_only_history
    union all select 'candidate_presence', has_candidate::text,
        count(*) from members group by has_candidate
    union all select 'core_collection', core_collection_complete::text,
        count(*) from members group by core_collection_complete
)
select dimension, segment, member_count from cells order by dimension, segment
