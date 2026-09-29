# Screen-to-API and data-source matrix

Capability names refer to the [backend specification](api-capability-spec.md), not implemented URLs. All reads carry explicit case version and selected snapshot; normal consumption is limited to `PUBLISHED_VALIDATION`. `analytics` is a governed read-only summary source, `core` operational evidence/review, and `ingestion` task/source provenance. No screen writes raw or published evidence.

| Screen | Data need | Backend capability | Read/write | Source and current gap |
|---|---|---|---|---|
| Investigation List | Release/case/window, cohort size, published snapshot state | List investigations | Read | `core.investigation_case`, release, membership, snapshot; no case-creation UI. |
| Investigation Overview | All members, collection/historical/candidate/finding summaries | Get investigation and cohort | Read | `core` membership plus `analytics.bridge_case_repository` and `fct_repository_investigation`; no automated risk priority. |
| Repository Investigation | Selected member, tasks, observations, stage findings, candidates | Get repository investigation; list findings/candidates/evidence | Read | Selected `core` records plus mart summary; comprehensive installed-version evidence absent. |
| Evidence Explorer | Captures, exact ref/path, clocks, source/task outcome | List evidence and historical observations; get artifact detail | Read | `core.evidence_artifact`, observation/pair; `ingestion` task/run/source; incomplete historical anchor stays visible. |
| Finding Detail | Literal state, assessment, reasons, actual support edges | Get finding detail; get artifact detail when supported | Read | `core.lifecycle_finding`, assessment/source reasons, support; current replay has no positive finding-support edges. |
| Candidate Review | Candidate/rule/artifact, current decision and inherited lineage | List/get candidates and reviews; conditional submit review | Read; **conditional write only for new eligible DRAFT** | `core.candidate`, selected `analyst_review`, `core.replay_candidate_lineage`; current published candidates read-only. Reviewer authority and DRAFT write target are gated. |
| Artifact / Provenance Detail | Original locator, digest, method, run/task, linked claims | Get artifact/provenance detail | Read | `core.evidence_artifact`/external reference and `ingestion` source/task/run; protect credentials and sensitive locator. |

The operational application uses core/ingestion for record-level traceability. It may use the published marts for cohort aggregates without becoming a copy of Power BI. The deferred [Power BI build](../../phase-4/m4-2/power-bi-build-handoff.md) owns aggregate analytical presentation; it does not submit candidate reviews or replace repository evidence navigation.
