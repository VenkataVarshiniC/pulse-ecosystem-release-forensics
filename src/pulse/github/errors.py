"""Structured GitHub client failures."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class GitHubApiError(RuntimeError):
    message: str
    status_code: int | None = None
    endpoint: str | None = None
    response_body: Any = None

    def __str__(self) -> str:
        status = f" status={self.status_code}" if self.status_code is not None else ""
        endpoint = f" endpoint={self.endpoint}" if self.endpoint else ""
        return f"{self.message}{status}{endpoint}"


class GitHubAuthenticationError(GitHubApiError):
    """Raised when authenticated access is unavailable or rejected."""
