"""Strict JSONL boundary for the processed evidence ledger."""

from __future__ import annotations

from pathlib import Path

from pydantic import ValidationError

from pulse.models.evidence import EvidenceEvent


class LedgerValidationError(ValueError):
    """Identify the ledger line that failed typed validation."""


def load_jsonl(path: Path) -> tuple[EvidenceEvent, ...]:
    events: list[EvidenceEvent] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                events.append(EvidenceEvent.model_validate_json(line))
            except ValidationError as exc:
                raise LedgerValidationError(f"invalid evidence ledger line {line_number}") from exc
    return tuple(events)
