"""Environment-backed settings with no secret persistence."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True, slots=True)
class Settings:
    github_token: str | None
    github_api_url: str = "https://api.github.com"
    pypi_api_url: str = "https://pypi.org/pypi"
    log_level: str = "INFO"

    @classmethod
    def from_env(cls, *, load_env_file: bool = True) -> Settings:
        if load_env_file:
            load_dotenv()
        return cls(
            github_token=os.getenv("GITHUB_TOKEN") or None,
            github_api_url=os.getenv("PULSE_GITHUB_API_URL", "https://api.github.com"),
            pypi_api_url=os.getenv("PULSE_PYPI_API_URL", "https://pypi.org/pypi"),
            log_level=os.getenv("PULSE_LOG_LEVEL", "INFO"),
        )
