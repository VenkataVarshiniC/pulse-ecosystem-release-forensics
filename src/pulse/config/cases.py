"""Load declarative forensic case definitions."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from pulse.models.case import CaseDefinition


class CaseConfigurationError(ValueError):
    """Raised when a case file cannot be parsed or validated."""


def load_case(path: Path) -> CaseDefinition:
    try:
        payload: Any = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise CaseConfigurationError("case configuration must contain a mapping")
        return CaseDefinition.model_validate(payload)
    except (OSError, yaml.YAMLError, ValueError) as exc:
        if isinstance(exc, CaseConfigurationError):
            raise
        raise CaseConfigurationError(f"invalid case configuration: {path}") from exc
