# Consulting issue tree: should PULSE be a dedicated release-forensics product?

The branches are decision tests, not a presumption to build. Current evidence and next test are separated so a negative answer can stop the thesis.

| Branch | What must be true? | Evidence now | Missing test / decision consequence |
| --- | --- | --- | --- |
| Meaningful problem | A named owner repeatedly needs a release-bounded answer that affects action. | Phase 3 public PRs show workflow traces, not business need. | Recent stakeholder case, frequency, consequence; no case → stop. |
| Adequately solved already? | Existing bot/SCM/SCA/CI/manual stack leaves a concrete decision unresolved. | Strong adjacent overlap [S01–S20]. | Demonstrate current workflow; adequate solution → choose A. |
| Obtainable evidence? | Historical refs, downstream signals, version source and CI can be accessed with enough completeness. | Phase 2 collection/replay works but historical/target-version gaps remain. | Authorized source trial; incomplete critical chain → narrow claims or stop. |
| Better decision? | A bounded report changes or strengthens a real decision beyond current notes. | No measured improvement. | Side-by-side case review; unchanged decision → reject extra product complexity. |
| Operationally viable? | Review burden, ownership, latency, privacy and source retention are acceptable. | Review ledger exists; user/organization process unknown. | Observe reviewer and access workflow; excessive burden → reporting-only or stop. |
| Differentiated enough? | The composite release-case method matters beyond existing inventory/risk views. | Documentation gap possible; cross-repo overlap strong [S05,S18,S19]. | Competitor trial plus stakeholder use; no distinctive value → integrate/stop. |
| Build versus integrate? | New code is limited to evidence assembly/sufficiency/review that sources do not already provide. | Registry, PR, CI and SCA sources exist [S06,S07,S13,S15,S16]. | Choose authoritative source per evidence type and rights. |
| What remains unknown? | User, use frequency, resolved-version source, recovery rule, confidence and acceptable UNKNOWN. | All open in Phase 3 HOLD. | Primary stakeholder reconciliation before requirements or implementation changes. |

**Decision tree outcome today:** A remains viable; B is a bounded validation slice; C depends on user workflow; D is unsupported. The root cannot yet be answered “yes.” [Strategic alternatives](strategic-alternatives.md).
