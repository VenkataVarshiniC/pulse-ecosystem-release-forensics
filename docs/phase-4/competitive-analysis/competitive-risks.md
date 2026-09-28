# Competitive and execution threats

These are **scenarios**, except where an existing capability is explicitly documented. Source IDs refer to the [ledger](source-ledger.md). They are not market probability estimates.

| Risk | Documented evidence versus scenario | Consequence / test |
| --- | --- | --- |
| Adjacent tools extend into release forensics | Documented: GitHub cross-repo inventory [S05], Socket organization scan/PR/commit views [S18], Sonatype cross-application risk [S19]. Expansion into the exact PULSE composite is **scenario**. | Monitor product docs; do not sell generic multi-repo view as differentiation. |
| Manual/API substitute is sufficient | Documented: GitHub PR APIs and CI logs [S06,S07]. Whether teams already have adequate scripts is **unknown**. | Ask for actual recent investigation and artifacts; compare decisions. |
| User prefers native GitHub/SCA workflow | Existing PR checks and dashboards documented [S04,S09,S14,S17,S20]; preference is **unknown**. | Observe where decisions happen, not stated feature interest alone. |
| Need is too infrequent or low consequence | No primary evidence of frequency or impact. | Establish trigger, owner, decision and cost of wrong/incomplete answer before build. |
| Private evidence inaccessible | Public APIs exist [S07]; private permissions, retention and CI access vary. | Test least-privilege case access and source completeness with an authorized organization. |
| UNKNOWN-heavy reports are not actionable | Phase 2 historical/target-version gaps are observed locally; user utility unknown. | Put incomplete report in front of decision owner; ask what next action it supports. |
| Integration/identity cost dominates | Multiple sources/editions and historical ref matching are required [S03,S06,S07,S11,S15,S18]. | Trace one case end to end before architecture expansion. |
| Automated classification overclaims | Phase 2 copied-upstream false positives and unavailable recall source are observed. | Retain human review and abstention; do not claim automated impact accuracy. |

There is no fabricated probability, revenue effect, TAM or implementation estimate.
