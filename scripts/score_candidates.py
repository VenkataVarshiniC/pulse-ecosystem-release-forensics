"""Print the Phase 0 candidate ranking and its human-entered inputs."""

from __future__ import annotations

from pulse.analysis.scorecard import Candidate, Dimension, Scorecard


def scores(*values: int) -> dict[Dimension, int]:
    return dict(zip(Dimension, values, strict=True))


CANDIDATES = [
    Candidate(
        project="NumPy",
        package="numpy",
        version="2.0.0",
        scores=scores(5, 5, 5, 5, 5, 5, 5, 4),
        rationale="ABI break, migration guide, compatibility tracker, and downstream fixes.",
    ),
    Candidate(
        project="Pydantic",
        package="pydantic",
        version="2.0",
        scores=scores(5, 5, 5, 4, 4, 4, 5, 4),
        rationale="Large API migration with a detailed guide and visible downstream work.",
    ),
    Candidate(
        project="SQLAlchemy",
        package="SQLAlchemy",
        version="2.0.0",
        scores=scores(5, 5, 5, 3, 5, 4, 4, 3),
        rationale="Major API transition with a staged 1.4 migration path.",
    ),
    Candidate(
        project="Django",
        package="Django",
        version="4.0",
        scores=scores(5, 4, 5, 3, 4, 3, 4, 3),
        rationale="Clear release boundary and compatibility notes across a mature ecosystem.",
    ),
    Candidate(
        project="Flask",
        package="Flask",
        version="3.0.0",
        scores=scores(4, 3, 4, 3, 4, 3, 3, 3),
        rationale="Deprecated API removals are visible, but the migration surface is smaller.",
    ),
]


def main() -> None:
    scorecard = Scorecard()
    for candidate, score in scorecard.rank(CANDIDATES):
        print(f"{candidate.project} {candidate.version}: {score:.2f}")
        for dimension in Dimension:
            print(f"  {dimension.value}: {candidate.scores[dimension]}/5")
        print(f"  rationale: {candidate.rationale}")


if __name__ == "__main__":
    main()
