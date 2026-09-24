# Data feasibility

## Sources tested

PyPI JSON metadata can establish package identity, release files, upload timestamps, Python constraints, and project links. GitHub provides releases, issues, pull requests, commits, repository files, and timestamps. Upstream documentation supplies the intended change and migration guidance. Downstream changelogs and dependency files provide stronger adoption and compatibility evidence than search-result counts.

## First reconstruction: NumPy 2.0.0

| Lifecycle stage | Observation | Confidence | Evidence |
|---|---|---|---|
| Release | NumPy 2.0.0 files were uploaded on 2024-06-16; release notes describe Python/C API changes and an ABI break. | High | [PyPI](https://pypi.org/project/numpy/2.0.0/), [release notes](https://numpy.org/doc/2.0/release/2.0.0-notes.html) |
| Adoption readiness | pandas 2.2.2, released before NumPy 2.0, states that its wheels work with NumPy 1.x and 2.x. | High | [pandas 2.2.2 notes](https://pandas.pydata.org/docs/whatsnew/v2.2.2.html#pandas-2-2-2-is-now-compatible-with-numpy-2-0) |
| Breakage | After 2.0.0, a pandas report reproduced `numpy.dtype size changed` when an old pandas binary resolved with NumPy 2.0. | High | [pandas #59052](https://github.com/pandas-dev/pandas/issues/59052) |
| Workaround | Maintainer guidance on that report was to install pandas 2.2.2 or pin NumPy below 2. | High | [pandas #59052](https://github.com/pandas-dev/pandas/issues/59052) |
| Remediation | Apache Arrow tracked NumPy 2.0 compatibility work before release and fixed release-associated Windows test failures afterward. | Medium | [Arrow #39532](https://github.com/apache/arrow/issues/39532), [Arrow #41924](https://github.com/apache/arrow/issues/41924) |
| Ecosystem response | NumPy maintained an explicit downstream compatibility tracker, while its migration guide documented ABI and API changes and an automated Ruff rule. | High | [NumPy #26191](https://github.com/numpy/numpy/issues/26191), [migration guide](https://numpy.org/doc/2.0/numpy_2_0_migration_guide.html) |
| Recovery signal | NumPy published 2.0.1 on 2024-07-21 and 2.0.2 on 2024-08-26; compatible downstream releases and trackers show remediation progressing. | Medium | [NumPy news](https://numpy.org/news/) |

This is an ecosystem-level recovery signal, not proof that every downstream project recovered. “Recovery” needs an explicit population and time window before it can become a metric.

## Evidence available

- Exact upstream and package timestamps.
- Direct statements of binary incompatibility and migration requirements.
- Repository-local compatibility issues, pull requests, commits, and release notes.
- Explicit dependency pins and recommendations to upgrade or downgrade.
- Patch releases and downstream compatibility releases.

## Evidence missing or incomplete

- GitHub code search cannot enumerate private repositories or all public usage.
- PyPI metadata does not identify which installations or repositories adopted a version.
- Repositories may squash, rewrite, or delete the commit history that carried a dependency transition.
- Issue text can name a release without demonstrating that it caused the observed failure.
- Package download counts do not establish successful adoption and are deliberately excluded.
- “No issue found” is weak evidence because support discussions may occur elsewhere.

## API and rate-limit constraints

The GitHub client records `X-RateLimit-*` headers, follows REST `Link` pagination, retries transient 429/5xx responses, and stops with a structured error rather than silently returning partial data. Authenticated REST quotas still constrain broad discovery. Search has separate limits and incomplete historical indexing. PyPI’s JSON API is simple but supplies package metadata rather than repository-level adoption.

## Detecting transitions and migration activity

An exact manifest or lockfile diff from `<2` to `>=2` is high-confidence adoption evidence. A PR that says “support NumPy 2” but contains no dependency or test change is medium at best. Text posted after release is low confidence until linked to a reproducible environment, code change, or released artifact.

## False-positive risk

Package names can appear in documentation, optional test environments, generated lockfiles, bot updates, and unrelated discussion. Temporal proximity amplifies this risk. Rules therefore require target package, target version, repository, event time, source, confidence, and a written evidence reason.

## Privacy and legal considerations

Phase 0 uses public project artifacts and avoids personal profiling. Raw records should retain source URL and retrieval time, respect platform terms and rate limits, and minimize copied personal data. Deletions or redactions upstream should be handled by a future retention policy before durable collection begins.
