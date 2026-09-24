# Forensic timelines

Generated from `data/processed/evidence-ledger.jsonl`. Every entry links back to its source.

## numpy 2.0.0

- **2024-04-10 - adoption_readiness:** pandas 2.2.2 declared NumPy 2.0 compatibility (high; [source 1](https://pandas.pydata.org/docs/whatsnew/v2.2.2.html#pandas-2-2-2-is-now-compatible-with-numpy-2-0))
- **2024-06-16 - release:** NumPy 2.0.0 released (high; [source 1](https://numpy.org/news/), [source 2](https://numpy.org/doc/2.0/release/2.0.0-notes.html))
- **2024-06-17 - observed_adoption:** Arrow CI began resolving NumPy 2.0 as latest (high; [source 1](https://github.com/apache/arrow/issues/42190))
- **2024-06-19 - migration_friction:** pandas 2.0.3 failed to import with NumPy 2.0 (high; [source 1](https://github.com/pandas-dev/pandas/issues/59052))
- **2024-06-19 - remediation:** Maintainer recommended pandas 2.2.2 or NumPy below 2 (high; [source 1](https://github.com/pandas-dev/pandas/issues/59052))

## pydantic 2.0

- **2023-06-30 - release:** Pydantic 2.0 released (high; [source 1](https://pydantic.dev/articles/pydantic-v2-final), [source 2](https://pypi.org/project/pydantic/2.0/))
- **2023-07-03 - remediation:** Prefect constrained Pydantic below 2 (high; [source 1](https://github.com/PrefectHQ/prefect/pull/10144))
- **2023-07-03 - migration_friction:** Prefect tracked a complex Pydantic 2 migration (high; [source 1](https://github.com/PrefectHQ/prefect/issues/10145))
- **2023-07-07 - adoption_readiness:** FastAPI 0.100.0 added Pydantic 2 support (high; [source 1](https://fastapi.tiangolo.com/release-notes/#01000))
- **2023-07-25 - migration_friction:** FastAPI user hit a Pydantic 2.1.0 compatibility failure (medium; [source 1](https://github.com/fastapi/fastapi/discussions/9942))
- **2023-08-04 - remediation:** FastAPI 0.101.0 excluded broken Pydantic 2.1.0 (high; [source 1](https://fastapi.tiangolo.com/release-notes/#01010))

## SQLAlchemy 2.0.0

- **2023-01-26 - release:** SQLAlchemy 2.0.0 released (high; [source 1](https://docs.sqlalchemy.org/en/20/changelog/changelog_20.html#change-2.0.0))
- **2023-01-27 - migration_friction:** pandas 1.5.3 failed with SQLAlchemy 2.0 (high; [source 1](https://github.com/pandas-dev/pandas/issues/51015))
- **2023-02-09 - remediation:** pandas merged SQLAlchemy 2.0 compatibility work (high; [source 1](https://github.com/pandas-dev/pandas/pull/48576))
- **2023-04-03 - recovery_signal:** pandas 2.0.0 shipped SQLAlchemy 2.0 support (high; [source 1](https://pandas.pydata.org/pandas-docs/version/2.0/whatsnew/v2.0.0.html))
- **2023-08-31 - remediation:** Flask-SQLAlchemy merged 2.0 DeclarativeBase support (high; [source 1](https://github.com/pallets-eco/flask-sqlalchemy/pull/1215))
- **2023-09-11 - recovery_signal:** Flask-SQLAlchemy 3.1.0 shipped SQLAlchemy 2.x support (medium; [source 1](https://github.com/pallets-eco/flask-sqlalchemy/blob/main/CHANGES.rst))
