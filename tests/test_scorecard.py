from __future__ import annotations

import pytest
from pydantic import ValidationError

from pulse.analysis.scorecard import Candidate, Dimension, Scorecard, ScorecardWeights


def complete_scores(value: int) -> dict[Dimension, int]:
    return dict.fromkeys(Dimension, value)


def test_scorecard_applies_configurable_weights_and_ranks_deterministically() -> None:
    weights = ScorecardWeights(values=dict.fromkeys(Dimension, 1 / len(Dimension)))
    stronger = Candidate(
        project="Stronger",
        package="stronger",
        version="2.0",
        scores=complete_scores(5),
        rationale="Direct evidence exists across every dimension.",
    )
    weaker = Candidate(
        project="Weaker",
        package="weaker",
        version="2.0",
        scores=complete_scores(2),
        rationale="Only partial evidence exists across the dimensions.",
    )

    ranking = Scorecard(weights=weights).rank([weaker, stronger])

    assert ranking[0] == (stronger, 5.0)
    assert ranking[1] == (weaker, 2.0)


def test_scorecard_rejects_incomplete_weights() -> None:
    with pytest.raises(ValidationError, match="every scorecard dimension"):
        ScorecardWeights(values={Dimension.ECOSYSTEM_SIZE: 1.0})
