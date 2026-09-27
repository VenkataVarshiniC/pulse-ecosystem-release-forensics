# Current PULSE capability matrix

This matrix describes the **current validated PULSE system**, not the public repositories' tooling or a proposed future system. Statuses mean: `supported` within the frozen Phase 2 boundary; `partially supported` with material evidence/coverage limits; `unsupported` because required input or method was absent; `not yet validated` where stakeholder or broader-case utility is untested. See [Phase 2 findings](../phase-2/phase-2-findings.md) and [evidence sufficiency](../phase-2/evidence-sufficiency.md).

| Capability | Status | Current evidence and limit |
| --- | --- | --- |
| Bounded collection reliability | `supported` | Authenticated, paginated live collection, task outcomes, verified resume, and immutable provenance worked for declared cases; not ecosystem completeness. |
| Historical reconstruction | `partially supported` | Exact-ref path-scoped parsing works, but missing in-window anchors and cross-file history leave many boundary states unresolved. |
| Dependency declaration evidence | `partially supported` | Target-package exact-ref declaration evidence in 2/8 frozen repositories; this is coverage, not adoption. |
| Installed target-version / observed adoption evidence | `unsupported` | Comprehensive target-version lockfile selection and ordinary runtime/CI resolution were not collected; no observed-adoption rate. |
| Candidate generation | `partially supported` | Rules emit reviewable candidates; two Phase 2 firings from one bot artifact were rejected; recall and broad precision unmeasured. |
| Analyst review separation | `supported` | Frozen baseline and independent decision ledger keep rejected candidates out of accepted evidence. |
| Evidence provenance and collection completeness | `supported` | Raw snapshots, task/run identity, source status, and capture method are explicit within validated cases. |
| Missing-data semantics | `supported` | UNKNOWN propagates unmet prerequisites; bounded `NO QUALIFYING EVIDENCE FOUND` is not real-world absence. |
| Remediation evidence | `partially supported` | Candidate/review path exists, but zero accepted lifecycle events in Phase 2; bounded negative findings need source sufficiency and pre-release context. |
| Recovery evidence and eligibility | `unsupported` | Downstream releases were not collected; no recovery-eligible denominator. |
| Deterministic reporting | `supported` | Two frozen case reports reproduce with verified identity and explicit unavailable measures; narrative utility untested. |
| Portfolio prioritization for a stakeholder | `not yet validated` | Cohort-level output exists, but no observed organizational priority decision or validated primary user. |

`Supported` is not a claim of production readiness or user value. The [gap analysis](gap-analysis.md) treats possible decision capabilities as conditional; no future architecture or requirement is prescribed here.
