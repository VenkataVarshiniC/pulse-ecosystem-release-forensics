# M4.2 future Power BI validation checklist

These are **future acceptance checks**, not completed Power BI tests. The immutable reference is release `m4-1b-9979f0a7b15d6e70b90f`, [manifest](../../../data/validation/m4-1b-publication-manifest.json), [46 metric outputs](../../../data/validation/m4-1b-replay-metrics.json), and [reconciliation](../../../data/validation/m4-1b-reconciliation.json). Before a future connection or refresh, validate the publication record and row fingerprints through the governed process; reject drift rather than refreshing into changed SQL/model outputs. Do not rebuild the database merely to check this documentation freeze.

| Checkpoint | pytest 8.0.0 published snapshot | urllib3 2.0.0 published snapshot | Cross-case rule |
|---|---:|---:|---|
| Snapshot ID | `08852d5f-9843-5406-a69b-7039ea2ddaa4` | `bd3a02a5-0c2d-5eec-84fd-8e9b93a238a3` | Both `PUBLISHED_VALIDATION`; legacy DRAFT excluded. |
| Declared members / core collection | 2 / 2 complete | 6 / 6 complete | Eight total; MET-001 2/2 and 6/6. |
| Historical declaration coverage (MET-002) | 1/2 | 1/6 | Two of eight exact-ref declaration members; not adoption. |
| Paired pre-release members | 1/2 | 0/6 | One of eight; separate from declaration count. |
| Candidate-emitting members (MET-008) | 0/2 | 1/6 | Candidate path separate from finding path. |
| Candidate IDs / distinct shared artifacts | 0 / 0 | 2 / 1 | Two detector firings from one artifact, not two incidents. |
| Inherited terminal reviews | 0 | 2 REJECT | Original review IDs/timestamps, not new reviewer actions. |
| Reviewed acceptance (MET-009) | 0/0 → **Unavailable** | 0/2 → **0%** | Never convert a zero denominator to zero percent. |
| Reviewed rejection (MET-010) | 0/0 → **Unavailable** | 2/2 → 100% | Review disposition only. |
| Required-task completion (MET-016) | 11/11 | 27/27 | 38/38 required planned tasks; no all-source completeness claim. |
| Findings / UNKNOWN / bounded NO | 10 / 8 / 2 | 30 / 30 / 0 | 40 / 38 / 2; positive = 0. |
| Replay sufficiency | 2 SUFFICIENT / 8 INSUFFICIENT | 0 SUFFICIENT / 30 INSUFFICIENT | 2 / 38; do not show legacy `LEGACY_UNCLASSIFIED`. |
| Adoption and recovery | UNKNOWN | UNKNOWN | All eight members; no adoption/recovery KPI. |
| Governed metric outputs | 23 | 23 | 46 outputs; registry `m2-5-metric-registry-v1`. |

The replay mart reference has eight `bridge_case_repository` rows, 54 `fct_collection_task`, 11 `fct_evidence_observation`, two `fct_candidate_review`, 40 `fct_lifecycle_finding`, eight `fct_repository_investigation`, and **zero** `bridge_finding_evidence` support edges. There are 72 selected artifact *links* across snapshots, not 72 distinct new captures. MET-005's 2/10 and 0/30 and MET-012's 8/10 and 30/30 are observed partial components with `metric_value = null`; no governed partial rate may be promoted to a card. Verify all per-case status, N/D, and values against the replay JSON rather than recopying the historical M2.5 DRAFT file.

When M4.2 resumes, check each item and retain evidence of the result:

- [ ] Read-only connection selects only the two manifest-approved `PUBLISHED_VALIDATION` IDs; default and refresh exclude every DRAFT snapshot.
- [ ] One case and one snapshot are required for every rate. Cross-case views label their population and calculate each case separately; no implicit pooled denominator.
- [ ] Every semantic relationship has expected cardinality and one-way direction. The member bridge has 2/6 rows; joins do not multiply candidate, finding, task, or observation rows. Shared upstream tasks with NULL repository key remain visible.
- [ ] Main pages preserve all declared members even without candidate or paired history. Candidate/artifact counts stay 2/1, not 2/2; support-edge count stays zero.
- [ ] Metric status, numerator, denominator, value, contract version, and unavailable reason match the 46 governed outputs. DAX only formats or aggregates within valid scope.
- [ ] `0/0` is Unavailable; READY `0/N` shows zero with N; UNKNOWN, INSUFFICIENT, REJECT, no candidate, and bounded NO remain distinct.
- [ ] Page 1 and 2 do not show unsupported adoption/recovery, ecosystem impact, or risk scores. MET-006 and PARTIAL metrics are withheld or explicitly partial.
- [ ] Drill-through preserves snapshot/case and stable finding/candidate/observation IDs. Missing support edges or path-level provenance display a gap, not invented evidence.
- [ ] Candidate detail identifies inherited review evidence and one shared artifact only after a publication-scoped lineage projection is validated; otherwise the deep drill is visibly unavailable.
- [ ] Provenance includes case, release, snapshot, rule, metric/model version, capture method, event versus retrieval time where known, and limitations; no credentials or unnecessary personal data.
- [ ] Labels, keyboard navigation, contrast, reading order, tooltip wording, and visible denominators pass accessibility review. Page priority and terminology await real stakeholder feedback.
- [ ] Save the eventual `.pbix`, screenshots, relationship diagram, metric reconciliation, and validation evidence only after a real build. Do not mark M4.2 complete from this checklist alone.
