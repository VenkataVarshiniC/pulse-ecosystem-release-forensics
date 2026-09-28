# M2.4 data-quality and publication record

**Model defects observed:** none after the complete dbt build, mart grain and
selected-input tests, 40 mart reconciliation checks and source/model
fingerprint comparisons. All eight cohort members survive the member bridge
and repository fact. The one-artifact/two-candidate/two-review shape remains
intact, with no inflated finding or observation counts. No dimension-key
orphans, duplicate mart grains, fixture fact rows or source mutations were
observed. The empty support bridge is faithful to the source.

**Correctly exposed source limitations:** only one paired pre-release path
exists; six decisions are AFTER_ONLY and nine UNRESOLVED. Source event and
candidate emission times may be absent and are not backfilled with retrieval
or PR event times. Thirty-eight assessments remain LEGACY_UNCLASSIFIED.
Thirty-eight findings remain UNKNOWN and two remain bounded NO. Both review
events reject copied-upstream text; no accepted positive chain exists.
Adoption and recovery remain UNKNOWN for all eight members. No pytest
candidate exists, so its acceptance denominator is zero and the rate is
unavailable. These statuses are evidence states, not real-world absence or
organizational outcomes.

The positive-YES support gate is encoded as a dbt integrity test, but the
frozen population has zero YES findings and zero typed support edges. Its
positive branch is therefore not empirically exercised here; an approved
future synthetic dbt unit fixture or real accepted chain is required before
publishing YES-based measures.

**Publication limitation:** the two input manifests are DRAFT and carry
unrecorded rule and not-yet-modeled metric versions. Their model version
describes the PostgreSQL load, not the M2.4 mart contract. Raw input hashes
and dbt checks can pass without repairing those missing approvals. The
analytical tables are therefore validation-only; no immutable published
snapshot was created. A later approved publication requires a new versioned
manifest and immutable output history. No Power BI consumption is authorized
by this milestone result.
