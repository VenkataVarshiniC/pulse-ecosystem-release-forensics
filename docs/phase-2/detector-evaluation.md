# Milestone 4 — Detector quality evaluation

**Result: PARTIAL.** The two frozen cases were collected with PULSE's authenticated collectors and all emitted candidates were independently reviewed, but only one case emitted candidates. Two rule firings came from one bot PR, and neither met its declared lifecycle evidence definition. The observed **reviewed-candidate precision is 0/2**, a narrow result about these emitted candidates, not a general estimate of detector quality.

The [preregistered protocol](detector-evaluation-protocol.md) was committed and pushed at `da343d5` before collection or detection. The unchanged first-pass candidate set was written with SHA-256 manifests and committed at `4752833` before review. The frozen cases are [pytest 8.0.0](../../cases/pytest-8.0.0.yaml) (2 repositories) and [urllib3 2.0.0](../../cases/urllib3-2.0.0.yaml) (6 repositories). The [cohort-selection record](cohort-selection.md) used current dependency declarations and does not establish dependency use in either historical release window. All eight repositories stayed in the evaluation denominator.

## Collector runs and coverage

Primary input was PULSE's own collector output with `capture_method=collector`, stored in new external roots `C:\Users\venka\pulse-phase2-m4-pytest-live` and `C:\Users\venka\pulse-phase2-m4-urllib3-live`. Their run IDs and task outcomes are preserved in the machine-readable [metrics](evaluation-data/metrics.json) and external immutable journals. No connector-assisted snapshots or manually chosen issue/PR URLs were used as primary input. Historical reconstruction ran separately, also with collector provenance, in `C:\Users\venka\pulse-phase2-m4-pytest-history-live` and `C:\Users\venka\pulse-phase2-m4-urllib3-history-live`; the selected refs were discovered automatically.

| Case | Planned | Operational status | Succeeded | Optional current-file 404 | Required failure | Partial / rate-limited / unauthorized / failed | Pages requested / completed | HTTP requests / retries |
| --- | ---: | --- | ---: | ---: | ---: | --- | ---: | ---: |
| pytest | 15 | complete | 14 | 1 | 0 | 0 / 0 / 0 / 0 | 14 / 13 | 14 / 0 |
| urllib3 | 39 | complete | 34 | 5 | 0 | 0 / 0 / 0 / 0 | 50 / 45 | 50 / 0 |

Operational completion means required tasks succeeded and optional current-file 404s were recorded. It does not guarantee historical manifest completeness or detector recall. The current planner collects upstream releases but no downstream release tasks, so the `text.support_release` rule had no downstream release input here. Text rules also require an exact target-version string, which can suppress potentially relevant but version-implicit records; suppressed records were not independently labeled in this milestone.

## Historical dependency context

PULSE queried both configured manifest paths for each member before candidate interpretation. `historically_supported` means a parsed target-package declaration existed in at least one exact-ref file state inside the window. It does **not** mean the target *version* was selected or installed. `historically_unknown` retains missing anchors, no in-window path history, or invalid file states. No repository qualified for the stronger `historically_not_established` status. Full path statuses, SHAs, observations, and transitions are in [metrics.json](evaluation-data/metrics.json); no repository was removed because its history was incomplete.

| Case / repository | Context | Path-level evidence and uncertainty |
| --- | --- | --- |
| pytest / `bsc-wdc/qdislib` | historically_unknown | `pyproject.toml` missing before anchor; after state parsed without a target declaration. `requirements.txt` had insufficient in-window history. |
| pytest / `planetlabs/cosmolog` | historically_supported | `pyproject.toml` paired; `pytest>=3.0.2` appears at both refs, unchanged. `requirements.txt` history insufficient. This permissive declaration does not establish pytest 8 installation. |
| urllib3 / `atenreiro/opensquat` | historically_unknown | `pyproject.toml` history insufficient; `requirements.txt` missing before anchor and its parsed after state lacks the target. |
| urllib3 / `jamesturk/scrapelib` | historically_unknown | `pyproject.toml` missing before anchor and its after file could not be parsed; `requirements.txt` history insufficient. |
| urllib3 / `wimglenn/advent-of-code-data` | historically_supported | `pyproject.toml` missing before anchor, but its parsed after state directly declares `urllib3`; `requirements.txt` history insufficient. This does not establish use of urllib3 2.0.0. |
| urllib3 / `Aiven-Open/pghoard` | historically_unknown | Neither configured manifest path had sufficient in-window history. |
| urllib3 / `facundoolano/feedi` | historically_unknown | Both paths missed a before anchor; the `pyproject.toml` after state lacked the target and the `requirements.txt` after state was invalid. |
| urllib3 / `enzet/map-machine` | historically_unknown | Neither configured manifest path had sufficient in-window history. |

