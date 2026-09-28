# Secondary workflow dashboard prototype readiness

This is a **specification**, not a Power BI build. It does not replace the separate [Phase 2 forensic visual audit](../baseline-analysis/dashboard-readiness.md). All percentage labels must state “of 20 selected base PRs,” and the seven purposive cases may appear only as linked examples or a separately labeled case ledger.

| Proposed visual | Data and denominator | Readiness | Guardrail |
| --- | --- | --- | --- |
| Disposition bar with nested closure reasons | 9 merged / 11 closed of 20; closure reasons 8/11 superseded, 2/11 no longer needed, 1/11 ignored | READY_WITH_LIMITATION | Never label merge compatibility success or closure failure. |
| Human-interaction split and merge cross-tab | 6/20 interaction; 5 merged/1 closed within six; 4 merged/10 closed within 14 without interaction | READY_WITH_LIMITATION | No causal reading or inference about private review. |
| Exception taxonomy matrix | 12/20 any label; multi-label counts and zero/one/multiple | READY_WITH_LIMITATION | Administrative closure separate from technical concern; no severity ranking. |
| Evidence-source presence matrix | Manifest/lockfile, notes, changelog, badge, copied text, local comment | READY_WITH_LIMITATION | Categories overlap; distinguish automatic upstream versus downstream origin. |
| PR elapsed-time dot/box distribution | 20 timestamped terminal base PRs, median 167.25h, IQR 607.7h | READY_WITH_LIMITATION | Show long tail and “elapsed PR time,” not work time. |
| Purposive discussion case ledger | Seven named PRs with comments, commands, test concern and disposition | READY_WITH_LIMITATION | No percentages or prevalence comparison. |
| User impact, adoption/recovery, time saved, detector precision | No valid PR-workflow denominator/source | BLOCKED_DATA | No proxy KPI. |

Audience, intended decision, accessibility, filters, annotation language and whether a user would need any of these views remain **BLOCKED_STAKEHOLDER**. No dashboard software or data mart is implemented.
