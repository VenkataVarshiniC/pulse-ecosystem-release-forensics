# Frozen public PR workflow dataset contract

**Population B** is the Phase 3 secondary-research sample, not the Phase 2 eight-repository forensic population (Population A). Source: [observations](../../phase-3/secondary-research/github-pr-observations.jsonl), [candidate frame](../../phase-3/secondary-research/github-pr-candidate-frame.json), [codebook](../../phase-3/secondary-research/github-pr-codebook.md), and [sampling protocol](../../phase-3/secondary-research/github-pr-sampling-protocol.md). The analytic grain is one **sample × repository × PR**. The composite key is `(sample_type, lower(repository), pr_number)`; the canonical URL is the source trace. There are 20 base and seven purposive discussion rows, frozen at the 2026-09-27 observation cutoff. No PR is added or recoded here.

| Analytic concept | Frozen field / derivation | Boundary |
| --- | --- | --- |
| Identity and sample | `sample_type`, `repository`, `pr_number`, `url`, `observed_on` | Base and discussion never pooled for prevalence. |
| Dependency and versions | `dependency`, `previous_version`, `proposed_version`, `dependency_changes` | Grouped PRs have null scalar versions; use their component list. |
| Initiator / mechanism / trigger | `initiator`, `update_mechanism`, `trigger` | All observed bot/Dependabot; trigger remains unknown. |
| File type | `changed_files`; `evidence_present.manifest_diff/lockfile_diff` | Presence of a changed file, not historical installed state. |
| Automated upstream context | `copied_upstream_release_text`, `evidence_present.release_notes/changelog/compatibility_score/linked_upstream_issue_in_copied_text` | Badge/link is not a verified score; upstream link is not downstream failure. |
| Downstream statement / human behavior | `downstream_statement_present/kind`, `human_interaction_present`, `human_review_present`, `visible_human_interaction_count`, `approval`, `changes_requested`, `bot_command_usage`, `maintainer_decision` | Public visibility only; bot commands differ from technical discussion. |
| Concern / exception | `concerns`, `additional_work`, `reason_for_close` | Explicit multi-label taxonomy; no severity or labor inference. |
| Code/test/config change | `additional_work.production_code_modification/test_modification/configuration_modification` | Checked visible diff; no hidden work inference. |
| Rebase / supersession | `additional_work.rebase_recreation`, `bot_command_usage`, `reason_for_close` | A rebase request and bot up-to-date reply do not prove rebase completed. |
| Disposition / duration | `outcome`, `reason_for_close`, `pr_resolution_duration_hours`, frame UTC creation/end timestamps | Elapsed open-to-terminal interval, never human work time. |
| Completion and links | `completion_signals`, `supporting_urls`, `evidence_present.linked_downstream_issue` | Merge is one observable signal, not compatibility or recovery proof. |

`null` means not established. `false` means checked and not observed in accessible public evidence. A substantive discussion flag is **derived only** from `downstream_statement_kind == substantive_review_comment`; bot commands remain a distinct kind. A “retained older version” label is grounded in the coded `version_constraint` concern and [uvicorn#2549](https://github.com/Kludex/uvicorn/pull/2549), not inferred from a generic version range. The original JSONL remains the source of truth; [workflow-metrics.json](workflow-metrics.json) is a reproducible analytic derivative.

The bounded search selected earliest result pages for `bump` titles; all 27 selected PRs were created on the first day of their half-year slice and all are Dependabot. Seven discussion cases were purposively selected for interaction after a three-case slice shortfall. These observations cannot estimate the broader Python or PULSE user population.
