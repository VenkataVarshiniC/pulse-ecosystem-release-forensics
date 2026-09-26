# Phase 1 findings

## Result

Phase 1 produced a coherent forensic baseline. Cases and cohorts are declarative; collection plans and IDs are stable; source failures remain visible; raw evidence is append-only; candidate rules are explainable; review decisions are stored; accepted evidence alone drives repository summaries and denominator-bearing metrics; and JSON plus Markdown reports are deterministic.

All three Phase 0 releases now have structured case definitions, and their original ledger and timelines remain valid. The new HTTPX 0.28.0 case ran through the same detector, review, forensic, and reporting code without release-specific branches. It also exposed a useful false positive: a friction issue that mentioned a linked fix triggered a remediation rule and was rejected during review.

## What remains unresolved

The validation collection was incomplete: three of eleven planned tasks were preserved through connector-assisted retrieval. The engine handles that correctly by reporting unknown states and failures, but Phase 1 did not demonstrate comprehensive unattended GitHub collection in this environment. Discovery still depends materially on analyst queries, and automatic selection of historical before/after refs remains open.

The one-repository validation cohort is sufficient to test architectural reuse, not detection quality at scale. Friction incidence is unavailable because no accepted observed-adoption event established its denominator. That is an analytically correct result, but it limits the substantive conclusion.

## Final decision: PIVOT

The final Phase 1 hardening patch clarifies that adoption evidence coverage is not an adoption rate, requires raw capture provenance, documents non-sequential lifecycle categories, and configures GitHub Actions to run locked dependency installation, Ruff, and the full pytest suite on pull requests and pushes to `main`. These quality controls do not validate unattended collection and do not change the decision.

Keep the repository-bounded evidence model, modular collectors, review boundary, lifecycle engine, and generated reporting. Before Phase 2 analytical scaling, add authenticated end-to-end collection fixtures, automate historical ref pairing, record paginated search observations directly from collector responses, and validate rule precision on several cohorts declared before evidence review.

The methodology works and the architecture does not need a redesign, but the current evidence does not justify scaling storage or making broader adoption and recovery claims.
