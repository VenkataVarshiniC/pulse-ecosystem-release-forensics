# Proposed Power BI semantic and measure contract

No connection, PBIX or DAX is built. Audience, dashboard priority, refresh, RLS and distribution await stakeholder/security reconciliation. The future model consumes **published governed analytics marts**, never raw snapshots directly. One case/version/snapshot slicer is mandatory; default to one published snapshot per selected case. Display N/D and unavailable reason next to every rate.

| Relationship | Cardinality / direction | Use |
| --- | --- | --- |
| dim_case → bridge_case_repository → dim_repository | 1:m then m:1, controlled one-way filtering through bridge | Declared member list; avoid global bidirectional many-to-many. |
| dim_case/dim_repository/dim_release → fct_repository_investigation | 1:m, dimension-to-fact single direction | Member coverage; release via case where possible. |
| dim_case/dim_repository/dim_evidence_source → fct_collection_task | 1:m, single direction; task snapshot-use bridge only in explicit views | Operational coverage, required/optional tasks. |
| dim_case/dim_repository → fct_candidate_review | 1:m, single direction | Candidate dispositions at candidate grain. |
| dim_case/dim_repository → fct_lifecycle_finding | 1:m, single direction | Stage/category status at selected version. |
| dim_case/dim_repository → fct_evidence_observation | 1:m, single direction | Exact-ref context, separate declaration/resolution. |
| fct_lifecycle_finding → bridge_finding_evidence → source artifact detail | 1:m drill-through path, not a measure filter path | Trace support chain without inflating finding counts. |

Snapshot ID is a shared filter and composite relationship component; do not join two facts directly on repository or artifact. Hide UUIDs/digests from main visuals but keep them as drill-through keys. Show package/version, repository label, category, source/method, status and reason as display fields. Artifact detail displays original locator, digest, capture method, event versus retrieval time, and whether the source is connector-assisted/fixture. Do not expose credentials or unnecessary personal identifiers. Human disposition is absent.

Governed dbt marts own eligibility, missingness, status, numerator/denominator and version logic. DAX owns only filter-respecting aggregation and display. Proposed measures:

| Measure | Mart; numerator / denominator | Unavailable behavior |
| --- | --- | --- |
| Core Collection Coverage | member fact; completed required-core members / declared members | Blank + reason if plan or identity invalid |
| Historical Context Coverage | member/observation fact; distinct exact-ref declaration members / declared members | Blank if qualification fails; after-only shown separately |
| Candidate Emission Coverage | member/candidate fact; distinct members with emission / declared members | Blank if baseline invalid |
| Reviewed Candidate Acceptance | candidate fact; accepted IDs / terminally reviewed ACCEPT-or-REJECT IDs | Blank for 0/0 or duplicate terminal |
| UNKNOWN Rate | finding fact; UNKNOWN required member-stage findings / verified required member-stage findings | Blank if question set or finding rows missing |
| Required Task Completion | task fact; verified completed required tasks / all required planned tasks | Blank if task plan invalid; failure stays in D |

Each measure surfaces count cards as well as a percentage and version label. No observed adoption/recovery card appears. The dashboard does not invent a risk score or replicate a generic update-bot/CI/SCA view. Drill-through uses stable IDs; bridge rows are never summed into measures.
