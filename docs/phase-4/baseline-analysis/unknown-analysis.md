# UNKNOWN is the measured boundary, not a zero event

The verified Phase 2 reports carry one finding for each of five **reported categories** per member. They do not establish which category set a future stakeholder considers required for investigation completion. Thus the counts below are reported-category diagnostics (partial MET-012), not MET-006 completion.

| Case | Adoption readiness UNKNOWN | Observed adoption UNKNOWN | Friction UNKNOWN | Remediation UNKNOWN | Recovery UNKNOWN |
| --- | --- | --- | --- | --- | --- |
| pytest (2 members) | 2/2 | 2/2 | 1/2 | 1/2 | 2/2 |
| urllib3 (6 members) | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 |

The remaining pytest friction/remediation findings for `planetlabs/cosmolog` are **bounded `NO_QUALIFYING_EVIDENCE_FOUND`**, after sufficient pre-release context and stage-source review. They do not prove no friction/remediation occurred. The urllib3 after-only declaration remains UNKNOWN for those stages. Zero accepted findings and zero candidate emissions in a repository do not establish a negative finding.

**Reason availability:** each UNKNOWN has a generic explanation (“required evidence or historical context is incomplete”), while report members have repository-level `missing_sources` labels: historical dependency and downstream releases. Missing resolved-version/runtime evidence is described at the case level. These labels are **multi-label and not linked to each member-stage prerequisite**. MET-013 and MET-015 therefore cannot produce a defensible stage-specific reason distribution/contribution rate. The evidence gaps include method-limited pre-release history, source class not collected, and undefined adoption/recovery eligibility. They are not interchangeable with malformed or missing analytical rows.

All 40 expected member-category finding records (2×5 and 6×5) exist in the two verified reports, with statuses. This is an **analytically correct UNKNOWN**, not a data-quality failure. A missing finding record, unrecognized status, or broken case key would instead be a data-quality defect and block a published rate. No UNKNOWN is recoded as NO or 0% adoption.