The existing Milestone 2 method compares the nearest path-changing commits around release, not every later change. It does not reconcile cross-file migrations. These contextual statuses were **not** used as automatic acceptance or rejection rules: a direct target-version failure could qualify even with unknown manifest history.

## First-pass candidates and analyst review

The unchanged rules emitted [zero pytest candidates](evaluation-data/baseline-pytest-8.0.0.jsonl) and [two urllib3 candidates](evaluation-data/baseline-urllib3-2.0.0.jsonl). Both are separate rule firings on the same collector-captured [scrapelib PR #226](https://github.com/jamesturk/scrapelib/pull/226). The full captured PR body and metadata were inspected, rather than relying on the title or candidate excerpt. It is a Dependabot proposal to widen urllib3's version range, was closed without merging, and includes copied upstream release notes. No supplemental external search was used for the review. The [structured decisions](evaluation-data/review-decisions.json) and [review ledger](evaluation-data/review-ledger.jsonl) label these as **analyst review of PULSE-emitted candidates**, distinct from detector output.

| Candidate / rule | Claimed stage | Analyst outcome | Reason |
| --- | --- | --- | --- |
| `bb4048c374b6b5c34d799903` / `text.version_specific_remediation` | remediation | rejected | `bot_or_dependency_update_noise`: an unmerged bot range proposal and copied upstream notes do not establish an implemented response to downstream friction. |
| `e3aebd0869d43caa3aee8e22` / `text.version_specific_friction` | migration friction | rejected | `generic_dependency_mention`: the PR supplies no concrete scrapelib failure, incompatible environment, or migration task. Error/fix words occur in upstream release notes. |

There were no accepted or unresolved candidates. The false-positive mechanism is version/term matching inside a bot-generated dependency update containing copied upstream changelog text. It produced two rule-level false positives but came from **one distinct artifact**. That falls below the preregistered threshold for a general rule change. No detector rule was changed; there is no revised candidate set or before/after tuning comparison.

## Emitted-candidate metrics and review burden

Precision below is **accepted / (accepted + rejected)**. `needs_review` is excluded from its denominator. A zero denominator is reported as unavailable. The complete machine-readable counts are in [metrics.json](evaluation-data/metrics.json).

| Scope | Emitted | Accepted | Rejected | Needs review | Reviewed-candidate precision |
| --- | ---: | ---: | ---: | ---: | --- |
| Both cases | 2 | 0 | 2 | 0 | **0/2 = 0%** |
| pytest, 2 repositories | 0 | 0 | 0 | 0 | unavailable (0/0) |
| urllib3, 6 repositories | 2 | 0 | 2 | 0 | **0/2 = 0%** |

| Stage | Emitted | Accepted | Rejected | Needs review | Reviewed-candidate precision |
| --- | ---: | ---: | ---: | ---: | --- |
| Adoption readiness | 0 | 0 | 0 | 0 | unavailable |
| Observed adoption | 0 | 0 | 0 | 0 | unavailable |
| Migration friction | 1 | 0 | 1 | 0 | 0/1 = 0% |
| Remediation | 1 | 0 | 1 | 0 | 0/1 = 0% |
| Recovery signal | 0 | 0 | 0 | 0 | unavailable |

| Rule | Emitted | Accepted | Rejected | Needs review | Reviewed-candidate precision | Common rejection reason |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| `text.version_specific_friction` | 1 | 0 | 1 | 0 | 0/1 = 0% | Generic dependency mention in copied release notes |
| `text.version_specific_remediation` | 1 | 0 | 1 | 0 | 0/1 = 0% | Bot dependency-update noise |
| `text.support_release` | 0 | 0 | 0 | 0 | unavailable | No emitted candidate |
| `dependency.target_excluded` | 0 | 0 | 0 | 0 | unavailable | No emitted candidate |
| `dependency.target_accepted` | 0 | 0 | 0 | 0 | unavailable | No emitted candidate |

Review burden was **2 emitted and 2 reviewed across 8 frozen repositories** (0.25 each per repository on average). `jamesturk/scrapelib` had 2 emitted and 2 reviewed; the other seven each had 0 emitted and 0 reviewed. The zero-candidate repositories are `bsc-wdc/qdislib`, `planetlabs/cosmolog`, `atenreiro/opensquat`, `wimglenn/advent-of-code-data`, `Aiven-Open/pghoard`, `facundoolano/feedi`, and `enzet/map-machine`. Zero emitted means only that these rules found no candidate in the collected evidence, **not** that the repository had no adoption, friction, remediation, or release impact.

This evaluation cannot measure recall: there is no independently labeled universe of all true events. Reviewed-candidate precision only describes emitted candidates. The pytest cohort's two-member size, one case with no candidates, one distinct candidate-bearing artifact, widespread unknown historical dependency context, and missing downstream-release collection materially limit rule assessment. These convenience cohorts are not representative of Python projects or the broader ecosystem; no ecosystem incidence or adoption estimate follows.
