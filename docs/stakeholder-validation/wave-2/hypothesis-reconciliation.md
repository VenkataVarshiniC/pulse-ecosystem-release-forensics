# Wave 2 cumulative hypothesis reconciliation

Classifications use the frozen Wave 1 n = 9 plus five additions. `CONFIRMED` means direct support in this convenience sample, not population validation.

## Original Phase 3 needs

| Need | Cumulative evidence and counter-evidence | Classification / confidence | Implication |
| --- | --- | --- | --- |
| N-01: know which repositories warrant attention | Most useful 5/14; pain 6/14; effort 4/14. No addition chose it as most useful. | `CONFIRMED`, moderate | Retain, but do not present as a universal lead capability. |
| N-02: know historical or installed state | Actual-version effort 7/14; historical pain 6/14; version/history trust 7/14 each. Reconstruction most useful 1/14. | `CONFIRMED`, moderate-high | Keep depth tied to a concrete investigation decision. |
| N-03: trace flags to evidence | Explanation and version/history inputs 7/14 each; traceability mean 4.07/5. | `CONFIRMED`, high | Preserve explanation and source navigation. |
| N-04: distinguish known, bounded NO, and missing evidence | Explicit uncertainty/UNKNOWN 7/14, confidence 3/14, non-reliance 4/14. | `PARTIALLY_CONFIRMED`, moderate-high | Preserve UNKNOWN; test presentation without changing finding semantics. |
| N-05: reduce irrelevant candidates without missing consequences | Irrelevant alerts 8/14; trust barrier 9/14; false positives 5/14. | `PARTIALLY_CONFIRMED`, high | Keep conservative qualification and measure review burden. |
| N-06: understand completion/recovery | Completion effort 5/14; difficulty 3/14; completion signals heterogeneous. No recovery outcome audited. | `PARTIALLY_CONFIRMED`, moderate | Represent several completion criteria; keep recovery deferred. |
| N-07: compare an owned repository set | 7/14 report multiple repositories; 4/14 one and 3/14 unsure. No portfolio task occurred. | `PARTIALLY_CONFIRMED`, moderate | Keep bounded comparison optional. |
| N-08: inspect method, completeness, and replay boundary | Provenance and missingness receive support; collection method/replay were not directly tested. | `PARTIALLY_CONFIRMED`, low-moderate | Retain integrity detail and validate usability. |

## Specific PULSE concepts

| Concept | Wave 2 result | Classification | Implication |
| --- | --- | --- | --- |
| A. Investigation spans fragmented sources | 11/14 use multiple sources, but explicit spread pain is 3/14. | `PARTIALLY_CONFIRMED` | Centralization is plausible; multiplicity alone is not pain. |
| B. Historical state is difficult/manual | Stable difficulty mean 3.21; repeated version/history signals. | `CONFIRMED` | Evidence depth remains aligned. |
| C. Affected-repository identification matters | Cumulative plurality 5/14, but 0/5 additions chose it as most useful. | `CONFIRMED` | Retain with weaker universality claim. |
| D. Engineers need more than declarations | Evidence sources and trust inputs extend across history, tests, CI, logs, issues, and commits. | `PARTIALLY_CONFIRMED` | Preserve evidence distinctions; test declaration-only cases. |
| E. CI/tests/runtime influence confidence | 11/14 select operational evidence as source/trust input. | `CONFIRMED` | Define eligibility and environment semantics. |
| F. Missing evidence should remain explicit | Explicit UNKNOWN strengthens; confidence and non-reliance remain material. | `MIXED` | Keep UNKNOWN; separately test labeled decision aids. |
| G. Provenance matters | Mean 4.07/5; 10/14 high. | `CONFIRMED` | Core trust requirement remains. |
| H. Automation needs qualification/explanation | Trust barrier 9/14; explanation 7/14; all select evidence prerequisites. | `CONFIRMED` | Avoid unqualified conclusions. |
| I. False positives block adoption | Alerts 8/14; barrier 5/14. | `PARTIALLY_CONFIRMED` | Preserve grouping and measure review cost. |
| J. Human review can be a barrier | Burden 4/14; only 3/14 require review for trust. | `PARTIALLY_CONFIRMED` | Use policy-based routing, pending validation. |
| K. Central evidence could help | Direct signal 7/14; central evidence most useful 4/14. | `PARTIALLY_CONFIRMED` | Interest strengthened; integration value untested. |
| L. Current tools incompletely support the workflow | Mean support 3.36/5; three say tools are sufficient. | `MIXED` | Demonstrate a narrow incremental gap. |
| M. Proposed investigator persona is accurate | 10/14 have upgrade experience; roles and authority remain diverse. | `PARTIALLY_CONFIRMED` | Use a broad engineer-investigator persona. |
| N. Final owner is one stable role | Seven categories; technical lead 4/14 is only a plurality. | `CONTRADICTED` | Keep roles configurable and separate. |
| O. Stakeholders would use PULSE as designed | Usefulness mean 3.86/5; no product task. | `NOT_ADDRESSED` | Interest is not observed use. |
| P. PULSE changes migration/remediation decisions | No decision experiment; two report possible non-impact. | `NOT_ADDRESSED` | Decision impact remains unvalidated. |
| Q. Evidence-depth investment aligns with needs | Repeated version/history, provenance, and operational-evidence signals; history top-ranked by 1/14. | `PARTIALLY_CONFIRMED` | Keep depth bounded and outcome-linked. |

Wave 2 strengthens trust, explicit UNKNOWN, centralization, and operational-evidence signals. It weakens the claim that affected-repository identification is consistently the top capability. No classification authorizes claims of adoption, ROI, or decision impact.
