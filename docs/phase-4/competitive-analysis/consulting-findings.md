# Consulting findings with disconfirming evidence

Research date: **2026-09-27**. Source IDs refer to the [22-source ledger](source-ledger.md). Confidence grades assess the stated finding, not vendor quality or market share.

## Finding 1 — Surrounding workflow is well served

**Question:** Must PULSE own discovery, update PRs, security checks or CI? **Evidence:** GitHub Dependabot, Renovate, GitHub dependency review/Actions, Snyk, Mend, Socket and Sonatype document these jobs [S01–S04,S06,S08–S14,S17,S20]. **Finding:** No meaningful general gap in those capabilities. **Confidence:** High for documented overlap. **Implication:** Consume/integrate, do not rebuild. **Counterargument:** Some organizations may have poor configuration or fragmented vendor coverage. **Remaining uncertainty:** Real stack and access. **Evidence needed next:** Observe one organization's actual tools and gaps.

## Finding 2 — “Multi-repository” alone is not a differentiator

**Question:** Does PULSE uniquely compare repositories? **Evidence:** GitHub organization dependency insights, Socket organization scans, Mend organization dashboards and Sonatype cross-application reports exist [S05,S18,S19,S22]. **Finding:** A generic cross-repo dependency/risk view is already served. **Confidence:** High. **Implication:** Narrow to a declared *target-release* cohort case if useful. **Counterargument:** Existing views emphasize current risk, not historical release outcomes. **Remaining uncertainty:** Whether target-release comparison changes action. **Evidence needed next:** Stakeholder walkthrough and side-by-side existing view.

## Finding 3 — A composite case-method gap is plausible, not proven market whitespace

**Question:** Is a release-bounded downstream evidence chain natively served? **Evidence:** Reviewed docs offer raw PR/API, history, CI and inventories [S03,S06,S07,S15]; no reviewed source documents the entire C09+C11+C12+C15+C16 combination. **Finding:** A narrow **documentation gap** exists in this representative review. **Confidence:** Medium for reviewed-document comparison; low for market absence. **Implication:** Test bounded reporting (Alternative B) before a workspace. **Counterargument:** Internal scripts and unreviewed/enterprise features may already assemble the same answer. **Remaining uncertainty:** User need, frequency and willingness to accept UNKNOWN. **Evidence needed next:** Actual case solved by current stack versus PULSE-style report.

## Finding 4 — PULSE's current evidence cannot support broad impact claims

**Question:** Could PULSE now automate adoption, recovery and prioritization? **Evidence:** Phase 2 historical context is weak and copied upstream text produced two rejected candidate firings; Phase 4 M1A marks target-version/recovery/recall unavailable. Existing SCA products already prioritize security risk [S12,S18,S19,S22]. **Finding:** Automated release-impact platform (D) is unsupported. **Confidence:** High for current PULSE limitations; no claim about future impossibility. **Implication:** Retain human review, explicit missingness and narrow reporting. **Counterargument:** Better sources could improve coverage later. **Remaining uncertainty:** Obtainable organizational evidence and validated decision. **Evidence needed next:** Authorized source trial and stakeholder acceptance criteria.

## Finding 5 — The key substitute may be a competent human with existing tools

**Question:** Is a new product needed at all? **Evidence:** GitHub exposes PR/review/commit sources and CI logs [S06,S07]; Renovate dashboards and SCA views supply more context [S09,S18,S19]. **Finding:** Manual investigation and internal scripts are credible substitutes. **Confidence:** High that substitute is technically possible; low on its cost/quality in actual organizations. **Implication:** A should remain an allowed outcome. **Counterargument:** Repeatability and provenance may matter in a high-stakes, frequent workflow. **Remaining uncertainty:** Frequency, error/consequence, reviewer labor. **Evidence needed next:** Recent incident reconstruction with task time and changed decision observed, not recalled estimates alone.

**Synthesis:** No final product recommendation is justified. The smallest defensible next test is Alternative B alongside the existing stack, with C contingent on demonstrated interactive review need. Phase 3 HOLD remains binding.
