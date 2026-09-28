with selected_support as (
    select analysis_snapshot_id, finding_id, count(*) as selected_edge_count
    from {{ ref('bridge_finding_evidence') }}
    group by 1, 2
), rejected_support as (
    select b.analysis_snapshot_id, b.finding_id, count(*) as rejected_edge_count
    from {{ ref('bridge_finding_evidence') }} b
    join {{ ref('stg_pulse__reviews') }} r on b.review_id = r.review_id
    where b.support_type = 'review' and r.decision <> 'ACCEPT'
    group by 1, 2
)
select f.analysis_snapshot_id, f.finding_id
from {{ ref('fct_lifecycle_finding') }} f
left join selected_support s
    on f.analysis_snapshot_id = s.analysis_snapshot_id and f.finding_id = s.finding_id
left join rejected_support r
    on f.analysis_snapshot_id = r.analysis_snapshot_id and f.finding_id = r.finding_id
where f.finding_status = 'QUALIFYING_EVIDENCE'
  and (coalesce(s.selected_edge_count, 0) = 0
       or coalesce(r.rejected_edge_count, 0) > 0
       or f.provenance_status <> 'TYPED_SUPPORT_RECORDED_UNVERIFIED')
