# Prioritized provisional requirements backlog

MoSCoW priorities follow the [specification](requirements-specification.md) and [CAP map](capability-prioritization.md). `Existing / validated` means the relevant **Phase 2 bounded behavior** exists, not a completed next-version product or stakeholder approval. `Existing / partial` means a material method or workflow gap remains. `Proposed / Not Implemented` means no Milestone 4 implementation occurred. Business and stakeholder requirements are outcomes/needs rather than code units, so their implementation column describes the supporting capability basis. Strength A/B/C/D follows the specification; **E = no stakeholder evidence** for every row. `Yes` in stakeholder dependency means direct primary-research reconciliation is needed to finalize need, ownership, priority, or criterion.

| ID / short name / type | Priority | Rationale and dependency | Strength | Stakeholder dependency | Implementation status |
| --- | --- | --- | --- | --- | --- |
| BR-001 / bounded investigation / Business | Must | Cohort integrity; real scope owner unknown. | A/D | Yes | Existing typed case / validation of use pending. |
| BR-002 / honest evidence states / Business | Must | UNKNOWN and negative boundary. | A/B | Presentation/value yes; integrity no | Existing / validated bounded semantics. |
| BR-003 / traceable human finding / Business | Must | Rejected bot-text candidates; reviewer role pending. | A/B | Yes for workflow | Existing / partial review path. |
| BR-004 / cohort decision view / Business | Should | GAP-07; depends on real portfolio decision. | D | Yes | Proposed / Not Implemented. |
| SR-001 / inspect declared scope / Stakeholder | Must | N-01; owner unvalidated. | A/D | Yes | Existing case data; proposed user workflow / Not Implemented. |
| SR-002 / inspect provenance / Stakeholder | Must | N-03/N-08; source trust threshold pending. | A/B/D | Yes for presentation | Existing provenance / partial view. |
| SR-003 / decide candidate / Stakeholder | Must | P2 independent review; needs-evidence outcome proposed. | A/C/D | Yes | Existing / partial. |
| SR-004 / understand missing evidence / Stakeholder | Must | P2 UNKNOWN; next action unknown. | A/B/D | Yes for utility | Existing status / partial user view. |
| SR-005 / attention suggestion / Stakeholder | Should | Portfolio role and review burden unobserved. | C/D | Yes | Proposed / Not Implemented. |
| SR-006 / completion distinction / Stakeholder | Should | PR disposition ≠ recovery; criterion unknown. | A/B/C/D | Yes | Existing report boundary; proposed disposition / Not Implemented. |
| FR-001 / typed case and cohort / Functional | Must | CAP-01; human setup modality TBD. | A/B | Yes for owner | Existing / validated typed case; proposed interaction Not Implemented. |
| FR-002 / task outcomes / Functional | Must | CAP-02; depends on frozen required/optional policy. | A/B | Source criticality later | Existing / validated bounded behavior. |
| FR-003 / raw provenance and resume / Functional | Must | CAP-02; depends on retained source identity. | A/B | Retention policy later | Existing / validated current sources. |
| FR-004 / exact-ref history / Functional | Must | GAP-02; older-anchor method needed. | A/B | Decision threshold yes | Existing / partial. |
| FR-005 / distinct dependency states / Functional | Must | GAP-03; resolved-version source absent. | A/B | Needed source yes | Proposed method / Not Implemented. |
| FR-006 / source sufficiency / Functional | Must | GAP-05; stage threshold changes need review. | A/B | Expanded threshold yes | Existing / partial. |
| FR-007 / provenance-sensitive candidates / Functional | Must | GAP-04; copied-text mechanism; recall unknown. | A/B/C | Review burden yes | Existing candidate rules / partial; new origin method Not Implemented. |
| FR-008 / three-outcome review / Functional | Must | CAP-06; reviewer authority pending. | A/B/D | Yes | Existing accept/reject / partial; needs-evidence Not Implemented. |
| FR-009 / bounded finding states / Functional | Must | RULE-003–013; no universal adoption/recovery negative. | A/B | Wording/value later | Existing / validated current bounded stages. |
| FR-010 / deterministic report / Functional | Must | CAP-08; unresolved-candidate presentation proposed. | A/B/D | View preference yes | Existing / partial. |
| FR-011 / attention rationale / Functional | Should | CAP-11; depends on portfolio role/factors. | C/D | Yes | Proposed / Not Implemented. |
| FR-012 / recovery eligibility / Functional | Should | CAP-10; depends on source and completion definition. | A/B/D | Yes | Proposed / Not Implemented. |
| NFR-001 / audit chain / Non-functional | Must | CAP-02/08; source retention TBD. | A/B | Trust presentation later | Existing / partial. |
| NFR-002 / replay equivalence / Non-functional | Must | CAP-08; frozen inputs. | A/B | Business value later | Existing / validated in P2 cases. |
| NFR-003 / identity integrity / Non-functional | Must | CAP-06/07; terminal review rule. | A/B | No for core correctness | Existing / partial. |
| NFR-004 / visible failure / Non-functional | Must | CAP-02/07; required/optional classification. | A/B | Source criticality later | Existing / validated current categories. |
| NFR-005 / secrets and source permission / Non-functional | Must | CAP-02; policy/retention unresolved. | B/D | Yes for policy | Proposed safeguard / Not Implemented for future sources. |
| NFR-006 / rule change trace / Non-functional | Should | CAP-02/05/08; convention TBD. | A/B/D | No for integrity, yes for workflow | Proposed / Not Implemented. |

No Could-Have requirement was promoted from CAP-13/14 without user evidence. No Won't-Have item is placed into an implementation backlog. No target for latency, throughput, recall, precision, adoption, or savings is asserted; any such target is **TBD — requires baseline measurement / stakeholder validation**.
