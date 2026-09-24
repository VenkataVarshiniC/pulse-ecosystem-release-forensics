"""Immutable raw source envelopes."""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict

from pulse.collection.planner import CollectionTask
from pulse.models.case import SourceSystem


class RawSnapshot(BaseModel):
    model_config = ConfigDict(frozen=True)

    task_id: str
    case_id: str
    source: SourceSystem
    source_identifier: str
    query: dict[str, Any]
    retrieved_at: datetime
    payload: Any


class RawSnapshotStore:
    def __init__(
        self,
        root: Path,
        *,
        prepare_directory: Callable[[Path], None] | None = None,
        write_exclusive: Callable[[Path, str], None] | None = None,
    ) -> None:
        self.root = root
        self._prepare_directory = prepare_directory or _prepare_directory
        self._write_exclusive = write_exclusive or _write_exclusive

    def save(self, task: CollectionTask, payload: Any, retrieved_at: datetime) -> Path:
        slug = (task.repository or "upstream").replace("/", "__")
        directory = self.root / task.case_id / task.source.value / slug
        self._prepare_directory(directory)
        timestamp = retrieved_at.strftime("%Y%m%dT%H%M%S.%fZ")
        path = directory / f"{task.task_id}-{timestamp}.json"
        snapshot = RawSnapshot(
            task_id=task.task_id,
            case_id=task.case_id,
            source=task.source,
            source_identifier=task.repository or task.parameters.get("package", "unknown"),
            query={"kind": task.kind.value, **task.parameters},
            retrieved_at=retrieved_at,
            payload=payload,
        )
        self._write_exclusive(path, snapshot.model_dump_json(indent=2))
        return path


def _prepare_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _write_exclusive(path: Path, content: str) -> None:
    with path.open("x", encoding="utf-8") as handle:
        handle.write(content)
