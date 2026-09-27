# Initial stakeholder-needs hypotheses

These are questions for discovery, **not validated needs or FR/NFR/BR requirements**. All statuses are `hypothesis`. The source column identifies a project observation or product boundary, not testimony from a stakeholder. Evidence strength is for the *need*, not the underlying technical observation; it is low until genuine user evidence is collected. See [Phase 2 BA inputs](phase-2-ba-inputs.md) and [the stakeholder register](stakeholder-register.md).

| Need ID | Candidate stakeholder | Hypothesized need | Source | Need evidence strength | Discovery question | Status |
| --- | --- | --- | --- | --- | --- | --- |
| N-01 | Dependency/platform engineer | Know which owned repositories warrant attention after a release. | Repository-bounded PULSE thesis; BA-01, BA-08 | Low: no user validation | How is the affected set found and prioritized today? | hypothesis |
| N-02 | Dependency/platform engineer; technical lead | Know what historical or installed dependency state supports exposure. | BA-01, BA-02, BA-06 | Low: technical gap only | What version/state is necessary for the decision? | hypothesis |
| N-03 | Investigator; reviewer | See why a repository or event was flagged and trace each conclusion to source evidence. | PULSE provenance boundary; BA-09 | Low: no user validation | Who reviews conclusions, and what proof do they request? | hypothesis |
| N-04 | Investigator; technical lead | Distinguish known evidence, bounded no qualifying evidence, and missing evidence. | BA-05; Phase 2 UNKNOWN-heavy output | Low: no user validation | What do you do with an inconclusive result? | hypothesis |
| N-05 | Investigator | Avoid reviewing irrelevant candidates without missing consequential signals. | BA-04 | Low: no user validation | Which review errors cost you more, and what volume is tolerable? | hypothesis |
| N-06 | Technical lead; manager | Understand when a migration is complete or recovery can be asserted. | BA-03 | Low: no user validation | What event or artifact marks completion in your workflow? | hypothesis |
| N-07 | Engineer responsible for multiple repos | Compare release-impact evidence across the owned set. | BA-08; proposed primary-user hypothesis | Low: no user validation | Do you actually make cross-repository comparisons, or work case by case? | hypothesis |
| N-08 | Auditor or reviewer | See collection method, completeness, and replay boundary. | BA-09 | Low: no user validation | Does provenance change trust, review, or communication? | hypothesis |

Discovery may reject, split, or replace these hypotheses. A technical limitation alone is not a mandate to build a feature.
