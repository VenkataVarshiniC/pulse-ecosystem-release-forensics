# Candidate releases

Scores are analyst assessments from 0 (poor) to 5 (excellent), not measured ecosystem facts. Weights live in `src/pulse/analysis/scorecard.py` and can be changed before selection. The executable scorecard requires a justification and at least one source for every dimension; `scripts/score_candidates.py` prints the full audit trail. Weighted totals are prioritization aids and should not be interpreted as measured precision.

| Release | Date | Ecosystem | Significance | Notes | Weighted score |
|---|---:|---:|---:|---:|---:|
| NumPy 2.0.0 | 2024-06-16 | 5 | 5 | 5 | 4.9 |
| Pydantic 2.0 | 2023-06-30 | 5 | 5 | 5 | 4.5 |
| SQLAlchemy 2.0.0 | 2023-01-26 | 5 | 5 | 5 | 4.3 |
| Django 4.0 | 2021-12-07 | 5 | 4 | 5 | 3.9 |
| Flask 3.0.0 | 2023-09-30 | 4 | 3 | 4 | 3.4 |

The displayed score uses all eight dimensions; the compact table exposes only three for readability. Run `uv run python scripts/score_candidates.py` for every score, reason, source, and weight-derived total.

## Selection rationale

NumPy 2.0.0 was selected first because it combines a first-major-release-in-years event, an explicit binary ABI break, a migration guide, an upstream ecosystem compatibility tracker, downstream compatibility releases, and reproducible import failures for old binaries. The NumPy result was a **qualified GO to Phase 0B**, not a general product decision. Its centralized tracker and distinctive binary errors could make it an unusually easy case.

Pydantic 2.0 was selected for Phase 0B as the pure-Python/API migration. Its migration guide and the FastAPI and Prefect records provide concrete API, import, compatibility-release, and pin evidence without an ABI break.

SQLAlchemy 2.0.0 was selected as the strongest tracker-free case. Its staged migration guide is strong, but downstream discovery required separate repository-local searches in pandas and Flask-SQLAlchemy. No centralized compatibility tracker was found during the documented search; this is a search result, not proof that no tracker exists.

## Primary candidate sources

- [NumPy 2.0.0 release notes](https://numpy.org/doc/2.0/release/2.0.0-notes.html)
- [NumPy 2.0 migration guide](https://numpy.org/doc/2.0/numpy_2_0_migration_guide.html)
- [NumPy 2.0 announcement and downstream guidance](https://github.com/numpy/numpy/issues/24300)
- [NumPy ecosystem compatibility tracker](https://github.com/numpy/numpy/issues/26191)
- [pandas 2.2.2 compatibility note](https://pandas.pydata.org/docs/whatsnew/v2.2.2.html#pandas-2-2-2-is-now-compatible-with-numpy-2-0)
- [pandas old-binary import failure](https://github.com/pandas-dev/pandas/issues/59052)
- [Apache Arrow Windows failures](https://github.com/apache/arrow/issues/41924)

## Added-case sources

- [Pydantic V2 release announcement](https://pydantic.dev/articles/pydantic-v2-final)
- [Pydantic V2 migration guide](https://docs.pydantic.dev/latest/migration/)
- [FastAPI Pydantic V2 support](https://github.com/fastapi/fastapi/pull/9816)
- [Prefect Pydantic V1 pin](https://github.com/PrefectHQ/prefect/pull/10144)
- [SQLAlchemy 2.0 migration guide](https://docs.sqlalchemy.org/en/20/changelog/migration_20.html)
- [pandas SQLAlchemy 2.0 failure](https://github.com/pandas-dev/pandas/issues/51015)
- [pandas SQLAlchemy 2.0 compatibility PR](https://github.com/pandas-dev/pandas/pull/48576)
- [Flask-SQLAlchemy 2.0 DeclarativeBase support](https://github.com/pallets-eco/flask-sqlalchemy/pull/1215)

## Other candidate sources

- [Django 4.0 release announcement](https://www.djangoproject.com/weblog/2021/dec/07/django-40-released/)
- [Django 4.0 release notes](https://docs.djangoproject.com/en/4.0/releases/4.0/)
- [Flask 3.0.0 changelog](https://flask.palletsprojects.com/en/3.0.x/changes/#version-3-0-0)
