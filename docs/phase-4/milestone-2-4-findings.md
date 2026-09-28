# Phase 4 Milestone 2.4 findings

**Classification: PASS for the analytical model; publication deferred by the
governed gate.** Four dimensions, five facts and two bridges were built as
11 dbt-managed `analytics` tables. They carry explicit snapshot scope and
source IDs, reconcile to M2.2/M2.3, and preserve the eight-member cohort.
The two current source snapshots remain DRAFT because their rule version is
unrecorded, metric version is not yet modeled, and model version describes
the PostgreSQL load rather than an approved mart contract. Publishing either
would violate the [publication contract](m2-prep/analytical-snapshot-contract.md).
No source or publication row was mutated. These marts are validation-only,
not yet a production or Power BI dataset.

The [analytical model](m2-implementation/m2-4-analytical-model.md) gives all
11 grains, keys and materialization choices. Row counts are dimensions
2 cases, 8 repositories, 2 releases and 9 represented sources; bridges
8 case/repository rows and 0 actual finding support edges; facts 54 tasks,
8 repository investigations, 2 candidates, 40 findings and 11 observations.
The [safe join guide](m2-implementation/m2-4-join-guide.md) documents
dimension-to-fact directions and snapshot filtering. The source-dimension
grain and snapshot-scoped task fact are documented deviations from M2-PREP.

The dbt clean build passed **30 models and 173 tests** with zero warnings or
failures. Standalone dbt tests passed. The deterministic
[40/40 mart reconciliation](m2-implementation/m2-4-mart-reconciliation.md)
preserved 1 PAIRED, 6 AFTER_ONLY and 9 UNRESOLVED historical paths; one
artifact/two candidates/two REJECT reviews; 2 SUFFICIENT and 38
LEGACY_UNCLASSIFIED assessments; and 38 UNKNOWN plus 2 bounded NO findings.
Adoption and recovery remain UNKNOWN for all eight members. Cross-fact,
orphan, grain, selected-input and fixture-isolation tests passed. All 30
source tables remained fingerprint-identical, and all 30 model row sets were
byte-identical after a repeat build. The 142 frozen input files still matched
their approved allowlist. The final clean-build baseline was 20.55 seconds, with
`fct_collection_task` the largest mart at 54 rows; no scale inference follows.

The [metric readiness matrix](m2-implementation/m2-4-metric-readiness.md)
covers all 23 contracts: 10 READY for bounded platform calculation, seven
partial, five unavailable for missing evidence and one stakeholder blocked.
Zero-candidate pytest acceptance remains unavailable, never 0%. The
[quality record](m2-implementation/m2-4-data-quality.md) separates preserved
source limitations from model defects; no model defect was observed.

The model is structurally prepared for a future one-way Power BI semantic
layer but has **no published snapshot** and is not ready for BI consumption.
M2.5 must not treat these DRAFT tables as a governed published dataset.
Before a publication-dependent analysis, an approved rule/metric/model
versioned manifest and immutable historical output mechanism are required.
No full advanced SQL analysis, statistical inference, Power BI or AI work
was started in M2.4.
