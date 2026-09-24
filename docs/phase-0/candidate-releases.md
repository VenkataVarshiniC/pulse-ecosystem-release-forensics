# Candidate releases

Scores are analyst assessments from 0 (poor) to 5 (excellent), not measured ecosystem facts. Weights live in `src/pulse/analysis/scorecard.py` and can be changed before selection.

| Release | Date | Ecosystem | Significance | Notes | Weighted score |
|---|---:|---:|---:|---:|---:|
| NumPy 2.0.0 | 2024-06-16 | 5 | 5 | 5 | 4.90 |
| Pydantic 2.0 | 2023-06-30 | 5 | 5 | 5 | 4.50 |
| SQLAlchemy 2.0.0 | 2023-01-26 | 5 | 5 | 5 | 4.25 |
| Django 4.0 | 2021-12-07 | 5 | 4 | 5 | 3.85 |
| Flask 3.0.0 | 2023-09-30 | 4 | 3 | 4 | 3.35 |

The displayed score uses all eight dimensions; the compact table exposes only three for readability. Run `uv run python scripts/score_candidates.py` for the full breakdown.

## Selection rationale

NumPy 2.0.0 is strongest because it combines a first-major-release-in-years event, an explicit binary ABI break, a migration guide, an upstream ecosystem compatibility tracker, downstream compatibility releases, reproducible import failures for old binaries, and subsequent patch releases. This supports every lifecycle stage without relying on inferred sentiment.

## Primary candidate sources

- [NumPy 2.0.0 release notes](https://numpy.org/doc/2.0/release/2.0.0-notes.html)
- [NumPy 2.0 migration guide](https://numpy.org/doc/2.0/numpy_2_0_migration_guide.html)
- [NumPy 2.0 announcement and downstream guidance](https://github.com/numpy/numpy/issues/24300)
- [NumPy ecosystem compatibility tracker](https://github.com/numpy/numpy/issues/26191)
- [pandas 2.2.2 compatibility note](https://pandas.pydata.org/docs/whatsnew/v2.2.2.html#pandas-2-2-2-is-now-compatible-with-numpy-2-0)
- [pandas old-binary import failure](https://github.com/pandas-dev/pandas/issues/59052)
- [Apache Arrow Windows failures](https://github.com/apache/arrow/issues/41924)

## Other candidate sources

- [Pydantic V2 release announcement](https://pydantic.dev/articles/pydantic-v2-final)
- [Pydantic V2 migration guide](https://docs.pydantic.dev/latest/migration/)
- [SQLAlchemy 2.0 migration guide](https://docs.sqlalchemy.org/en/20/changelog/migration_20.html)
- [Django 4.0 release announcement](https://www.djangoproject.com/weblog/2021/dec/07/django-40-released/)
- [Django 4.0 release notes](https://docs.djangoproject.com/en/4.0/releases/4.0/)
- [Flask 3.0.0 changelog](https://flask.palletsprojects.com/en/3.0.x/changes/#version-3-0-0)
