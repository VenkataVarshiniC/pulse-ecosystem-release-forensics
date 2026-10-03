# M4.2 Power BI implementation record

Status: **M4.2 PASS — TECHNICAL POWER BI MILESTONE COMPLETE**. The text-based PBIP was refreshed and validated in Power BI Desktop after the final scope-isolation repair. PBIR/TMDL static validation, live semantic queries, source reconciliation, rendered case isolation, KPI formatting, and drill-through behavior passed. This is a technical milestone result only: G8 remains **NOT_YET_VALIDATED**, and no stakeholder validation is claimed.

The project is at analytics/powerbi/PULSE_Release_Forensics.pbip, directly under analytics/powerbi; the handoff's extra PULSE directory is absent. The pre-existing .pbix is a separate binary export and was not edited or reconciled to these PBIP changes.

## Governed scope and model

Seven snapshot-bearing M import queries filter at source to snapshot_state = PUBLISHED_VALIDATION and exactly:

- pytest: 08852d5f-9843-5406-a69b-7039ea2ddaa4
- urllib3: bd3a02a5-0c2d-5eec-84fd-8e9b93a238a3

The four approved dimensions remain import queries. SnapshotScope derives from the filtered bridge, projects the six lineage fields, joins readable case context, and supplies single-select case and snapshot labels. A read-only SQL DISTINCT over the six scope fields returned exactly two approved rows, and Desktop validation confirmed dynamic selection of the two published scopes. DRAFT rows are excluded at query level.

The semantic member key is lowercased analysis_snapshot_id|case_key|repository_key on the case-repository bridge and four member facts. The bridge exposes repository_name from dim_repository. Collection tasks retain a direct snapshot route because shared upstream tasks can have a NULL repository key.

The edited model has 11 approved marts, SnapshotScope, _Measures, and existing auto-date tables. Its 12 governed relationships are active many-to-one from child to parent with single-direction propagation: release→case→bridge, repository→bridge, scope→bridge and tasks, bridge→four member facts, and evidence source→tasks/candidates/observations. The bridge-finding-evidence table has no relationship into metric paths. Ten existing auto-date relationships remain. There are no fact-to-fact, many-to-many, or bidirectional shortcuts.

_Measures contains 35 DAX presentation measures for scope selection, declared-member and collection coverage, historical declaration context, candidate activity and review, required tasks, finding counts, path counts, and finding-state display. SQL/dbt remains authoritative for eligibility, statuses, numerators, denominators, sufficiency, and missingness. Desktop validation confirmed **Unavailable (0 eligible observations)** for pytest's 0/0 reviewed population, urllib3 acceptance **Inherited review · 0% (0/2)**, and urllib3 rejection **Inherited review · 100% (2/2)**. No governed UNKNOWN-rate, adoption, recovery, ecosystem-impact, risk, or health KPI was added.

The PBIR defines Release Investigation Overview, Evidence & Uncertainty Diagnostics, Candidate & Review Quality, Finding Detail, Observation Detail, and Candidate Detail. The three main pages contain strict case/snapshot slicers, explicit slicer-to-visual filtering, investigation visuals, and both required provisional/cohort labels. Desktop validation confirmed pytest and urllib3 remain dynamically isolated in member and observation visuals. Detail pages are hidden from ordinary navigation, use ID drill-through fields, open one selected record, and have working Back buttons. Lifecycle categories are evidence categories, not causal chronology. UNKNOWN is distinct from bounded NO; missing evidence is not negative evidence; AFTER_ONLY does not prove historical absence; REJECT does not prove absence of migration friction; and candidate firings that share an artifact are not independent incidents.

The Microsoft TMDL parser accepted 24 tables, 22 relationships (12 governed and 10 auto-date), and 35 measures. The Microsoft Power BI report-author CLI validated the PBIR with zero errors and warnings. Static checks resolved every visual field to a model object, checked canvas bounds and strict slicers, and confirmed seven source filters. The repository's frozen replay reconciliation passed against the connected local database. Power BI Desktop then loaded and rendered the edited project and validated dynamic filtering, governed measure displays, non-truncated denominators, hidden detail pages, single-record drill-through, and Back navigation.

The project was authored by text editing only. Credentials, PostgreSQL data, source evidence, collectors, migrations, and stakeholder results were not changed. The pre-existing `.pbix` binary was not regenerated from the final PBIP and is excluded from the milestone commit.

