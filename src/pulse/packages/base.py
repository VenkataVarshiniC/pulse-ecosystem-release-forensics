"""Package ecosystem boundary used by forensic collectors."""

from __future__ import annotations

from datetime import datetime
from typing import Protocol

from pydantic import BaseModel, ConfigDict, HttpUrl


class PackageRelease(BaseModel):
    model_config = ConfigDict(frozen=True)

    package: str
    version: str
    uploaded_at: datetime
    artifact_url: HttpUrl
    python_requires: str | None = None


class PackageMetadata(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    latest_version: str
    project_url: HttpUrl
    repository_url: HttpUrl | None = None
    releases: tuple[PackageRelease, ...]


class PackageIndex(Protocol):
    def package(self, name: str, *, version: str | None = None) -> PackageMetadata: ...
