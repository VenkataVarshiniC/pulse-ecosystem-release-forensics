# Stakeholder follow-up map for future interviews

This does **not** alter the already-sent Google Form. It adds prompts for authorized follow-up and later [Phase 3 reconciliation](../../phase-3/stakeholder-reconciliation-framework.md). Do not assume a respondent has used any specific vendor.

| Competitive observation | Ask about a recent real case | What would change the hypothesis |
| --- | --- | --- |
| Bots and Renovate dashboards already handle update proposals/deferrals [S01,S09]. | Which update was delayed/ignored, and what decision remained unanswered after the PR/dashboard? | If none, remove update-management overlap from PULSE scope. |
| GitHub, Socket, Mend and Sonatype have cross-repo/app views [S05,S18,S19,S22]. | Show the current view used for one dependency release across repositories. What could it not establish? | If view suffices, remove generic cohort comparison feature. |
| GitHub PR, issue, commit and CI sources exist [S06,S07]. | Reconstruct the last investigation: exact source order, decisive artifact, missing artifact and time boundary. | If manual assembly is easy/reliable, prefer Alternative A; otherwise test B. |
| Package/version metadata is abundant, actual historical use is different [S03,S15,S16]. | What evidence proves the target version was installed/resolved at the relevant point? | Refine or drop adoption question if source inaccessible/unneeded. |
| PULSE's reviewed candidates require human judgment. | Who would review a copied-upstream candidate, how many per case, and what error matters more? | Interactive C only if reviewer workflow/burden supports it. |
| Security tools already report remediations [S19,S22]. | Does a compatibility recovery decision exist apart from vulnerability closure? Who owns it, and what window? | Deprioritize recovery metrics if no distinct decision. |
| Honest UNKNOWN may dominate. | Show a real incomplete report: what action, evidence request or escalation would it trigger? | If no action follows UNKNOWN, rework/stop PULSE value thesis. |
| Reports may duplicate internal scripts. | Ask for current script/spreadsheet/dashboard and compare its answer with a bounded case report. | Accept A if current tool already changes the same decision. |

Record role, direct versus secondhand experience, counterexamples and contradictory accounts separately. Primary research must precede formal boundary/metric revisions or implementation authorization.
