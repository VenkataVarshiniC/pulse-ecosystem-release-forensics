# Wave 1 hypothesis reconciliation

Classifications apply only to Wave 1: `CONFIRMED`, `PARTIALLY_CONFIRMED`, `CONTRADICTED`, `MIXED`, or `NOT_ADDRESSED`. “Confirmed” means the stated need has direct support in this convenience sample; it does not mean population validation.

## Original Phase 3 need hypotheses

| ID and original hypothesis | Source | Survey questions | Direct evidence | Counter-evidence | Classification / confidence | Implication |
| --- | --- | --- | --- | --- | --- | --- |
| N-01: know which owned repositories warrant attention | `stakeholder-needs-hypotheses.md` | Q10, Q11, Q21, Q26 | 5/9 chose affected-repository identification as most useful; 3/9 reported manual effort and 3/9 a problem. | Four chose another most-useful capability. | `CONFIRMED`, moderate-high | Retain repository identification and evidence-based prioritization; validate workflow integration. |
| N-02: know historical or installed dependency state | Same | Q11–Q13, Q21–Q23 | Actual-version effort 5/9; historical-state problem 3/9; historical state/version/CI each required by 5/9 for trust. | Only 1/9 chose reconstruction as most useful. | `CONFIRMED`, moderate | Evidence depth is relevant, but it supports another decision rather than being the primary user-facing outcome. |
| N-03: see why a repository/event was flagged and trace it to evidence | Same | Q22, Q24 | Explanation 4/9; original link 3/9; traceability mean 4.11/5 and 7/9 rated 4–5. | Two traceability ratings were 3. | `CONFIRMED`, high | Preserve explanation and source navigation as core trust requirements. |
| N-04: distinguish known, bounded NO, and missing evidence | Same | Q13, Q14, Q23 | All respondents encounter insufficient evidence at least rarely; four prefer a likely answer with explicit uncertainty and one prefers explicit UNKNOWN. | Four want a likely answer alongside uncertainty; two prefer confidence scores; two reject automated conclusions. | `PARTIALLY_CONFIRMED`, moderate | Preserve UNKNOWN semantics; test presentation separately and never turn estimates into findings. |
| N-05: avoid irrelevant candidates without missing consequential signals | Same | Q21, Q27 | Irrelevant alerts 5/9; false positives 4/9; trust barrier 5/9. | No acceptable volume, recall tradeoff, or PULSE example was tested. | `PARTIALLY_CONFIRMED`, moderate-high | Retain conservative qualification and grouping; measure review burden before adding automation. |
| N-06: understand completion/recovery | Same | Q11, Q17, Q21 | Completion manual effort 4/9; completion problem 2/9; every respondent supplied completion signals. | Signals are heterogeneous and no recovery outcome was audited. | `PARTIALLY_CONFIRMED`, moderate | Strengthen support for multiple completion criteria; do not collapse migration, deployment, monitoring, and recovery. |
| N-07: compare evidence across an owned repository set | Same | Q6, Q10, Q15, Q26 | 5/9 reported more than one repository; affected-repository identification led usefulness; respondents named priority factors. | Three reported one repository; no respondent demonstrated a portfolio comparison. | `PARTIALLY_CONFIRMED`, moderate-low | Retain bounded multi-repository triage as optional, not as a universal persona assumption. |
| N-08: inspect collection method, completeness, and replay boundary | Same | Q22–Q24 | Provenance and missing-evidence preferences support traceability and completeness disclosure. | Collection method and replay were not directly asked or demonstrated. | `PARTIALLY_CONFIRMED`, low-moderate | Keep the integrity requirement; validate whether method-level detail helps actual decisions. |

## Specific PULSE concepts

