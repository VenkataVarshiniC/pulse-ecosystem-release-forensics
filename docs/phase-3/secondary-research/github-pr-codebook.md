# Public PR observation codebook

Unit: one selected public GitHub pull request. The frozen [sampling protocol](github-pr-sampling-protocol.md) and [candidate frame](github-pr-candidate-frame.json) determine membership. Code only what is visible in the PR at the 2026-09-27 observation cutoff. `null` means not established; `false` means checked and not observed in the accessible record. A PR can show several categories. Search-result metadata and bot boilerplate are not proof of a downstream failure.

## Required identity and provenance

Record `sample_type` (`base` or `discussion`), `repository`, `pr_number`, canonical `url`, `observed_on`, title, changed-file paths, dependency and old/new version where identifiable. Record material comment, review, or linked-issue URLs in `supporting_urls`. The subject is the workflow, not contributors; do not retain unnecessary personal data.

## Initiation and evidence

- `initiator`: `bot`, `human`, or `unclear`, based on the PR author identity, not title alone.
- `update_mechanism`: `dependabot`, `renovate`, `manual`, `other`, or `unknown`. A human author alone does not prove a manual mechanism.
- `trigger`: one of `scheduled_update`, `security`, `compatibility`, `maintenance`, `deprecation`, or `unknown`, with a source URL or explicit text. A Dependabot PR alone does not prove scheduling.
- `evidence_present`: checked booleans for release notes, changelog, compatibility score, manifest diff, lockfile diff, linked upstream issue, linked downstream issue, test results, CI/check discussion, security advisory, documentation, and other evidence. Distinguish an actual passed/failed check from merely a PR mentioning CI.
- `linked_upstream_issue_in_copied_text` identifies upstream issue URLs embedded in bot-copied release-note/changelog sections. Such links count as presented upstream context but do **not** establish a downstream issue, failure, or material explanation of the selected PR. No independent issue sample is created from them. `compatibility_score` records the badge/link's presence, not an independently verified score value.
- `copied_upstream_release_text`: `true` only when the PR body presents upstream release notes/changelog or clearly imported text. `downstream_statement_present`: `true` only for a human statement about this repository's own experience/decision; `downstream_statement_kind` separates a substantive review comment from a bot command. These flags are independent. Copied upstream text is never coded as downstream friction or remediation.

## Review, concern, and work

- `human_interaction_present`, `human_review_present`, `visible_human_interaction_count`: count visible public human comments/review submissions without treating count as effort. Exclude known bot/automated accounts and their boilerplate. When identity is ambiguous, mark `unclear` in notes and avoid positive human coding.
- `approval`, `changes_requested`, `bot_command_usage`, `maintainer_decision`: direct public signals only.
- `concerns`: a list drawn from `compatibility`, `test_failure`, `runtime_failure`, `breaking_change`, `version_constraint`, `transitive_dependency`, `security`, `performance`, `deprecation`, `deployment_build`, `uncertainty`, `irrelevant_no_substantive_concern`, `other`. A version bump alone does not imply a concern; empty list is allowed.
- `additional_work`: checked categories `dependency_file_only`, `lockfile_change_observed`, `lockfile_regeneration`, `test_modification`, `production_code_modification`, `configuration_modification`, `version_pin_change`, `additional_dependency_update`, `rebase_recreation`, `workaround`, `follow_up_issue_pr`. A changed lockfile is directly observable; the command or process used to regenerate it is not, so `lockfile_regeneration` may remain `null`. Comments/commits must support actions not visible in the diff.

## Outcome and time

`outcome`: `merged`, `closed_without_merge`, or `open_at_cutoff`; record reason only if explicit (`ignored_postponed`, `superseded`, `replacement_pr`, `unresolved`, or stated text). `pr_resolution_duration_hours` is the elapsed UTC time from creation to merge or closure, when timestamps exist. It is **not engineering time** or time saved. Completion signals may include visible passed CI/tests, reviewer approval, completed code changes, compatibility evidence, merge itself, no explicit evidence, or another documented signal. Do not infer that a merge proves test success.

`uncertainty`: distinguish explicit uncertainty, missing evidence discussed, unresolved concern, and no visible uncertainty. An empty discussion is not proof that the team had no uncertainty privately.

## Observation versus interpretation

Each record contains `observations` with concise, source-linked descriptions of what the PR shows, and `analyst_interpretations` that make any inferred workflow role explicit. No inferred motivation, frustration, time savings, business impact, portfolio prioritization, or user preference may be coded as an observation. Linked issues are inspected only if explicitly linked by a selected PR and material to its outcome or concern; they remain support for the PR, never additional sample units.
