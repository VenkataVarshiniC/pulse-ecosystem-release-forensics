# Public GitHub PR sampling protocol — frozen before outcome review

Protocol version: `p3-m1a-v1`. Fixed observation window: PRs **created 2025-01-01 through 2026-06-30 UTC**, inclusive. Observation/coding cutoff: **2026-09-27 UTC**. This protocol is committed before detailed PR outcomes or discussions are reviewed. Any deviation must be logged, not silently optimized for interesting cases.

## Question and source

What observable steps, evidence sources, decisions, exceptions, and remediation actions occur in public Python dependency-upgrade PRs? Source: public GitHub PR metadata, changed-file record, body, reviews/comments, and materially linked issues. PRs are the observation unit; issues are supporting evidence only. Public GitHub activity is secondary observational research, not stakeholder validation.

## Candidate searches and frame construction

Use GitHub PR search, ordered by `created` ascending, with these exact query templates for each of three non-overlapping created-date slices: `2025-01-01..2025-06-30`, `2025-07-01..2025-12-31`, and `2026-01-01..2026-06-30`.

- Base frame: `is:pr language:Python in:title bump created:<slice>`; request the first **30** results per slice.
- Discussion frame: `is:pr language:Python in:title bump comments:>=2 created:<slice>`; request the first **15** results per slice.

Search query, sorting, retrieval date, returned count, total count if exposed, and any search truncation/error will be recorded. These are bounded search-result frames, **not** a probability sample of all Python upgrades. The `bump` title term favors conventional automated PRs and may miss human-authored “update” PRs; the discussion query deliberately favors visible activity. Search results can change as GitHub indexing changes. Freeze the returned canonical `owner/repo#number` IDs in `github-pr-candidate-frame.json` before coding. The maximum raw frame is 135 entries before overlap; the **actual candidate-frame size** is recorded in the frozen frame and its summary after retrieval, rather than guessed here.

## Eligibility and exclusions

Include a publicly accessible GitHub PR that proposes a Python package dependency version or constraint change in a Python project (for example `pyproject.toml`, `requirements*.txt`, `poetry.lock`, `uv.lock`, `Pipfile*`, `setup.py`, or `setup.cfg`). The PR need not merge, discuss a problem, or exhibit friction. Exclude with an explicit reason if it changes only GitHub Actions or non-Python dependencies, is not a dependency upgrade, is inaccessible/unavailable, duplicates an exact change under this protocol, or lacks a reviewable public record sufficient to identify the dependency change. Do **not** exclude for quick merge, passed CI, absent discussion, or contradiction of PULSE's hypotheses.

Screen the search-result title and metadata first; inspect changed-file paths and dependency diff as needed to confirm eligibility. Record every candidate, including exclusions and unknown metadata, in the frame. Record dependency, previous/proposed version, initiator and mechanism only when identifiable; null means not established. Search metadata may reveal state/timestamps, but neither selection nor eligibility uses merge/close outcome, concern type, or qualitative interest. When a selected title is not actually eligible after artifact inspection, log the reason and take the next ranked eligible candidate in that slice. Do not silently replace an inconvenient eligible case.

## Deterministic selection and freeze

Canonical key is lowercase `owner/repo#number`. Rank eligible base-frame IDs within each slice by lowercase hexadecimal SHA-256 of UTF-8 text `p3-m1a-v1:base:<canonical-key>`, ascending; select **7, 7, and 6** across the three slices. Rank eligible discussion-frame IDs analogously using `p3-m1a-v1:discussion:<canonical-key>`; select **4, 3, and 3**. The discussion set excludes base-selected IDs, and takes the next ranked candidate on overlap. Require visible public human comment/review interaction for Sample B; if metadata comment count is only bot activity, document the replacement. Sample B is purposive and **never pooled with Sample A for prevalence**. Freeze selected IDs and any replacements before qualitative coding; save the ranking, decision, and reason in the candidate frame.

The target is 20 base and 10 discussion PRs, approximately 30 total. If a slice lacks enough eligible public PRs, record the shortfall and do not improvise a new search without a protocol amendment committed before inspecting outcomes. No statistical representativeness is claimed. Within the bounded base frame, only descriptive counts such as “x of 20 sampled base PRs” are permissible; they do not estimate Python ecosystem rates.

## Candidate record and coding boundary

For **every returned candidate**, store repository, PR number, canonical URL, author type, created/closed/merged date, title, dependency and versions if identifiable, mechanism if observable, current state, search-frame membership, eligibility decision and exclusion reason, rank, and selection status. Dates and state may be null/unknown if unavailable. The human-readable frame summary reports raw counts, deduplication, exclusions, and final sample counts.

Detailed body, diff, comments, reviews, and linked-issue interpretation begins only after IDs are frozen. The [codebook](github-pr-codebook.md) will distinguish copied upstream release notes from downstream statements, direct observations from analyst interpretation, and PR resolution duration from engineering effort. The study cannot reveal private work or users' motivations, preferences, time savings, or business impact unless explicitly stated in the public record.

## Execution accounting (added after the protocol and sample were frozen)

The six searches returned 135 entries and 110 unique PR IDs. File-path/metadata screening marked 55 eligible and 55 excluded. SHA-256 selection froze 20 base IDs and 7 discussion IDs in commit `a8d4007` before qualitative coding. Discussion slice 1 (2025-07-01..2025-12-31) supplied no eligible candidate with visible human interaction, leaving its three positions unfilled. No query or quota was changed to compensate. See the [frame summary](github-pr-candidate-frame-summary.md) for the full accounting. All 27 selected PRs happened to be created on the first day of their respective half-year slice, a substantial consequence of taking the earliest search page; the resulting workflow evidence is narrow and bot-centered.
