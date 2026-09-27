"""Typed dependency observations and transitions."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class DependencyObservation(BaseModel):
    model_config = ConfigDict(frozen=True)

    repository: str
    file_path: str
    package: str
    constraint: str
    commit_reference: str
    observed_at: datetime
    source: HttpUrl
    raw_requirement: str | None = None
    declared_package: str | None = None
    raw_constraint: str | None = None
    marker: str | None = None
    extras: tuple[str, ...] = ()
    direct_reference: str | None = None
    declaration_group: str | None = None


class TransitionKind(StrEnum):
    INTRODUCED = "introduced"
    REMOVED = "removed"
    CONSTRAINT_CHANGED = "constraint_changed"
    TARGET_EXCLUDED = "target_excluded"
    TARGET_ACCEPTED = "target_accepted"


class DependencyTransition(BaseModel):
    model_config = ConfigDict(frozen=True)

    repository: str
    package: str
    before: DependencyObservation | None
    after: DependencyObservation | None
    target_version: str
    kind: TransitionKind
    reason: str = Field(min_length=15)
