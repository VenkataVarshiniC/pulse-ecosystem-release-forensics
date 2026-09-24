from __future__ import annotations

import pytest
from pydantic import ValidationError

from pulse.analysis.scorecard import (
    Candidate,
    Dimension,
    DimensionAssessment,
    Scorecard,
    ScorecardWeights,
)


def complete_assessments(value: int) -> dict[Dimension, DimensionAssessment]:
    return {
        dimension: DimensionAssessment(
            score=value,
            justification=f"Documented evidence supports the {dimension.value} assessment.",
            sources=("https://example.com/evidence",),
        )
        for dimension in Dimension
    }


def test_scorecard_applies_configurable_weights_and_ranks_deterministically() -> None:
    weights = ScorecardWeights(values=dict.fromkeys(Dimension, 1 / len(Dimension)))
    stronger = Candidate(
        project="Stronger",
        package="stronger",
        version="2.0",
        assessments=complete_assessments(5),
        rationale="Direct evidence exists across every dimension.",
    )
    weaker = Candidate(
        project="Weaker",
        package="weaker",
        version="2.0",
        assessments=complete_assessments(2),
        rationale="Only partial evidence exists across the dimensions.",
    )

    ranking = Scorecard(weights=weights).rank([weaker, stronger])

    assert ranking[0] == (stronger, 5.0)
    assert ranking[1] == (weaker, 2.0)


def test_scorecard_rejects_incomplete_weights() -> None:
    with pytest.raises(ValidationError, match="every scorecard dimension"):
        ScorecardWeights(values={Dimension.ECOSYSTEM_SIZE: 1.0})


def test_candidate_rejects_an_unauditable_dimension() -> None:
    assessments = complete_assessments(3)
    assessments.pop(Dimension.HISTORICAL_DEPTH)

    with pytest.raises(ValidationError, match="every dimension"):
        Candidate(
            project="Example",
            package="example",
            version="2.0",
            assessments=assessments,
            rationale="A candidate with one missing dimension.",
        )
