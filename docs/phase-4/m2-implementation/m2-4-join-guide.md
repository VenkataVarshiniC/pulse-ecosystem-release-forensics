# M2.4 join and Power BI relationship guide

Select **one** `analysis_snapshot_id` and its `case_version_id` before an
analytical query. The current snapshot states are DRAFT, so these examples
are for validation only; no Power BI connection or published dataset exists.
Use `bridge_case_repository` or `fct_repository_investigation` for the declared
member denominator. Both preserve all eight members, including repositories
with no candidate or paired history.

Dimension relationships are `dim_case.case_key` and
`dim_repository.repository_key` to their corresponding fact/bridge keys;
`dim_release.release_key` anchors `dim_case.release_key`. The source dimension
uses `source_key` for task, candidate and observation facts. A task's
`repository_key` may be NULL for a shared upstream task. Use one-way
dimension-to-fact filters. Snapshot identity is an additional relationship
and filter component, not a field to omit because case/repository looks
unique today. The support bridge is for drill-through from a selected finding
only; never put it on a counting or denominator path.

Safe candidate acceptance query shape:

```sql
select c.case_name,
       count(*) filter (where f.terminal_review_status = 'ACCEPT') as numerator,
       count(*) filter (where f.has_terminal_review) as denominator,
       count(*) filter (where f.terminal_review_status = 'ACCEPT')::numeric
           / nullif(count(*) filter (where f.has_terminal_review), 0) as rate
from analytics.dim_case c
left join analytics.fct_candidate_review f on c.case_key = f.case_key
    and f.analysis_snapshot_id = :analysis_snapshot_id
group by c.case_name;
```

The pytest result has denominator zero and `rate=NULL`, not 0%. The selected
snapshot must also be checked for `state='PUBLISHED'` before any production
consumer uses it; currently no snapshot meets that filter. Never join task,
candidate, finding and observation facts directly on repository: their
independent one-to-many grains create a Cartesian fan-out. Aggregate each fact
to `(analysis_snapshot_id, case_version_id, repository_id)` first, then left
join the aggregates to the bridge. `fct_repository_investigation` has already
done this for supported diagnostics. Its `candidate_count`, `finding_count`
and `observation_count` reconcile to separate fact aggregates; the dbt
cross-fact test enforces this.

Power BI readiness is **structural only**: four conformed dimensions, explicit
snapshot IDs, one-way filter paths and stable drill-through IDs exist. A
future semantic layer must filter to a single PUBLISHED snapshot, hide raw
UUID/digest fields from headline visuals while retaining them for lineage,
show numerator/denominator and unavailable reason, and avoid bidirectional
fact-to-fact relationships. It must not display adoption, recovery or
stakeholder-success rates from these UNKNOWN outcomes. The source dimension's
one-source-ID grain and snapshot-scoped task fact differ from M2-PREP as
explained in the [analytical model](m2-4-analytical-model.md).
