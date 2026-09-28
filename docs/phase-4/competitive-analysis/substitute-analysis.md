# Existing-stack and manual substitutes

A realistic possible stack is **Dependabot/Renovate → GitHub PR → dependency review and CI checks → SCA/Socket/Sonatype signal → human reviewer → issues/commits/releases → manual case investigation** [S01,S04,S06,S08,S13,S17,S19]. This is a model, not an observed universal workflow. The frozen Phase 3 public PR sample supports only a narrower visible Dependabot workflow.

| Substitute | What it can solve | Remaining effort/limitation to test |
| --- | --- | --- |
| Manual GitHub search and repository history | Find release, PR, issue, comment and commit evidence [S07]. | Reproduce selection, timing, provenance and sufficiency across repositories. |
| Update PRs and dashboards | Proposed versions, changelogs, pending/ignored state [S01,S09,S10]. | PR merge is not qualified resolved use or recovery. |
| Dependency graph, SBOM, SCA dashboard | Inventory and known security/policy exposure across repos/apps [S03,S05,S13,S18,S19]. | Temporal release-case interpretation may still require manual work. |
| CI logs/checks | Exact runs and failures when available [S06]. | Logs may not answer installed-version or later runtime questions. |
| Internal scripts, notebooks or spreadsheets | Join APIs and annotate case evidence at low marginal tooling cost. | Quality depends on local method, ownership, repeated demand and audit need. |
| Existing analytics/reporting stack | Export Sonatype/GitHub/Socket data and share a dashboard [S05,S18,S19]. | Could be sufficient; PULSE must show a different decision, not a prettier chart. |

The most serious strategic substitute is **competent manual investigation with existing APIs and internal scripts**. No measured time, error rate, frequency or willingness-to-pay evidence establishes that replacing it would be valuable. Stakeholder interviews should ask for a recent case walkthrough and compare actual decisions made with and without a bounded report.
