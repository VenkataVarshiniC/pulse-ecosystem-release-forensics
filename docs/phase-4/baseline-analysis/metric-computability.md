# Audit of all 23 metric contracts

Status is at the **contract across this input set**. A `COMPUTABLE` metric can still have a case-specific 0/0, correctly shown as `UNAVAILABLE_UNDEFINED_DENOMINATOR` in [baseline-metrics.json](baseline-metrics.json). Five reported lifecycle categories are available as a descriptive diagnostic, but the **stakeholder-required completion question set is not defined**. No metric status licenses an adoption, recovery, population, or labor-saving claim. Exact N/D, status, grain, filters, exclusions and reason are in the machine output.

| Metric | Status | Required fields | Available fields | Missing fields / boundary | Denominator valid? | Baseline computable? / reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MET-001 Core collection | COMPUTABLE | Frozen member, required core task outcome | 2/6 members and source statuses | None for planned sources | Yes, 2 and 6 | Yes; planned acquisition only. |
| MET-002 Historical context | COMPUTABLE | Exact-ref parsed target declaration, member | Report history context and paths | Broader release-time history | Yes, 2 and 6 | Yes; declaration coverage only. |
| MET-003 Target-version evidence | UNAVAILABLE_MISSING_SOURCE | Qualified version, ref/environment/time/artifact | Declarations only | Installed/resolved-version source | Cohort exists; qualifying N cannot be established | No; no observed-adoption inference. |
| MET-004 Stage source completeness | PARTIALLY_COMPUTABLE | Versioned required-source set per category, source outcomes | Source-class statuses | Frozen category→required-source map as analytical field | Not fully qualified | Source availability only, not contract rate. |
| MET-005 Stage sufficiency | COMPUTABLE | Member-category sufficiency under current method | Boolean for all reported categories/members | Future evidence method | Yes per named category | Yes for current bounded Phase 2 rule. |
| MET-006 Investigation outcome | UNAVAILABLE_STAKEHOLDER_DEFINITION | Required category question set, resolved output | Findings exist | Approved completion/question set | Cohort exists; eligible question set undefined | No; analytical completion unvalidated. |
| MET-007 Recovery eligibility | UNAVAILABLE_UNDEFINED_DENOMINATOR | Eligible event/set/window and downstream source | No accepted event | Eligibility and qualifying source | No eligible set | No; PR merge insufficient. |
| MET-008 Emission coverage | COMPUTABLE | Member, immutable candidate baseline | Complete baseline and member counts | None | Yes, 2 and 6 | Yes; activity, not incidence. |
| MET-009 Reviewed acceptance | COMPUTABLE | Candidate ID, terminal review | Two reviewed rejected emissions in urllib3 | No missing field | pytest 0/0; urllib3 2 | urllib3 0/2; pytest unavailable. |
| MET-010 Reviewed rejection | COMPUTABLE | Candidate ID, terminal review | Same | No missing field | pytest 0/0; urllib3 2 | urllib3 2/2; pytest unavailable. |
| MET-011 Unresolved share | COMPUTABLE | Baseline IDs, review state | Same | No missing field | pytest 0/0; urllib3 2 | urllib3 0/2; pytest unavailable. |
| MET-012 UNKNOWN rate | PARTIALLY_COMPUTABLE | Required member-category set, verified finding | Five report categories per member | Stakeholder-required question set | Valid only per **reported** category | Descriptive per-category N/D, not completion-wide rate. |
| MET-013 UNKNOWN reasons | PARTIALLY_COMPUTABLE | Reason per UNKNOWN member-category | Report explanation; repository `missing_sources` | Controlled stage-level reason codes | UNKNOWN count known; reason partition not | Qualitative/repository labels only. |
| MET-014 Conflict rate | UNAVAILABLE_MISSING_FIELD | Explicit conflict taxonomy and assessment | No complete conflict coding | Conflict state across all assessed pairs | Not verified | No; absence of conflict code ≠ no conflicts. |
| MET-015 Missing-source contribution | PARTIALLY_COMPUTABLE | UNKNOWN stage→required missing source | Repository missing-source labels | Stage-source linkage and required-set version | UNKNOWN pairs known; attribution invalid | Qualitative overlap only. |
| MET-016 Required-task completion | COMPUTABLE | Plan requirement, terminal status | Frozen journals/54 attempts | None | Yes, 11 and 27 | Yes; operational only. |
| MET-017 Optional not-found | COMPUTABLE | Optional plan, terminal status | Frozen journals/54 attempts | None | Yes, 4 and 12 | Yes; verified 404, not historical absence. |
| MET-018 Retry incidence | COMPUTABLE | Attempt retry count | All 54 actual attempt stats | None | Yes, 15 and 39 | Yes; both zero observed retries. |
| MET-019 Resume reuse | PARTIALLY_COMPUTABLE | Documented resume run, eligible tasks, reuse links | Separate HTTPX live 11/11 verified reuse | Resume run for either frozen release case | No release-case resume D | HTTPX-only method example; no release-case rate. |
| MET-020 Replay success | COMPUTABLE | Verified attempts and canonical output hashes | Two new attempts/case with matching hashes | None | Yes, 2/case | Yes; frozen replay, not live-source stability. |
| MET-021 YES provenance | UNAVAILABLE_UNDEFINED_DENOMINATOR | YES findings and intact support links | Zero YES findings | Positive finding population | 0/0 in both cases | No rate; zero YES is not zero provenance quality. |
| MET-022 Candidate density | COMPUTABLE | Candidate IDs, member count | Frozen baseline | None | Yes, 2 and 6 | Yes; candidate activity per member. |
| MET-023 Review duration | UNAVAILABLE_MISSING_FIELD | Trusted emission and terminal review timestamps | Source `occurred_at`, review `reviewed_at` | Candidate emission/availability time | No eligible time pairs | No; source event time cannot stand in. |

**Contract-level count:** 12 `COMPUTABLE`, 5 `PARTIALLY_COMPUTABLE`, 6 unavailable. Status labels are audit findings, not inherited from Milestone 1's C/P/F planning labels. No metric definition changed; [change log](../metric-change-log.md) records unresolved ambiguities for later versioning.
