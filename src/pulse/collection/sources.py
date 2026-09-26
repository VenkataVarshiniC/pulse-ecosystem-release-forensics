"""Normalized capabilities of Phase 1 public source systems."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from pulse.models.case import SourceSystem


class SourceCapability(BaseModel):
    model_config = ConfigDict(frozen=True)

    source: SourceSystem
    artifact_types: tuple[str, ...]
    preserves_raw_payload: bool = True
    time_bounded_artifacts: tuple[str, ...] = ()


SOURCE_REGISTRY = (
    SourceCapability(
        source=SourceSystem.GITHUB,
        artifact_types=(
            "repository",
            "release",
            "issue",
            "pull_request",
            "commit",
            "file_content",
        ),
        time_bounded_artifacts=("issue", "pull_request", "commit"),
    ),
    SourceCapability(
        source=SourceSystem.PYPI,
        artifact_types=("package_version", "artifact", "release_timestamp", "project_url"),
    ),
    SourceCapability(
        source=SourceSystem.REPOSITORY_FILE,
        artifact_types=("requirements.txt", "pyproject.toml", "setup.py", "setup.cfg"),
    ),
)
