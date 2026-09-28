# Phase 4 Milestone 1C — market landscape and solution alternatives

## Classification

**PARTIAL.** Current official documentation clarifies substantial competitive overlap and a narrow *possible* release-forensics gap. Differentiation and a final product recommendation remain stakeholder-dependent. Research/access date **2026-09-27**; conclusions describe **documented capabilities observed as of that date**, not an exhaustive product trial or proof of absent features.

## Tools researched

The 22-source [machine](competitive-analysis/source-ledger.json) and [human](competitive-analysis/source-ledger.md) ledgers cover GitHub Dependabot, repository/dependency graph/review/Actions/API, Mend Renovate, Mend Remediate/SCA, Snyk Open Source, deps.dev, PyPI, Socket and Sonatype Lifecycle. All material product claims refer to official documentation. Mend Classic Remediate and GitHub Enterprise organization insights have edition/availability caveats.

## Market categories

Update automation, package intelligence, vulnerability/SCA, pre-merge risk review, CI/repository evidence and organization risk views all overlap a possible release investigation. Several tools span categories; none was classified as a proven direct end-to-end release-forensics competitor from this representative documentation review. [Category map](competitive-analysis/market-category-map.md).

## Major jobs to be done

Inventory, detect release, propose upgrade, assess risk, validate pre-merge, inspect upstream context, reconstruct historical state, prove resolved target version, correlate downstream events, trace response, assess bounded recovery, compare a declared cohort, expose provenance/UNKNOWN and decide whether investigation is worthwhile. These [jobs](competitive-analysis/jobs-to-be-done.md) are vendor-neutral.

## Capability overlap

The [16-capability taxonomy](competitive-analysis/capability-taxonomy.md) and [source-traceable matrix](competitive-analysis/competitive-capability-matrix.md) show strong overlap in proposals, grouping, notes, risk, checks and generic cross-repo views. Matrix `NF` means “not found in reviewed documentation,” never product absence.

## Capabilities well served by existing tools

Dependabot/Renovate update and manage PRs; GitHub exposes dependency graphs, dependency review, CI history and PR evidence; Mend/Snyk/Socket/Sonatype handle significant security/policy risk; PyPI/deps.dev expose package facts. GitHub organization insights, Socket scans, Mend dashboards and Sonatype dashboards already cross repository/application boundaries [S01–S22].

## Possible PULSE gaps

The reviewed sources did **not** document a single native workflow combining exact release-boundary pairing, downstream issue/PR origin separation, a declared target-release cohort, human forensic review and evidence sufficiency/UNKNOWN. This is a **composite documentation gap**, not a claim of uniqueness, competitive absence or validated demand. Historical reconstruction, actual resolved version and bounded recovery remain especially uncertain in PULSE itself. [White-space audit](competitive-analysis/white-space-analysis.md).

## Unsupported differentiation claims

“Only multi-repository view,” “first forensic tool,” “no competitor does this,” “automated impact/recovery,” “actual adoption from PR merge,” and “time saved” are rejected. Cross-repo and security remediation capabilities are documented elsewhere; PULSE currently lacks valid adoption, recovery and labor denominators. [Guardrails](competitive-analysis/positioning-guardrails.md).

## Manual substitutes

GitHub search/history/APIs, update PRs, CI logs, SCA dashboards, spreadsheets and internal scripts can assemble a case. Whether the assembly is too slow, unreliable or unactionable has not been measured. Alternative A must remain a viable outcome. [Substitutes](competitive-analysis/substitute-analysis.md).

## Build versus integrate findings

Consume registry facts; integrate SCM/CI/SCA references; do not recreate update bots, scanners, CI or generic dashboards. A narrow evidence-pairing, origin/sufficiency and human-reviewed case report may be worth testing, while target-version and recovery claims must wait for qualified sources and rules. [Boundary table](competitive-analysis/build-vs-integrate.md).

## Strategic alternatives

A existing tools/do nothing is the valid status quo; B bounded report is a **provisionally supported research slice**; C interactive human-review workspace is stakeholder-dependent; D automated release-impact platform is unsupported at current evidence quality. No weighted score or dollar ROI was invented. [Alternatives](competitive-analysis/strategic-alternatives.md).

## Provisionally preferred path

Test **B** against a stakeholder-owned recent investigation while preserving A as the comparator. Move toward C only if real review/handoff work makes a report insufficient. This is not a final product or implementation recommendation.

## Competitive risks

Adjacent expansion, API/script substitutability, native-workflow preference, rare need, private-data access, UNKNOWN-heavy output, integration cost and overclaiming are documented as evidence versus scenarios in [risks](competitive-analysis/competitive-risks.md). No probability or market-size figures are asserted.

## PULSE boundary implications

Retain declared case/cohort, provenance, sufficiency, UNKNOWN and human acceptance; narrow historical/adoption/recovery claims; integrate existing data/tool sources; remove generic cross-repo ranking from a core differentiation claim unless stakeholders validate it. The formal Phase 3 requirement baseline is unchanged. [Boundary reassessment](competitive-analysis/pulse-boundary-reassessment.md).

## Consulting findings

The [issue tree](competitive-analysis/consulting-issue-tree.md) cannot yet answer “should PULSE be a dedicated product?” positively: user need, existing-tool adequacy, evidence access, decision improvement and operational viability are unvalidated. [Findings](competitive-analysis/consulting-findings.md) retain counterarguments and disconfirming overlap.

## PA implications

Proposed future work: source-origin and sufficiency breakdowns, comparison against the existing-stack answer, actual reviewer events, and continued unavailability of adoption/recovery until qualified. The [change list](competitive-analysis/pa-proposed-change-list.md) does **not** revise metric v1.0.

## Stakeholder questions

What recent release case changed a decision? Which current tools and internal scripts were used? What remained unknown? Did a cross-repo view suffice? Who reviews candidate evidence, and what would an incomplete report cause them to do? What proves installed/used target version and meaningful recovery? [Follow-up map](competitive-analysis/stakeholder-followup-map.md) leaves the already-sent form unchanged.

## PostgreSQL implications

If authorized later, reference external provider/edition/object/ref/capture provenance rather than replicate dependency, CI or SCA systems. No operational PR fact follows from the small frozen public sample. [Data-model note](competitive-analysis/postgresql-implications.md).

## Implementation gate

**Phase 3 HOLD remains binding until authorized primary stakeholder reconciliation changes the decision.** No PostgreSQL, dbt, Power BI, collector, detector, product feature, PR or merge is part of this milestone. Phase 4 Milestone 2 has not started.

## Validation

The ledger parses as JSON with **22 unique official-source IDs**, all dated 2026-09-27. The capability matrix covers each of C01–C16 exactly once for each of nine compared tool scopes, and local links in the 19 Milestone 1C Markdown files resolve. `uv run ruff check .` passed; `uv run pytest -p no:cacheprovider` passed **134 tests**. Existing behavioral code and metric v1.0 were not changed.
