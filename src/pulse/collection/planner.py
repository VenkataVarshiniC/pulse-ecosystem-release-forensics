"""Expand a case and cohort into an inspectable collection plan."""

from __future__ import annotations

import hashlib
import json
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, model_validator

from pulse.models.case import CaseDefinition, SourceSystem


class TaskKind(StrEnum):
    PYPI_VERSION = "pypi_version"
    GITHUB_REPOSITORY = "github_repository"
    GITHUB_RELEASES = "github_releases"
    GITHUB_ISSUES = "github_issues"
    GITHUB_PULL_REQUESTS = "github_pull_requests"
    GITHUB_COMMITS = "github_commits"
    GITHUB_FILE = "github_file"


class TaskRequirement(StrEnum):
    REQUIRED = "required"
    OPTIONAL_PROBE = "optional_probe"


class CollectionTask(BaseModel):
    model_config = ConfigDict(frozen=True)

    task_id: str
    case_id: str
    source: SourceSystem
    kind: TaskKind
    repository: str | None = None
    parameters: dict[str, Any]
    requirement: TaskRequirement = TaskRequirement.REQUIRED

    @model_validator(mode="after")
    def optional_is_a_file_probe(self) -> CollectionTask:
        if (
            self.requirement is TaskRequirement.OPTIONAL_PROBE
            and self.kind is not TaskKind.GITHUB_FILE
        ):
            raise ValueError("Only configured file probes may be optional")
        return self


class CollectionPlan(BaseModel):
    model_config = ConfigDict(frozen=True)

    case_id: str
    tasks: tuple[CollectionTask, ...]


def _task(
    definition: CaseDefinition,
    source: SourceSystem,
    kind: TaskKind,
    *,
    repository: str | None = None,
    requirement: TaskRequirement = TaskRequirement.REQUIRED,
    **parameters: Any,
) -> CollectionTask:
    identity = {
        "case_id": definition.case.case_id,
        "source": source.value,
        "kind": kind.value,
        "repository": repository,
        "parameters": parameters,
    }
    digest = hashlib.sha256(
        json.dumps(identity, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()[:20]
    return CollectionTask(task_id=digest, requirement=requirement, **identity)


def plan_collection(definition: CaseDefinition) -> CollectionPlan:
    case = definition.case
    tasks = [
        _task(
            definition,
            SourceSystem.PYPI,
            TaskKind.PYPI_VERSION,
            package=case.target_package,
            version=case.target_version,
        ),
        _task(
            definition,
            SourceSystem.GITHUB,
            TaskKind.GITHUB_REPOSITORY,
            repository=case.upstream_repository,
        ),
        _task(
            definition,
            SourceSystem.GITHUB,
            TaskKind.GITHUB_RELEASES,
            repository=case.upstream_repository,
        ),
    ]
    window = {
        "since": case.observation_window_start.isoformat(),
        "until": case.observation_window_end.isoformat(),
    }
    file_paths = {
        path
        for rule in case.collection_rules
        if rule.source in {SourceSystem.GITHUB, SourceSystem.REPOSITORY_FILE}
        for path in rule.file_paths
    }
    for member in definition.cohort.repositories:
        repository = member.repository
        tasks.extend(
            [
                _task(
                    definition,
                    SourceSystem.GITHUB,
                    TaskKind.GITHUB_REPOSITORY,
                    repository=repository,
                ),
                _task(
                    definition,
                    SourceSystem.GITHUB,
                    TaskKind.GITHUB_ISSUES,
                    repository=repository,
                    **window,
                ),
                _task(
                    definition,
                    SourceSystem.GITHUB,
                    TaskKind.GITHUB_PULL_REQUESTS,
                    repository=repository,
                    **window,
                ),
                _task(
                    definition,
                    SourceSystem.GITHUB,
                    TaskKind.GITHUB_COMMITS,
                    repository=repository,
                    **window,
                ),
            ]
        )
        tasks.extend(
            _task(
                definition,
                SourceSystem.REPOSITORY_FILE,
                TaskKind.GITHUB_FILE,
                repository=repository,
                requirement=TaskRequirement.OPTIONAL_PROBE,
                path=path,
            )
            for path in sorted(file_paths)
        )
    return CollectionPlan(case_id=case.case_id, tasks=tuple(tasks))
