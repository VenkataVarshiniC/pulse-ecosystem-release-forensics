-- Branches have different grains. F3/F4 remain category-specific, not summed as members.
with members as (
    select * from analytics.fct_repository_investigation
    where analysis_snapshot_id = %(snapshot_id)s
), candidates as (
    select * from analytics.fct_candidate_review
    where analysis_snapshot_id = %(snapshot_id)s and candidate_status = 'EMITTED'
), findings as (
    select * from analytics.fct_lifecycle_finding
    where analysis_snapshot_id = %(snapshot_id)s
), root as (
    select count(*) as members from members
)
select 'F0_DECLARED'::text as step, null::text as category,
       members::bigint as numerator, members::bigint as denominator,
       'members'::text as unit from root
union all
select 'F1_CORE_COLLECTED', null,
       (select count(*) from members where core_collection_complete), members, 'members' from root
union all
select 'F2_CONTEXT_DECLARATION', null,
       (select count(*) from members where has_historical_declaration), members, 'members' from root
union all
select 'F2_PAIRED_SUBCOUNT', null,
       (select count(*) from members where has_paired_pre_release_history), members, 'members'
from root
union all
select 'B1_CANDIDATE_MEMBERS', null,
       (select count(*) from members where has_candidate), members, 'members' from root
union all
select 'B1_CANDIDATE_IDS', null,
       (select count(*) from candidates), null::bigint, 'candidate_ids'
union all
select 'B2_TERMINAL_REVIEW', null,
       (select count(*) from candidates where has_terminal_review),
       (select count(*) from candidates), 'candidate_ids'
union all
select 'B3_ACCEPTED', null,
       (select count(*) from candidates where terminal_review_status = 'ACCEPT'),
       (select count(*) from candidates where has_terminal_review), 'candidate_ids'
union all
select 'F3_STAGE_SUFFICIENT', lifecycle_category,
       count(*) filter (where source_sufficiency_status = 'SUFFICIENT'),
       count(*), 'member_stage_pairs' from findings group by lifecycle_category
union all
select 'F4_BOUNDED_FINDING', lifecycle_category,
       count(*) filter (where finding_status <> 'UNKNOWN'),
       count(*), 'member_stage_pairs' from findings group by lifecycle_category
union all
select 'F5_REPOSITORY_OUTCOME', null, null::bigint, members, 'members' from root
