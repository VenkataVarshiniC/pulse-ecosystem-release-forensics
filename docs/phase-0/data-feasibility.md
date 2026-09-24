# Data feasibility

## Sources and data contract

PyPI JSON metadata establishes package identity, selected-version distribution artifacts, upload timestamps, Python constraints, and project links. GitHub provides releases, issues, pull requests, commits, repository files, and timestamps. Upstream documentation supplies intended changes and migration guidance. Downstream changelogs and dependency files provide stronger compatibility evidence than search-result counts.

Accepted observations live in `data/processed/evidence-ledger.jsonl`. Each line is validated as an `EvidenceEvent` and records the case, target release, repository, lifecycle stage, event type, occurrence time and precision, source URL, observation time, confidence, and evidence reason. Excerpts are short discovery aids; the linked source remains authoritative.

The PyPI adapter models the response’s `urls` collection as distribution artifacts for the selected version. It does not claim that those files are package release history. [ADR 0002](../decisions/0002-model-pypi-artifacts.md) records the corrected semantics.

## NumPy 2.0.0

| Stage | Observation | Confidence | Evidence |
|---|---|---|---|
| Release | Official records place the release on 2024-06-16 and document an ABI break. | High | [News](https://numpy.org/news/), [release notes](https://numpy.org/doc/2.0/release/2.0.0-notes.html) |
| Adoption readiness | pandas 2.2.2 stated that its wheels work with NumPy 1.x and 2.x before the release. | High | [pandas 2.2.2 notes](https://pandas.pydata.org/docs/whatsnew/v2.2.2.html#pandas-2-2-2-is-now-compatible-with-numpy-2-0) |
| Observed adoption | Arrow reported that ordinary CI jobs resolved the newly released NumPy 2.0 as latest. | High | [Arrow #42190](https://github.com/apache/arrow/issues/42190) |
| Friction | pandas 2.0.3 with NumPy 2.0 reproduced a binary dtype-size import error. | High | [pandas #59052](https://github.com/pandas-dev/pandas/issues/59052) |
| Remediation | Maintainer guidance was to use pandas 2.2.2 or temporarily constrain NumPy below 2. | High | [pandas #59052](https://github.com/pandas-dev/pandas/issues/59052) |
| Recovery | Not claimed. Patch releases and tracker updates do not establish recovery for a declared population. | — | [Lifecycle definitions](lifecycle-definitions.md) |

The NumPy case supports a **qualified GO to Phase 0B**. It does not support a general product GO because the central tracker and explicit ABI failure signature may be atypically favorable.

## Pydantic 2.0

| Stage | Observation | Confidence | Evidence |
|---|---|---|---|
| Release | The official final announcement and package page establish the 2023-06-30 boundary. | High | [Announcement](https://pydantic.dev/articles/pydantic-v2-final), [PyPI](https://pypi.org/project/pydantic/2.0/) |
| Adoption readiness | FastAPI 0.100.0 shipped dual Pydantic 1 and 2 support with both test paths. | High | [FastAPI 0.100.0 notes](https://fastapi.tiangolo.com/release-notes/#01000) |
| Friction | Prefect tracked import and migration work; a FastAPI user reported a version-specific Pydantic 2.1.0 failure. | High/Medium | [Prefect #10145](https://github.com/PrefectHQ/prefect/issues/10145), [FastAPI discussion #9942](https://github.com/fastapi/fastapi/discussions/9942) |
| Remediation | Prefect constrained Pydantic below 2; FastAPI later excluded the broken 2.1.0 release. | High | [Prefect #10144](https://github.com/PrefectHQ/prefect/pull/10144), [FastAPI 0.101.0 notes](https://fastapi.tiangolo.com/release-notes/#01010) |
| Recovery | Not claimed. Issue closure and a fix in one selected project do not establish cohort recovery. | — | [Lifecycle definitions](lifecycle-definitions.md) |

This case shows that API migration evidence remains useful without compiled binaries. It also exposes how compatibility releases demonstrate readiness more readily than ordinary adoption.

## SQLAlchemy 2.0.0

No centralized compatibility tracker was found during the documented search. Discovery therefore began with the upstream migration surface and continued with exact version and removed-API searches in plausible downstream repositories. The result is reproducible for the named repositories, but the repository sample is analyst-selected.

| Stage | Observation | Confidence | Evidence |
|---|---|---|---|
| Release | The official changelog places 2.0.0 on 2023-01-26. | High | [Changelog](https://docs.sqlalchemy.org/en/20/changelog/changelog_20.html#change-2.0.0) |
| Friction | pandas 1.5.3 failed against SQLAlchemy 2.0.0 because the old execution path was removed. | High | [pandas #51015](https://github.com/pandas-dev/pandas/issues/51015) |
| Remediation | pandas and Flask-SQLAlchemy merged concrete SQLAlchemy 2.0 compatibility changes. | High | [pandas #48576](https://github.com/pandas-dev/pandas/pull/48576), [Flask-SQLAlchemy #1215](https://github.com/pallets-eco/flask-sqlalchemy/pull/1215) |
| Recovery signal | In the declared two-project cohort, pandas 2.0.0 and Flask-SQLAlchemy 3.1.0 both shipped explicit SQLAlchemy 2.0 support by 2023-09-11. | High/Medium | [pandas 2.0.0 notes](https://pandas.pydata.org/pandas-docs/version/2.0/whatsnew/v2.0.0.html), [Flask-SQLAlchemy changes](https://github.com/pallets-eco/flask-sqlalchemy/blob/main/CHANGES.rst) |

The recovery statement applies only to the purposive cohort `{pandas, Flask-SQLAlchemy}` during 2023-01-26 through 2023-09-11. It is not an estimate of SQLAlchemy ecosystem recovery.

## Collection and analysis behavior

The GitHub issues endpoint includes pull requests. `GitHubClient.issues()` filters every record containing a `pull_request` object, and its regression test prevents analytical issue counts from including pull requests.

The timeline layer groups ledger events by case and target release, sorts them by occurrence time and lifecycle order, and renders source links. It contains no embeddings, AI classification, or inferred events. Analysts still decide which public artifacts satisfy the published lifecycle definitions.

## Constraints and false-positive risk

- Public GitHub search cannot enumerate private repositories or all public usage.
- PyPI metadata does not identify which installations or repositories adopted a version.
- Tracker-free discovery depends on repository selection and recorded search terms.
- Package names appear in documentation, optional tests, bot updates, and generated lockfiles.
- Temporal proximity does not establish causality; reports use “release-associated” unless a source demonstrates the mechanism.
- “No issue found” is weak evidence because support discussions may occur elsewhere.
- Search indexes and mutable issues can change, so exact re-runs may differ even when the method is preserved.

Phase 0 uses public project artifacts, avoids personal profiling, and stores only short excerpts with source and observation timestamps. A durable collection system would still need a retention and upstream-deletion policy.
