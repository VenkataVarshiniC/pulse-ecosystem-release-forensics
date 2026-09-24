"""Configurable prioritization score; never an automatic case-selection oracle."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Dimension(StrEnum):
    ECOSYSTEM_SIZE = "ecosystem_size"
    RELEASE_SIGNIFICANCE = "release_significance"
    RELEASE_NOTE_QUALITY = "release_note_quality"
    OBSERVABLE_ADOPTION = "observable_adoption"
    GITHUB_VISIBILITY = "github_visibility"
    MIGRATION_EVIDENCE = "migration_evidence"
    ISSUE_PR_AVAILABILITY = "issue_pr_availability"
    HISTORICAL_DEPTH = "historical_depth"


class ScorecardWeights(BaseModel):
    model_config = ConfigDict(frozen=True)

    values: dict[Dimension, float]

    @model_validator(mode="after")
    def weights_sum_to_one(self) -> ScorecardWeights:
        if set(self.values) != set(Dimension):
            raise ValueError("weights must cover every scorecard dimension")
        if abs(sum(self.values.values()) - 1.0) > 1e-9:
            raise ValueError("weights must sum to 1.0")
        if any(weight < 0 for weight in self.values.values()):
            raise ValueError("weights cannot be negative")
        return self

    @classmethod
    def default(cls) -> ScorecardWeights:
        return cls(
            values={
                Dimension.ECOSYSTEM_SIZE: 0.15,
                Dimension.RELEASE_SIGNIFICANCE: 0.15,
                Dimension.RELEASE_NOTE_QUALITY: 0.10,
                Dimension.OBSERVABLE_ADOPTION: 0.15,
                Dimension.GITHUB_VISIBILITY: 0.10,
                Dimension.MIGRATION_EVIDENCE: 0.15,
                Dimension.ISSUE_PR_AVAILABILITY: 0.10,
                Dimension.HISTORICAL_DEPTH: 0.10,
            }
        )


class Candidate(BaseModel):
    model_config = ConfigDict(frozen=True)

    project: str
    package: str
    version: str
    scores: dict[Dimension, int]
    rationale: str

    @model_validator(mode="after")
    def validate_scores(self) -> Candidate:
        if set(self.scores) != set(Dimension):
            raise ValueError("candidate scores must cover every dimension")
        if any(score < 0 or score > 5 for score in self.scores.values()):
            raise ValueError("scores must be between 0 and 5")
        return self


class Scorecard(BaseModel):
    model_config = ConfigDict(frozen=True)

    weights: ScorecardWeights = Field(default_factory=ScorecardWeights.default)

    def score(self, candidate: Candidate) -> float:
        return sum(
            candidate.scores[dimension] * weight
            for dimension, weight in self.weights.values.items()
        )

    def rank(self, candidates: list[Candidate]) -> list[tuple[Candidate, float]]:
        return sorted(
            ((candidate, self.score(candidate)) for candidate in candidates),
            key=lambda item: (-item[1], item[0].project.casefold()),
        )
