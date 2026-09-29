# Seven operational screens

| Screen | Route below `/investigations` | API read | Implemented behavior |
|---|---|---|---|
| Investigation List | `/` | `GET /investigations` | Package/release, case, declared member count, window and publication state. Opens the API-selected case version and snapshot. |
| Investigation Overview | `/:caseVersionId` | `GET /investigations/{case_version_id}` | All declared members, including zero-candidate members, literal finding counts, release/window and snapshot/rule context. |
| Repository Investigation | `/:caseVersionId/repositories/:repositoryId` | `GET .../repositories/{repository_id}` plus candidate list when present | Declaration and resolved observation displayed separately; historical pair state, source task outcomes, five category findings and candidate links. |
| Evidence Explorer | `.../evidence` | `GET .../evidence` | Source grouping, exact source/ref/path filters, API cursor pagination at 25 per page, capture method, event/retrieval clocks, abbreviated digest and observation context. UUID order is not described as chronology. |
| Finding Detail | `.../findings/:findingId` | `GET .../findings/{finding_id}` | Literal status, sufficiency, reason and source reasons, rule/source set, bounded interpretation and only recorded support edges. |
| Candidate Detail / Review | `.../candidates/:candidateId` | `GET .../candidates/{candidate_id}` and candidate list | Detector origin/rule/span, inherited/direct review provenance, shared-artifact peers, immutable published review notice. No active review controls. |
| Artifact / Provenance | `.../artifacts/:artifactId` | `GET .../artifacts/{artifact_id}` | Source/provider/ref, capture method, two clocks, digest, task/run context, allowed public locators and recorded candidate/finding links. |

Every route after the list requires a validated `snapshot_id` query parameter. Breadcrumbs return to the exact case and repository; they do not select a newer snapshot. The artifact path is repository-scoped, matching M5.2's actual contract rather than an unscoped global artifact URL.

The current published cohort contains two cases, eight declared repositories, 40 findings and two inherited rejected candidates from one artifact. These figures are validation expectations, **not** frontend constants or product metrics. The API supplies rendered counts. Lifecycle categories are forensic questions; remediation or compatibility work can precede a later public friction report. The UI makes no causal ordering claim.
