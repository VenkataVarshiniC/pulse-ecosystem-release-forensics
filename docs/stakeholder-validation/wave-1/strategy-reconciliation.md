# Wave 1 strategy reconciliation

## Phase 6 recommendation

**Sequenced evidence-depth-first strategy: `PARTIALLY_SUPPORTED`.**

| Recommendation element | Wave 1 classification | Evidence and boundary |
| --- | --- | --- |
| Evidence depth | `SUPPORTED` | Version/history and CI/test evidence were each selected by 5/9 as trust inputs. This supports depth as an input, not as the sole product outcome. |
| Historical context | `SUPPORTED` | Actual-version effort 5/9, historical-state problem 3/9, difficulty mean 3.22/5. |
| Explicit uncertainty | `PARTIALLY_SUPPORTED` | Five prefer explicit uncertainty or UNKNOWN, two prefer confidence scores, and two reject reliance on automation. |
| Provenance | `SUPPORTED` | Traceability mean 4.11/5 and 7/9 high ratings. |
| Centralized evidence | `PARTIALLY_SUPPORTED` | Four respondents supplied a direct centralization signal; explicit evidence-spread pain was 2/9. |
| More automation | `CHALLENGED` | Trust barrier 5/9, false positives 4/9, two would not rely on automated conclusions. |
| Additional human review | `CHALLENGED` | Review burden 3/9 and human review trust requirement only 2/9. |
| Workflow integration cost | `CHALLENGED` | Integration effort barrier 5/9. |
| Problem relevance/frequency | `NOT_ADDRESSED` | Insufficient causal evidence occurs, but upgrade frequency, effort, delay, and impact were not measured; one selected low frequency. |

Wave 1 supports the sequence of improving evidence integrity before expanding automation or breadth. It also shows that depth must serve the affected-repository and trust decisions rather than become open-ended collection.

## Phase 7 decision

**`GO_BOUNDED`: `PARTIALLY_SUPPORTED`.** The exact-ref method and explicit source states align with historical-state, provenance, and missingness preferences. However, Wave 1 does not show that the Phase 7 method changes a real decision, and only 1/9 chose historical reconstruction as the single most useful capability. The method should remain experimental and connected to affected-repository triage, eligible CI/test/version evidence, and clearly stated limits.

Wave 1 does not justify replacing the published baseline, broadening cohorts, adding private sources, or promoting Phase 7 experimental measures to production KPIs.
