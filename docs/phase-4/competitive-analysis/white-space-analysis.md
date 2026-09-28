# White-space audit and attempted falsification

“Gap” below means a **documented workflow gap in the reviewed public sources as of 2026-09-27**. It does not establish competitor absence, willingness to pay or a defensible product business. The [matrix](competitive-capability-matrix.md) and [source ledger](source-ledger.md) provide traceability.

## Supported documentation gap

The reviewed official pages cover update PRs, CI, SCA, risk scans, organization dependency views and raw repository APIs [S01–S21]. They did **not** document one native workflow that starts with a named release and explicit downstream cohort, reconstructs release-boundary states, separates copied upstream from downstream event evidence, records review and sufficiency, and reports bounded UNKNOWN/recovery conclusions. This is a **composite documentation gap**, not a claim that no competitor can do it. GitHub APIs plus internal scripts are a credible implementation substitute [S07].

## Possible gaps requiring product/customer verification

- **Historical release-boundary reconstruction:** generic/current dependency views and version APIs do not themselves establish the historical repository environment [S03,S15]. Phase 2 PULSE historical coverage is weak, so feasibility is also uncertain.
- **Origin-aware downstream event chain:** PR and issue APIs offer the data [S07], while Phase 2 showed copied upstream text can cause false candidates. Native integrated review method was not verified; existing private/internal tooling may already perform it.
- **Evidence sufficiency and outcome UNKNOWN:** Sonatype exposes unknown *component identity* [S21], and Socket provides scan origin [S18]. Neither is evidence of a complete release-case sufficiency rule, but absence is unproven.
- **Bounded compatibility recovery:** security-remediation dashboards exist [S12,S19,S20]. A general release recovery denominator and decision use remain undefined even within PULSE.

## No meaningful general gap

Dependency inventory, new-version detection, automated update PRs, grouping/approval, vulnerability analysis, package risk, pre-merge review, CI logs, package metadata, and **generic cross-repository risk/inventory views** are already documented [S01–S06,S08–S20]. PULSE should not claim novelty for these. The strongest disconfirmation is that Sonatype and Socket already aggregate organization-level evidence [S18,S19], and Renovate already handles pending/ignored update visibility [S09]. A dedicated release-forensics product could still add value, but only if stakeholders demonstrate a concrete unmet decision and existing-tool friction.
