"""Print the Phase 0 candidate ranking and its sourced human assessments."""

from __future__ import annotations

from pulse.analysis.scorecard import Candidate, Dimension, DimensionAssessment, Scorecard


def assessments(
    source: str,
    scores: tuple[int, int, int, int, int, int, int, int],
    reasons: tuple[str, str, str, str, str, str, str, str],
    source_overrides: dict[Dimension, str] | None = None,
) -> dict[Dimension, DimensionAssessment]:
    overrides = source_overrides or {}
    return {
        dimension: DimensionAssessment(
            score=score,
            justification=reason,
            sources=(overrides.get(dimension, source),),
        )
        for dimension, score, reason in zip(Dimension, scores, reasons, strict=True)
    }


CANDIDATES = [
    Candidate(
        project="NumPy",
        package="numpy",
        version="2.0.0",
        assessments=assessments(
            "https://github.com/numpy/numpy/issues/26191",
            (5, 5, 5, 5, 5, 5, 5, 4),
            (
                "The compatibility tracker names many dependent packages.",
                "The release introduced an explicit C ABI break.",
                "Release and migration notes enumerate breaking changes.",
                "The tracker and downstream CI expose transition activity.",
                "The upstream and sampled downstream work is public on GitHub.",
                "The tracker links downstream compatibility and migration work.",
                "Linked issues and pull requests provide dated evidence.",
                "The tracker preserves a useful but non-random transition record.",
            ),
            {
                Dimension.OBSERVABLE_ADOPTION: (
                    "https://github.com/apache/arrow/issues/42190"
                ),
                Dimension.MIGRATION_EVIDENCE: (
                    "https://github.com/pandas-dev/pandas/issues/59052"
                ),
            },
        ),
        rationale="Strongest single-case evidence, aided by an unusually rich upstream tracker.",
    ),
    Candidate(
        project="Pydantic",
        package="pydantic",
        version="2.0",
        assessments=assessments(
            "https://docs.pydantic.dev/latest/migration/",
            (5, 5, 5, 4, 4, 4, 5, 4),
            (
                "The migration guide addresses a broad Python user base.",
                "Version 2 changes validation APIs and model behavior.",
                "The maintained migration guide gives concrete API mappings.",
                "FastAPI and Prefect expose adoption work, but no census exists.",
                "Important downstream projects are public, with uneven coverage.",
                "The guide and downstream fixes expose concrete migration work.",
                "FastAPI and Prefect preserve dated issues and pull requests.",
                "The transition is recent enough for records but lacks a central tracker.",
            ),
            {
                Dimension.OBSERVABLE_ADOPTION: (
                    "https://github.com/fastapi/fastapi/discussions/9942"
                ),
                Dimension.GITHUB_VISIBILITY: (
                    "https://github.com/PrefectHQ/prefect/issues/10145"
                ),
                Dimension.MIGRATION_EVIDENCE: (
                    "https://github.com/PrefectHQ/prefect/issues/10145"
                ),
                Dimension.ISSUE_PR_AVAILABILITY: (
                    "https://github.com/fastapi/fastapi/pull/9816"
                ),
            },
        ),
        rationale=(
            "A pure-Python API migration with direct downstream evidence and no ABI dependency."
        ),
    ),
    Candidate(
        project="SQLAlchemy",
        package="SQLAlchemy",
        version="2.0.0",
        assessments=assessments(
            "https://docs.sqlalchemy.org/en/20/changelog/migration_20.html",
            (5, 5, 5, 3, 5, 4, 4, 3),
            (
                "The migration guide targets a widely used database toolkit ecosystem.",
                "Version 2 removes or changes long-standing execution APIs.",
                "The upstream migration guide documents staged compatibility work.",
                "Adoption must be inferred from selected downstream repositories.",
                "Upstream and major downstream projects keep public GitHub histories.",
                "Pandas and Flask-SQLAlchemy expose concrete compatibility changes.",
                "Useful issues and pull requests exist but require repository searches.",
                "The staged 1.4 path disperses evidence across a longer interval.",
            ),
            {
                Dimension.OBSERVABLE_ADOPTION: (
                    "https://github.com/pandas-dev/pandas/issues/51015"
                ),
                Dimension.GITHUB_VISIBILITY: (
                    "https://github.com/pandas-dev/pandas/pull/48576"
                ),
                Dimension.MIGRATION_EVIDENCE: (
                    "https://github.com/pallets-eco/flask-sqlalchemy/pull/1215"
                ),
                Dimension.ISSUE_PR_AVAILABILITY: (
                    "https://github.com/pandas-dev/pandas/issues/51015"
                ),
            },
        ),
        rationale=(
            "A strong tracker-free test case with evidence dispersed across downstream projects."
        ),
    ),
    Candidate(
        project="Django",
        package="Django",
        version="4.0",
        assessments=assessments(
            "https://docs.djangoproject.com/en/4.0/releases/4.0/",
            (5, 4, 5, 3, 4, 3, 4, 3),
            (
                "Django has a broad extension and application ecosystem.",
                "The release removes deprecated APIs but follows a documented cadence.",
                "Official release notes enumerate removals and compatibility changes.",
                "No centralized downstream adoption record is identified.",
                "Many projects are public while deployed applications are often private.",
                "Release notes identify migration needs without downstream prevalence.",
                "Public extensions expose issues, with substantial discovery effort.",
                "Older evidence remains available but was not validated in Phase 0B.",
            ),
        ),
        rationale="Plausible mature-ecosystem case retained as an unvalidated candidate.",
    ),
    Candidate(
        project="Flask",
        package="Flask",
        version="3.0.0",
        assessments=assessments(
            "https://flask.palletsprojects.com/en/stable/changes/#version-3-0-0",
            (4, 3, 4, 3, 4, 3, 3, 3),
            (
                "Flask has a substantial extension ecosystem.",
                "The release removes deprecated code with a narrower surface than peers.",
                "Official change notes identify removals and dependency changes.",
                "No centralized downstream adoption record is identified.",
                "Many extensions are public but application adoption is often private.",
                "Documented removals imply migration without measured prevalence.",
                "Extension evidence is available but requires repository searches.",
                "The case is recent and was not reconstructed in Phase 0B.",
            ),
        ),
        rationale="Useful contrast candidate, but not selected for the cross-case validation.",
    ),
]


def main() -> None:
    scorecard = Scorecard()
    for candidate, score in scorecard.rank(CANDIDATES):
        print(f"{candidate.project} {candidate.version}: {score:.1f}")
        for dimension in Dimension:
            assessment = candidate.assessments[dimension]
            print(f"  {dimension.value}: {assessment.score}/5 - {assessment.justification}")
            for source in assessment.sources:
                print(f"    source: {source}")
        print(f"  rationale: {candidate.rationale}")


if __name__ == "__main__":
    main()
