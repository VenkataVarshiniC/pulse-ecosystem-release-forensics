# Constraint and index contract

PostgreSQL constraints protect row-level identity; dbt and application checks protect cross-row evidence semantics. Proposed PK/FK/uniques are enumerated per table in [physical model](postgresql-physical-model.md). FKs to artifact, observation, review, finding and membership must be validated before publication; avoid deferred constraints except a narrowly documented cyclic load (none is proposed). Use migration-time validation for legacy rows, never disable FK enforcement to make a load pass.

| Invariant | Enforcement layer | Failure |
| --- | --- | --- |
| Frozen case version unique, valid window, nonempty cohort before freeze | DATABASE unique/check; APPLICATION freeze check | Reject version / block publication |
| Exactly one membership per case version/repository, no silent deletion | DATABASE composite PK; APPLICATION immutable freeze; DBT denominator anti-join | Block snapshot |
| Release natural key and provider repository ID unique where known | DATABASE unique/partial unique; APPLICATION reconciliation | Quarantine conflict |
| Run/task/attempt identity and nonnegative attempts, counts, valid status | DATABASE PK/FK/check; APPLICATION journal validation | Reject task/load |
| Optional verified not_found distinct from required failure | DATABASE status/required flag; DBT completion logic | Block wrong metric, preserve task |
| Artifact SHA format, method, URI/ref and task/source chain | DATABASE not-null/check/FK; APPLICATION raw digest verification | Quarantine artifact |
| Source event time distinct from retrieval time | Separate nullable timestamptz columns; APPLICATION forbids fallback copy; DBT lineage test | Reject fabricated time |
| Observation semantic type exclusivity and exact ref qualification | DATABASE conditional check; APPLICATION parser/source validation; DBT category test | Quarantine observation |
| Historical paired/after-only endpoint rules | DATABASE endpoint CHECK/FK; APPLICATION ref/path/release ordering; DBT negative-eligibility test | Block affected finding |
| Candidate ID distinct from artifact ID; unique canonical firing | DATABASE unique fingerprint/FK; APPLICATION baseline check; DBT count reconciliation | Quarantine collision |
| One terminal review per candidate/cycle | DATABASE partial unique terminal index; APPLICATION cycle governance; DBT latest-selected test | Block finding |
| Assessment controlled status and version, required reason | DATABASE check/unique/not-null; APPLICATION question prerequisites; DBT cross-row test | Block finding |
| Finding status/version and matching assessment scope | DATABASE FK/unique/check where possible; APPLICATION matching case/member/category/question; DBT matching test | Block finding |
| YES support chain accepted/qualified; rejected/unresolved never support YES | APPLICATION/HUMAN REVIEW qualification; DBT typed-bridge lineage tests | Block finding/mart |
| Bounded NO requires sufficient prerequisites; UNKNOWN remains UNKNOWN | APPLICATION rule evaluation; DBT anti-conversion test | Block finding/mart |
| Recovery needs event, eligible set, window, source | APPLICATION method gate; DBT eligibility test; HUMAN REVIEW definition | Keep unavailable |
| Snapshot input/fact grains unique, no candidate × artifact fan-out | DATABASE manifest uniqueness; DBT unique/relationships/golden totals | Block mart |

Proposed indexes are access-pattern driven, not current-scale tuning: unique case version and membership; (repository_id, package_name, observation_time) for exact-ref evidence; (collection_run_id, repository_id, terminal_status) and task attempt key; artifact (content_sha256), (source_id, source_locator), and task FK; candidate (case_version_id, repository_id, lifecycle_category) and (artifact_id); review (candidate_id, review_cycle, review_sequence DESC); assessment/finding (case_version_id, repository_id, lifecycle_category, question_id, version DESC); manifest fingerprint and publication state. Prefer FK supporting indexes only where query plans justify them; avoid speculative full-text indexes and indexing every URL. Measure with actual workload before adding more.