| Concept | Relevant evidence | Counter-evidence | Classification | Implication |
| --- | --- | --- | --- | --- |
| A. Investigation uses fragmented sources | 8/9 used multiple source types; R02/R08 explicitly reported spread. | Explicit fragmentation pain was only 2/9. | `PARTIALLY_CONFIRMED` | Centralization is plausible but source multiplicity alone is not proof of pain. |
| B. Historical state is difficult/manual | Difficulty mean 3.22/5; version-use effort 5/9; historical problem 3/9. | No rating was 5 and only one chose history as most useful. | `CONFIRMED` | Phase 7 evidence depth aligns with a real need, within limits. |
| C. Identifying affected repositories matters | Most useful for 5/9; manual/problem selections from 3/9 each. | Four preferred other capabilities. | `CONFIRMED` | Lead with affected-set support, tied to evidence. |
| D. Engineers need more than a declaration | Respondents used issues, commits, CI, tests, logs and documentation; trust requires version/history/CI. | The survey did not test a declaration-only counterexample. | `PARTIALLY_CONFIRMED` | Preserve distinct evidence types and avoid adoption inference. |
| E. CI/tests/runtime influence confidence | Six used or required CI/test/runtime evidence; 3/9 named tests/CI as most confident. | Package documentation led at 3/9; context varies. | `CONFIRMED` | Treat operational evidence as important but source-specific. |
| F. Missing evidence should stay explicit | Four preferred a likely answer with explicit uncertainty, one explicit UNKNOWN, and two confidence scores; three requested a missing-evidence indication. | Four prefer a likely answer and two a confidence score; two reject automation. | `MIXED` | Keep UNKNOWN as the finding; separately test labeled decision aids. |
| G. Provenance matters | Traceability mean 4.11/5, 7/9 high. | Original-link selection was 3/9. | `CONFIRMED` | Provenance remains a core requirement. |
| H. Automation requires qualification/explanation | Explanation 4/9, evidence prerequisites across all respondents, trust barrier 5/9. | Only 2/9 selected human review as required. | `CONFIRMED` | Qualification is required; mandatory human review at every step is not validated. |
| I. False positives are a barrier | Selected by 4/9; irrelevant alerts encountered by 5/9. | Four respondents gave no signal. | `PARTIALLY_CONFIRMED` | Preserve conservative candidate semantics and measure review cost. |
| J. Human review burden is a barrier | Selected by 3/9. | Six did not; two want human review for trust. | `PARTIALLY_CONFIRMED` | Make review proportional and optional by evidence/risk, pending validation. |
| K. Centralized evidence could help | Central evidence was most useful for 2/9; four gave direct consolidation signals. | Five did not identify it. | `PARTIALLY_CONFIRMED` | Retain as a capability, not a demand claim. |
| L. Current tools incompletely support end-to-end workflow | Tool support median 3/5; multiple problems were reported. | Two said tools are sufficient; all ratings were 3 or 4. | `MIXED` | PULSE must demonstrate a specific incremental gap. |
| M. Proposed investigator persona is accurate | Seven have upgrade experience; five reported multi-repository scope. | No platform/dependency role; roles and experience are broad. | `PARTIALLY_CONFIRMED` | Broaden persona to an investigation role spanning several engineering functions. |
| N. Final owner is one stable role | Five owner categories; no category exceeds 2/9. | None. | `CONTRADICTED` | Separate investigator, reviewer, and decision owner. |
| O. Stakeholders would use PULSE as designed | Usefulness mean 3.89/5. | Trust, integration, privacy, review, and tool-sufficiency barriers; no usage trial. | `NOT_ADDRESSED` | Interest cannot substitute for observed use or acceptance. |
| P. PULSE changes migration/remediation decisions | No direct decision experiment. | Two said results would not affect decisions. | `NOT_ADDRESSED` | Keep decision impact and user value unvalidated. |
| Q. Evidence-depth investment aligns with needs | Historical/version evidence and traceability received repeated support. | Affected-repository identification led usefulness; only one chose historical reconstruction. | `PARTIALLY_CONFIRMED` | Keep Phase 7 bounded and connect depth to affected-set and trust decisions. |

## Classification summary

- Strongest confirmed needs: affected-repository identification, historical/version evidence, provenance, CI/test/runtime evidence, and explained qualification.
- Contradicted: a single stable final decision-owner role.
- Mixed: preferred insufficient-evidence presentation and whether existing tools leave an end-to-end gap.
- Not addressed: actual PULSE use and changed migration/remediation decisions.
