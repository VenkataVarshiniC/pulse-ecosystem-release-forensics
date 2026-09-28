with pair_counts as (
    select
        case_version_id,
        repository_id,
        count(*) filter (where pair_status = 'PAIRED') as paired_count,
        count(*) filter (where pair_status = 'AFTER_ONLY') as after_only_count,
        count(*) filter (where pair_status = 'UNRESOLVED') as unresolved_count
    from {{ source('pulse_core', 'historical_pair') }}
    group by 1, 2
)
select e.case_version_id, e.repository_id
from {{ ref('int_repository_evidence') }} e
left join pair_counts p
    on e.case_version_id = p.case_version_id and e.repository_id = p.repository_id
where e.paired_path_count <> coalesce(p.paired_count, 0)
   or e.after_only_path_count <> coalesce(p.after_only_count, 0)
   or e.unresolved_path_count <> coalesce(p.unresolved_count, 0)
   or e.has_paired_pre_release_history <> (coalesce(p.paired_count, 0) > 0)
   or e.has_after_only_history <> (coalesce(p.after_only_count, 0) > 0)
union all
select p.case_version_id, p.repository_id
from {{ ref('stg_pulse__historical_pairs') }} p
where p.pair_status = 'AFTER_ONLY' and p.before_observation_id is not null
