"""Release-case and declared-cohort domain models."""

from __future__ import annotations

from datetime import date, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, model_validator

from pulse.models.evidence import Confidence, EvidenceReference


class CohortSelectionMethod(StrEnum):
    EXPLICIT = "explicit"
    RULE_BASED = "rule_based"


class SourceSystem(StrEnum):
    GITHUB = "github"
    PYPI = "pypi"
    REPOSITORY_FILE = "repository_file"


class CollectionRule(BaseModel):
    model_config = ConfigDict(frozen=True)

    source: SourceSystem
    artifact_types: tuple[str, ...] = Field(min_length=1)
    file_paths: tuple[str, ...] = ()


class CohortRepository(BaseModel):
    model_config = ConfigDict(frozen=True)

    repository: str = Field(pattern=r"^[^/\s]+/[^/\s]+$")
    project_name: str
    inclusion_reason: str = Field(min_length=15)
    dependency_evidence: EvidenceReference | None = None
    selection_confidence: Confidence


class RepositoryCohort(BaseModel):
    model_config = ConfigDict(frozen=True)

    cohort_id: str = Field(pattern=r"^[a-z0-9][a-z0-9._-]*$")
    case_id: str = Field(pattern=r"^[a-z0-9][a-z0-9._-]*$")
    selection_method: CohortSelectionMethod
    selection_rationale: str = Field(min_length=25)
    repositories: tuple[CohortRepository, ...] = Field(min_length=1)
    created_at: datetime

    @model_validator(mode="after")
    def repositories_are_unique(self) -> RepositoryCohort:
        names = [item.repository.casefold() for item in self.repositories]
        if len(names) != len(set(names)):
            raise ValueError("cohort repositories must be unique")
        return self


class ReleaseCase(BaseModel):
    model_config = ConfigDict(frozen=True)

    case_id: str = Field(pattern=r"^[a-z0-9][a-z0-9._-]*$")
    target_package: str = Field(min_length=1)
    target_version: str = Field(min_length=1)
    upstream_repository: str = Field(pattern=r"^[^/\s]+/[^/\s]+$")
    release_timestamp: datetime
    ecosystem: str = "pypi"
    observation_window_start: date
    observation_window_end: date
    collection_rules: tuple[CollectionRule, ...] = Field(min_length=1)
    created_at: datetime

    @model_validator(mode="after")
    def validate_window(self) -> ReleaseCase:
        if self.observation_window_start > self.observation_window_end:
            raise ValueError("observation window start must not follow its end")
        release_day = self.release_timestamp.date()
        if not self.observation_window_start <= release_day <= self.observation_window_end:
            raise ValueError("release timestamp must fall within the observation window")
        if self.release_timestamp.tzinfo is None or self.created_at.tzinfo is None:
            raise ValueError("case timestamps must include a timezone")
        return self


class CaseDefinition(BaseModel):
    model_config = ConfigDict(frozen=True)

    case: ReleaseCase
    cohort: RepositoryCohort

    @model_validator(mode="after")
    def ids_match(self) -> CaseDefinition:
        if self.case.case_id != self.cohort.case_id:
            raise ValueError("case and cohort case_id values must match")
        return self
