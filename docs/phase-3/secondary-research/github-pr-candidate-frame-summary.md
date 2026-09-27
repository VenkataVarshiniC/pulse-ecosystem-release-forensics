# Candidate-frame and sample accounting

Source: public GitHub PR search and PR/file/comment records retrieved through the GitHub connector on **2026-09-27**. This is connector-assisted secondary research, not a PULSE collector run. Canonical PR URLs and metadata for **every** returned candidate are in [the machine-readable frame](github-pr-candidate-frame.json). [The protocol](github-pr-sampling-protocol.md) was committed as `93a651a` before detailed outcome review; the screened frame and selected IDs were committed as `a8d4007` before qualitative coding. GitHub search did not expose an ecosystem denominator in the connector result, and the bounded first-page frame must not be described as one.

| Frame accounting | Count |
| --- | ---: |
| Raw search entries (90 base-frame, 45 discussion-frame) | 135 |
| Overlapping entries across searches | 25 |
| Unique candidate PRs | 110 |
| Eligible Python package-upgrade PRs | 55 |
| Excluded: no Python package dependency file changed | 54 |
| Excluded: changed-file artifact unavailable for review | 1 |
| Frozen Sample A, base | 20 |
| Frozen Sample B, purposive discussion | 7 |

The 25 overlapping search entries were deduplicated by canonical PR ID. No further candidate pair had the same repository, title, and changed-file set during the metadata duplicate check; no distinct PR was excluded as an exact-change duplicate.

Sample A met its planned slice quotas `7 / 7 / 6`. Sample B yielded `4 / 0 / 3` against `4 / 3 / 3`; the middle slice had no eligible PR with visible human interaction in its predeclared first 15 discussion search hits. It was not backfilled from another slice. SHA-256 ranking and the precise selected IDs are in the candidate frame; [the selection helper](select_pr_sample.py) reproduces the rule. All sampled PRs were opened by Dependabot; this is an observed property of this **title-and-early-page frame**, not evidence that Python upgrades generally use Dependabot.

The connector returned PR bodies and outcome metadata alongside the fields needed for screening. The selection procedure used canonical ID, slice membership, changed-file eligibility, and (for Sample B) visible human-interaction presence; it did not use body themes, merge/close outcome, or compatibility discussion to rank or replace cases. Qualitative coding began after the selected IDs were frozen.

The selected PRs span 15 public repositories: `artichoke/nightly`, `reddit/baseplate.py`, `Kludex/uvicorn`, `anna-money/aio-request`, `Couchers-org/couchers`, `cordada/lib-cl-sii-python`, `superdesk/superdesk-stt`, `CODEX-CELIDA/execution-engine`, `KristopherKubicki/glimpser`, `ktamamu/neko_sg`, `dsp-testing/freqtrade`, `delphix/virtualization-sdk`, `aio-libs/aiohttp-session`, `team-ocean/veros`, and `gugarosa/statys`.

## Limits affecting interpretation

GitHub returned the earliest 30/15 results per half-year slice. All selected PRs were created on **2025-01-01, 2025-07-01, or 2026-01-01**, so the sample does not cover the window evenly. The title term `bump` strongly favors bot-generated PRs, and the `language:Python` filter did not prevent non-Python dependency changes from entering the candidate frame. The file-path exclusions account for those false hits. Several selected PRs come from the same repository and update family, especially the Delphix pytest 9.0.2 group; those are distinct PR artifacts, not independent organizations. The purposive discussion sample contains approvals/commands as well as one substantive compatibility discussion; it should not be portrayed as a sample of failures.

The [27 coded observations](github-pr-observations.jsonl) support a bounded account of visible PR workflow. Sample A counts can be stated as counts **within 20 sampled base PRs**. Sample B is used for qualitative examples, not pooled with A for prevalence. Neither sample estimates ecosystem-wide frequency, invisible engineering work, preferences, or value.
