# Evidence-driven design change history

This is a BA decision-history log, **not** a requirements catalogue. It records how observed system/public evidence changed provisional PULSE design assumptions. Dates and approvals are intentionally not invented. Links identify the current source record; no stakeholder endorsement is implied. Future primary research may confirm, refine, or reverse a design choice.

| Change | Earlier assumption or interpretation | Evidence that challenged it | Design decision and boundary | Status |
| --- | --- | --- | --- | --- |
| CH-01 — Collection outcomes | Every file probe had to succeed for a repository task to count. | Live Phase 2 collection encountered optional manifest-path 404s while required tasks succeeded; [Phase 2 findings](../phase-2/phase-2-findings.md). | Preserve required/optional task semantics and verified optional absence, while exposing failed required collection. An optional 404 is not proof the dependency is absent. | System-supported; carry into provisional To-Be. |
| CH-02 — Lifecycle order | Adoption, friction, remediation, and recovery could be read as mandatory chronology. | Phase 1 HTTPX evidence showed same-day compatibility work before a later public friction report; [Phase 1 methodology](../phase-1/methodology.md). | Treat stages as evidence categories, not causal chronology. A later report does not cause earlier remediation. | Methodological boundary; carry forward. |
| CH-03 — Current declaration | Current target declaration could stand in for historical release-time exposure. | Phase 2 exact-ref declaration evidence appeared in only 2/8 repositories and only one stronger pre-release paired path; [P2 historical analysis](../phase-2/historical-dependency-reconstruction.md). | Separate current, historical release-boundary, resolved-version/adoption, and compatibility evidence. Preserve unresolved history. | System-supported gap; acquisition improvement pending. |
| CH-04 — After-only history | An after-release declaration might support a negative release-window friction/remediation finding. | [Phase 2 closure audit](../phase-2/phase-2-findings.md) found the urllib3 after-only path insufficient for release-boundary context. | After-only declaration can count as contextual evidence coverage but yields UNKNOWN for a stricter release-window negative; require parsed pre-release anchor in a paired path under current bounded rule. | Corrected current rule; future thresholds may change only with evidence. |
| CH-05 — Text mentioning failures | A bot PR body that mentions failure or a version could be treated as downstream friction/remediation evidence. | Two Phase 2 firings from one Dependabot PR with copied upstream release notes were independently rejected; [P2 detector findings](../phase-2/detector-evaluation.md). The [public PR sample](secondary-research/github-workflow-analysis.md) also frequently contained copied notes. | Preserve text origin; candidate is not accepted evidence. Require downstream-specific context and human review; do not infer general detector precision or recall from one artifact. | Failure mechanism observed; new detection method unvalidated. |
| CH-06 — PR completion | Merge or closure might be read as migration or recovery. | Milestone 1A records PR disposition but not production state; Phase 2 collected no downstream releases or recovery-eligible set. | Distinguish artifact disposition, target-version use, migration, and recovery; leave unsupported completion UNKNOWN. | Evidence boundary supported; stakeholder completion criterion pending. |
| CH-07 — Universal deep review | Every update might receive the same investigative depth. | Only 6/20 base sampled bot PRs had visible human interaction; the purposive 7/7 discussion set cannot estimate prevalence. | Test explainable triage between routine updates and investigation-worthy cases; do not assume hidden review was absent or that a priority queue is desired. | Design hypothesis only. |

The future [Milestone 2A reconciliation](secondary-research/primary-research-integration-plan.md) should record any stakeholder-driven revisions here before formal requirements are finalized. `CH` IDs are change-history references, not functional requirement IDs.

## Milestone 4 trace links — baseline prepared, no stakeholder approval

The earlier CH-01–07 entries are preserved. The [provisional specification](requirements-specification.md) translates each decision into requirements and [rules](business-rules.md); this is **evidence → requirement change → resulting bounded behavior**, not a claim that new behavior was implemented.

| History ID | Formal trace | Resulting behavior or guard in the provisional baseline |
| --- | --- | --- |
| CH-01 | FR-002, NFR-004; RULE-001/010; AC-FR-002-01 | Optional not-found remains distinct from required failure and analytical sufficiency. |
| CH-02 | FR-009/010; RULE-008/013; AC-FR-009-01 | Lifecycle categories and report wording do not impose stage order or causality. |
| CH-03 | FR-004/005; RULE-002/003; AC-FR-004-01/AC-FR-005-01 | Current declaration, release-boundary evidence, and target-version observation stay distinct. |
| CH-04 | FR-004/006/009; RULE-009; AC-FR-004-01 | After-only declaration cannot support a negative release-window finding. |
| CH-05 | FR-007/008/009; RULE-004/005/007; AC-FR-007-01/AC-FR-008-01 | Copied upstream text stays tentative and rejected candidates cannot become findings. |
| CH-06 | SR-006, FR-012; RULE-012; AC-SR-006-01/AC-FR-012-01 | PR disposition, target-version use, and recovery are separate. |
| CH-07 | BR-004, SR-005, FR-011; RULE-011; AC-FR-011-01 | Attention suggestions are explainable and human-overrideable only if a real portfolio decision is validated. |

At the later reconciliation checkpoint, a change record should retain the response source, affected IDs, proposed wording/priority change, reason, decision authority, updated AC/RTM/backlog links, and whether the result is confirmed, modified, split, removed, added, or unresolved. Level B integrity rules require an explicit evidence tradeoff review rather than silent relaxation. No such primary-research change has occurred yet.

## Milestone 5 validation correction

| Change | Trigger and old interpretation | New interpretation / rationale | Impacted baseline and verification | Status |
| --- | --- | --- | --- | --- |
| CH-08 | Milestone 5 code/test audit found `AnalystDecision` and `test_precision_excludes_unresolved_and_handles_zero_denominator` already accept a reasoned `NEEDS_REVIEW`; Milestone 4 described the third review outcome as proposed. | The **bounded three-outcome ledger behavior exists**. This does not validate a stakeholder review role, interface, or acceptable workload. | FR-008 status and backlog implementation label corrected; AC-FR-008-01 and RTM link remain; [UAT-016](uat-test-cases.md) records current-system evidence. Requirement wording and priority unchanged. | Evidence-based status correction; no stakeholder approval. |
