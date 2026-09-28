# PULSE boundary reassessment for future stakeholder reconciliation

This proposes changes to the [provisional Phase 3 solution boundary](../../phase-3/solution-boundary.md); it does **not** edit formal Phase 3 requirements or authorize implementation. Research date **2026-09-27**. The [matrix](competitive-capability-matrix.md) shows adjacent overlap, and [Phase 4 M1A](../milestone-1a-findings.md) shows current PULSE computability limits.

| Existing proposed responsibility | Proposed treatment | Reason / evidence gate |
| --- | --- | --- |
| Typed release case, declared cohort/window and denominator | **Retain** | Distinguishes a case from generic inventory; must be useful to a real decision owner. |
| Raw collection, capture method, artifact identity | **Retain and integrate** | GitHub/API, registry, CI and risk tools should remain authoritative sources [S06,S07,S15,S16,S18]. Avoid recreating them. |
| Exact-ref historical state | **Narrow** | Own only release-boundary evidence rule and unresolved state; Phase 2 historical coverage is weak. Need validated source method. |
| Qualified target-version adoption claims | **Narrow/defer** | Current target-version metric unavailable; proposed PR or generic graph insufficient. Never convert UNKNOWN to NO. |
| Origin-aware downstream candidate/review | **Retain** | Phase 2 false positives from copied upstream text support review separation; stakeholder burden and precision still unknown. |
| Evidence sufficiency, conflict and UNKNOWN | **Retain** | Integrity property differentiates the *case method* from a risk score, but utility of UNKNOWN-heavy output is unvalidated. |
| Bounded recovery finding | **Stakeholder-dependent/defer** | Eligible set, qualified signal, window and owner absent; existing security remediation dashboards overlap [S19,S20]. |
| Cross-repository attention/ranking | **Narrow or remove** | Generic cross-repo views exist [S05,S18,S19]; no stakeholder priority decision validated. |
| Automated updates, SCA, CI, package registry | **Integrate references / explicitly not own** | Mature documented alternatives [S01,S03,S06,S08,S13,S16–S20]. |
| Human review workspace | **Stakeholder-dependent** | A report plus case ledger may suffice; interactive handoff/collaboration need direct validation. |

**Provisional differentiation statement:** Unlike update automation and security/risk tooling, which document upgrade proposals, pre-merge checks and portfolio risk views [S01,S04,S08,S13,S18,S19], PULSE is *designed* to assemble a declared target-release cohort into a human-reviewed, source-linked forensic case that preserves evidence gaps and UNKNOWN. This is a **design hypothesis**, not a verified market advantage or current full product capability.

No claim that PULSE is unique, first, faster, more accurate or already useful follows from this assessment. If stakeholders show their existing stack resolves the same decision adequately, narrow or stop the dedicated product idea.
