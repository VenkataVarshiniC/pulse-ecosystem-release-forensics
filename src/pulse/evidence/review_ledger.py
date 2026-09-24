"""JSONL persistence for candidate and reviewed evidence."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from pulse.models.review import ReviewableEvidence


def load_review_ledger(path: Path) -> tuple[ReviewableEvidence, ...]:
    return tuple(
        ReviewableEvidence.model_validate_json(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    )


def write_review_ledger(path: Path, candidates: Iterable[ReviewableEvidence]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = "\n".join(item.model_dump_json() for item in candidates)
    path.write_text(f"{content}\n" if content else "", encoding="utf-8")
    return path
