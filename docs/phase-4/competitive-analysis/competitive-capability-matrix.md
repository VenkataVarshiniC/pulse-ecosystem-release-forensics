# Documented competitive capability matrix

Research date **2026-09-27**. Codes map to the [neutral taxonomy](capability-taxonomy.md); source IDs to the [official-source ledger](source-ledger.md). **D** = documented native capability; **P** = partial capability relative to the exact taxonomy definition; **I** = possible by integrating/configuring documented data or tools, *not* a verified turnkey feature; **NF** = not found in reviewed documentation; **NV** = not verified for this edition/ecosystem. A code listed in one column is excluded from the others. **NF never means “No.”** This is a documentation audit, not hands-on product testing.

| Product/scope | D: documented native | P: partially addresses defined capability | I: assembly/integration possible | NF: not found in reviewed docs | Evidence |
| --- | --- | --- | --- | --- | --- |
| GitHub Dependabot | C03,C04,C05 | C01,C06 | C07,C08,C11 | C02,C09,C10,C12,C13,C14,C15,C16 | [S01](source-ledger.md),[S02](source-ledger.md); separate GitHub services below. |
| Mend Renovate | C03,C04,C05 | C01 | C06,C07,C08,C11 | C02,C09,C10,C12,C13,C14,C15,C16 | S08–S10; Dependency Dashboard handles pending/ignored updates, not forensic cohort. |
| GitHub graph/review/Actions/API | C06,C07,C08 | C01,C02,C12,C15 | C03,C04,C05,C09,C10,C11,C13,C16 | C14 | S03–S07. Current inventory does not itself satisfy named-ref C01; C12 is org inventory only; C15 has source/ref, not end-to-end sufficiency/UNKNOWN. C10 requires qualified submitted/external resolved evidence. |
| Mend SCA + Classic Remediate | C03,C06 | C01,C02,C05,C07,C12,C13,C14 | C04,C08,C11 | C09,C10,C15,C16 | S11,S12,S22; edition-specific; C12 is risk/project aggregation, C13/C14 are **security-only** remediation trends, not general compatibility recovery. |
| Snyk Open Source | C01,C06,C07 | C02,C03,C13 | C08,C11 | C04,C05,C09,C10,C12,C14,C15,C16 | S13,S14; C03 fix/upgrade integration depends on SCM/ecosystem; cross-repo release view not verified. |
| deps.dev | C02 | C01,C06 | C09 | C03,C04,C05,C07,C08,C10,C11,C12,C13,C14,C15,C16 | S15; generic resolved graph differs from actual historical repository state. |
| PyPI | C02 | C06 | — | C01,C03,C04,C05,C07,C08,C09,C10,C11,C12,C13,C14,C15,C16 | S16; API includes known-vulnerability listing for releases; not a full SCA workflow. |
| Socket | C06,C07 | C01,C02,C08,C12,C15 | C03,C11,C13 | C04,C05,C09,C10,C14,C16 | S17,S18; organization scans include PR/commit links, but are risk scans. |
| Sonatype Lifecycle | C06,C07 | C01,C02,C03,C12,C13,C15 | C08,C11 | C04,C05,C09,C10,C14,C16 | S19–S21; component “Unknown” is identity uncertainty, not forensic outcome UNKNOWN. |

**Counterevidence to a broad gap:** GitHub already provides dependency inventory, PR review, CI and an organization view; Renovate has a dashboard and closed/ignored-update handling; Socket exposes organization scans by repository/PR/commit; Sonatype aggregates component risk across applications. Thus “cross-repository evidence,” “review,” “uncertainty” or “auditable dashboard” **alone** are not credible unique claims.

**Narrower unverified composite:** The reviewed documentation did not establish a single native flow combining C09 + C11 + C12 + C15 + C16 for a *declared target release*, or C14 for general compatibility recovery. GitHub APIs and internal scripts could assemble much of it; this is a **documentation gap**, not proven customer need or competitor absence. PULSE itself has only bounded Phase 2 prototypes: historical coverage is weak, two urllib3 candidates were rejected, target-version and recovery metrics remain unavailable. It cannot claim to deliver the full composite today.
