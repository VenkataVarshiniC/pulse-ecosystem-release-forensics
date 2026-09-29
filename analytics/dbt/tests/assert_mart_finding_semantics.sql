with shape as (
    select s.rule_version, count(f.finding_id) as findings,
           count(*) filter (where finding_status = 'UNKNOWN') as unknown_count,
           count(*) filter (where finding_status = 'NO_QUALIFYING_EVIDENCE_FOUND')
               as bounded_no_count,
           count(*) filter (where finding_status = 'QUALIFYING_EVIDENCE') as positive_count,
           count(*) filter (where source_sufficiency_status = 'SUFFICIENT') as sufficient_count,
           count(*) filter (where source_sufficiency_status = 'LEGACY_UNCLASSIFIED')
               as legacy_count,
           count(*) filter (where source_sufficiency_status = 'INSUFFICIENT')
               as insufficient_count
    from {{ ref('int_analysis_snapshot') }} s
    left join {{ ref('fct_lifecycle_finding') }} f
        on s.analysis_snapshot_id = f.analysis_snapshot_id
    group by s.rule_version
), adoption_recovery as (
    select s.rule_version, count(*) as members,
           count(*) filter (where observed_adoption_status = 'UNKNOWN') as adoption_unknown,
           count(*) filter (where recovery_signal_status = 'UNKNOWN') as recovery_unknown
    from {{ ref('fct_repository_investigation') }} r
    join {{ ref('int_analysis_snapshot') }} s
        on r.analysis_snapshot_id = s.analysis_snapshot_id
    group by s.rule_version
)
select 'frozen_finding_shape' as failure from shape
where findings <> 40 or unknown_count <> 38 or bounded_no_count <> 2
   or positive_count <> 0 or sufficient_count <> 2
   or (rule_version = 'unrecorded_in_frozen_report' and
       (legacy_count <> 38 or insufficient_count <> 0))
   or (rule_version <> 'unrecorded_in_frozen_report' and
       (legacy_count <> 0 or insufficient_count <> 38))
union all
select 'adoption_recovery_unknown' from adoption_recovery
where members <> 8 or adoption_unknown <> 8 or recovery_unknown <> 8
union all
select 'legacy_reclassification' from {{ ref('fct_lifecycle_finding') }}
where (source_sufficiency_status = 'LEGACY_UNCLASSIFIED'
       and analytical_status_family <> 'UNRESOLVED_LEGACY')
   or (finding_status = 'UNKNOWN' and provenance_status <> 'NO_POSITIVE_SUPPORT_CLAIMED')
union all
select 'member_finding_set' from {{ ref('fct_repository_investigation') }}
where finding_count <> 5
