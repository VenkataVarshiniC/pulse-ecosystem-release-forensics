# Analytics data-quality and integrity framework

Quality is checked at raw capture, structured load, transformation and publication. A failure blocks or labels the affected measure; it is not repaired by dropping rows. [Phase 3 rules](../phase-3/business-rules.md) and [data requirements](../phase-3/data-requirements.md) are the source of the proposed checks.

| Dimension | Proposed assertion and rule mapping | Failure response |
| --- | --- | --- |
| Completeness | Every frozen member (RULE-011) and required planned task has a row/outcome; stage-specific source set/version exists (RULE-001/010). | Keep member in denominator; mark incomplete/UNKNOWN, publish reason. |
| Provenance | Accepted evidence has source URI/ref, capture method, artifact digest, task/run and review chain (RULE-014). | Block accepted finding or report, never infer source. |
| Validity | Controlled statuses, qualified target-version method, finding status; current declaration ≠ adoption (RULE-003). | Reject invalid row; preserve raw evidence. |
| Consistency | Assessment status agrees with finding; rejected/unresolved candidate cannot support YES (RULE-004/005/006). | Block affected finding/mart and trace rule version. |
| Uniqueness | Unique case membership, task, candidate, terminal review, snapshot/fact composite grain (RULE-011/014). | Deduplicate only by governed identity rule; otherwise fail load/test. |
| Temporal integrity | Release boundary/window and event/capture/review times are distinct; after-only cannot support negative window (RULE-008/009/013). | Make chronology unresolved; no causal wording. |
| Referential integrity | All candidate/review/finding/observation links resolve to matching case, repository, task and artifact (RULE-014). | Quarantine mismatch; prevent orphan fact publication. |
| Analytical grain | One fact row per documented grain; bridge joins cannot multiply counts; frozen member count reconciles (RULE-011). | Fail mart test and inspect fan-out. |
| Recovery eligibility | Qualifying event, eligible set, window and source all explicit (RULE-012). | Rate unavailable; PR merge cannot fill missing source. |
| Replay/reproducibility | Frozen input hashes, rule versions and output fingerprint match under verified replay (RULE-014). | Record mismatch; do not call output deterministic. |

Monitor distinct **method coverage** and **data quality**: a correctly recorded UNKNOWN may be high-quality representation of incomplete evidence. A complete API plan can still miss relevant events (RULE-010). Quality tests must expose that limitation. Capture method separates unattended collection from connector-assisted validation and fixtures. Retention, source permissions, alert thresholds and SLAs await policy/stakeholder decisions; none are asserted here.
