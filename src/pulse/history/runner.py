"""Path-scoped history collection and conservative exact-ref comparison."""

from __future__ import annotations

import base64
import binascii
import hashlib
import re
import tomllib
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
from urllib.parse import quote
from uuid import uuid4

from packaging.utils import canonicalize_name

from pulse.collection.planner import historical_commit_task, historical_file_task
from pulse.collection.raw import CaptureMethod, RawSnapshotStore
from pulse.dependencies.parsers import parse_dependency_file_with_diagnostics
from pulse.dependencies.transitions import detect_transition
from pulse.github.client import GitHubClient
from pulse.github.errors import GitHubApiError
from pulse.history.models import (
    ChangeStatus,
    FileStateStatus,
    HistoricalFileState,
    HistoricalPathResult,
    HistoricalRef,
    HistoricalRun,
    PairStatus,
)
from pulse.history.pairing import select_ref_pair, unresolved_pair
from pulse.models.case import CaseDefinition, SourceSystem
from pulse.models.evidence import Confidence

SUPPORTED = ("requirements.txt", "pyproject.toml", "setup.py", "setup.cfg")
MAX_CONTENT_BYTES = 1_000_000


class HistoricalRunner:
    def __init__(self, client: GitHubClient, output_root: Path) -> None:
        self.client = client
        self.output_root = output_root
        self.raw = RawSnapshotStore(
            output_root / "data/raw", capture_method=CaptureMethod.COLLECTOR
        )

    def run(self, definition: CaseDefinition) -> tuple[HistoricalRun, Path]:
        started = datetime.now(UTC)
        run_id = uuid4().hex
        directory = (
            self.output_root / "data/interim" / definition.case.case_id / "historical" / run_id
        )
        directory.mkdir(parents=True, exist_ok=False)
        paths = sorted({
            path for rule in definition.case.collection_rules
            if rule.source in {SourceSystem.GITHUB, SourceSystem.REPOSITORY_FILE}
            for path in rule.file_paths if path.endswith(SUPPORTED)
        })
        results = []
        for member in definition.cohort.repositories:
            repository_results = [
                self._collect_path(definition, member.repository, path, run_id)
                for path in paths
            ]
            results.extend(_flag_cross_file_migration(repository_results))
        run = HistoricalRun(
            run_id=run_id, case_id=definition.case.case_id,
            started_at=started, completed_at=datetime.now(UTC), results=tuple(results),
        )
        manifest = directory / "manifest.json"
        with manifest.open("x", encoding="utf-8") as handle:
            handle.write(run.model_dump_json(indent=2))
        return run, manifest

    def _collect_path(
        self, definition: CaseDefinition, repository: str, path: str, run_id: str,
    ) -> HistoricalPathResult:
        case = definition.case
        since = f"{case.observation_window_start.isoformat()}T00:00:00Z"
        until_day = case.observation_window_end + timedelta(days=1)
        until = f"{until_day.isoformat()}T00:00:00Z"
        task = historical_commit_task(definition, repository, path, since, until)
        self.client.reset_stats()
        commits: list[dict[str, Any]] = []
        error: GitHubApiError | None = None
        try:
            for item in self.client.commits(repository, path=path, since=since, until=until):
                commits.append(item)
        except GitHubApiError as exc:
            error = exc
        stats = self.client.stats.model_copy(deep=True)
        snapshot = self.raw.save(
            task, commits, datetime.now(UTC), run_id=run_id,
            attempt_id=uuid4().hex, stats=stats,
        )
        if error or stats.termination != "complete":
            reason = (
                "Path history collection was incomplete; no anchors selected "
                f"({error.failure_kind if error else stats.termination})."
            )
            pair = unresolved_pair(
                definition, repository, path, PairStatus.COLLECTION_FAILED, reason
            )
            return HistoricalPathResult(
                pair=pair, history_snapshot_path=str(snapshot), history_stats=stats,
            )
        pair = select_ref_pair(definition, repository, path, commits)
        if pair.status is not PairStatus.PAIRED:
            before = self._file_state(definition, pair.before, run_id) if pair.before else None
            after = self._file_state(definition, pair.after, run_id) if pair.after else None
            return HistoricalPathResult(
                pair=pair, history_snapshot_path=str(snapshot), history_stats=stats,
                before_state=before, after_state=after,
            )
        assert pair.before is not None and pair.after is not None
        before = self._file_state(definition, pair.before, run_id)
        after = self._file_state(definition, pair.after, run_id)
        if (
            before.status is not FileStateStatus.PARSED
            or after.status is not FileStateStatus.PARSED
        ):
            status = (PairStatus.FILE_UNAVAILABLE if any(
                item.status in {FileStateStatus.NOT_FOUND, FileStateStatus.UNAVAILABLE}
                for item in (before, after)
            ) else PairStatus.MALFORMED)
            pair = pair.model_copy(update={
                "status": status, "confidence": Confidence.LOW,
                "reason": (
                    "At least one exact-ref manifest could not be parsed; absence is unknown."
                ),
            })
            return HistoricalPathResult(
                pair=pair, history_snapshot_path=str(snapshot), history_stats=stats,
                before_state=before, after_state=after,
            )
        if len(before.target_observations) > 1 or len(after.target_observations) > 1:
            if _same_grouped_observations(before, after):
                pair = pair.model_copy(update={"confidence": Confidence.HIGH})
                return HistoricalPathResult(
                    pair=pair, history_snapshot_path=str(snapshot), history_stats=stats,
                    before_state=before, after_state=after,
                    change_status=ChangeStatus.UNCHANGED,
                    notes=(
                        "All separately named dependency groups retained the same declarations.",
                    ),
                )
            pair = pair.model_copy(update={
                "status": PairStatus.AMBIGUOUS, "confidence": Confidence.LOW,
                "reason": (
                    "Multiple target declarations in a manifest require manual reconciliation."
                ),
            })
            return HistoricalPathResult(
                pair=pair, history_snapshot_path=str(snapshot), history_stats=stats,
                before_state=before, after_state=after,
            )
        transition = detect_transition(
            before.target_observations[0] if before.target_observations else None,
            after.target_observations[0] if after.target_observations else None,
            target_version=case.target_version,
        )
        status = ChangeStatus(transition.kind.value) if transition else ChangeStatus.UNCHANGED
        pair = pair.model_copy(update={"confidence": Confidence.HIGH})
        return HistoricalPathResult(
            pair=pair, history_snapshot_path=str(snapshot), history_stats=stats,
            before_state=before, after_state=after, transition=transition,
            change_status=status,
        )

    def _file_state(
        self, definition: CaseDefinition, ref: HistoricalRef, run_id: str,
    ) -> HistoricalFileState:
        repository, path, sha = ref.repository, ref.path, ref.commit_sha
        encoded = quote(path, safe="/")
        api_url = f"{self.client.api_base_url}/repos/{repository}/contents/{encoded}?ref={sha}"
        source_url = f"https://github.com/{repository}/blob/{sha}/{encoded}"
        common = dict(
            repository=repository, path=path, commit_sha=sha,
            commit_timestamp=ref.commit_timestamp, api_url=api_url,
            source_url=source_url, retrieved_at=datetime.now(UTC),
            capture_method=CaptureMethod.COLLECTOR,
        )
        self.client.reset_stats()
        try:
            payload = self.client.contents(repository, path, ref=sha)
        except GitHubApiError as exc:
            return HistoricalFileState(
                **common, status=(FileStateStatus.NOT_FOUND if exc.failure_kind == "not_found"
                                  else FileStateStatus.UNAVAILABLE),
                diagnostics=(f"Exact-ref retrieval failed ({exc.failure_kind}).",),
            )
        task = historical_file_task(definition, repository, path, sha)
        snapshot = self.raw.save(
            task, payload, datetime.now(UTC), run_id=run_id,
            attempt_id=uuid4().hex, stats=self.client.stats.model_copy(deep=True),
        )
        try:
            content = _decode_content(payload)
            observations, unparsed = parse_dependency_file_with_diagnostics(
                repository=repository, file_path=path, content=content,
                commit_reference=sha, observed_at=ref.commit_timestamp,
                source=source_url,
            )
            target = canonicalize_name(definition.case.target_package)
            selected = tuple(obs for obs in observations if obs.package == target)
            diagnostics = _uncertainty(content, path, unparsed)
            if diagnostics:
                return HistoricalFileState(
                    **common, status=FileStateStatus.INVALID,
                    content_sha256=hashlib.sha256(content.encode()).hexdigest(),
                    raw_snapshot_path=str(snapshot), diagnostics=diagnostics,
                    target_observations=selected,
                )
            return HistoricalFileState(
                **common, status=FileStateStatus.PARSED,
                content_sha256=hashlib.sha256(content.encode()).hexdigest(),
                raw_snapshot_path=str(snapshot), target_observations=selected,
            )
        except (ValueError, TypeError, UnicodeError, binascii.Error, SyntaxError) as exc:
            return HistoricalFileState(
                **common, status=FileStateStatus.INVALID,
                raw_snapshot_path=str(snapshot),
                diagnostics=(f"Manifest decode or parse failed ({type(exc).__name__}).",),
            )


def _decode_content(payload: Any) -> str:
    if not isinstance(payload, dict) or payload.get("type") != "file":
        raise ValueError("Expected a file content response")
    if payload.get("encoding") != "base64" or not isinstance(payload.get("content"), str):
        raise ValueError("Expected inline base64 content")
    binary = base64.b64decode("".join(payload["content"].split()), validate=True)
    if len(binary) > MAX_CONTENT_BYTES or (
        isinstance(payload.get("size"), int) and payload["size"] != len(binary)
    ):
        raise ValueError("Content too large or size mismatch")
    return binary.decode("utf-8")


def _uncertainty(
    content: str, path: str, unparsed: tuple[str, ...],
) -> tuple[str, ...]:
    notes = []
    if unparsed:
        notes.append("Unparsed dependency declarations prevent an exhaustive comparison.")
    if path.endswith(("requirements.txt", "setup.cfg")) and re.search(
        r"(?m)^\s*-(?:r|c|-[a-z-]+)\b", content
    ):
        notes.append("Requirements indirection or options prevent an exhaustive comparison.")
    if path.endswith("pyproject.toml"):
        project = tomllib.loads(content).get("project", {})
        dynamic = project.get("dynamic", [])
        if set(dynamic) & {"dependencies", "optional-dependencies"}:
            notes.append("Dynamic dependency metadata prevents an exhaustive comparison.")
    if path.endswith("setup.py") and not re.search(r"install_requires\s*=\s*[\[(]", content):
        notes.append("No literal install_requires list can be established in setup.py.")
    return tuple(notes)


def _flag_cross_file_migration(
    results: list[HistoricalPathResult],
) -> list[HistoricalPathResult]:
    kinds = {result.change_status for result in results}
    statuses = {result.pair.status for result in results}
    if {PairStatus.MISSING_BEFORE, PairStatus.MISSING_AFTER} <= statuses:
        results = [
            result.model_copy(update={
                "notes": (*result.notes, "Complementary path histories may indicate a "
                          "manifest migration; no cross-file transition is inferred."),
            }) if result.pair.status in {PairStatus.MISSING_BEFORE, PairStatus.MISSING_AFTER}
            else result
            for result in results
        ]
    if not {ChangeStatus.INTRODUCED, ChangeStatus.REMOVED} <= kinds:
        return results
    amended = []
    for result in results:
        if result.change_status in {ChangeStatus.INTRODUCED, ChangeStatus.REMOVED}:
            pair = result.pair.model_copy(update={
                "status": PairStatus.AMBIGUOUS, "confidence": Confidence.LOW,
                "reason": "Opposite target changes across manifests may be a path migration.",
            })
            result = result.model_copy(update={
                "pair": pair, "transition": None, "change_status": ChangeStatus.UNKNOWN,
                "notes": (*result.notes, "Cross-file migration requires manual reconciliation."),
            })
        amended.append(result)
    return amended


def _same_grouped_observations(
    before: HistoricalFileState, after: HistoricalFileState,
) -> bool:
    def grouped(state: HistoricalFileState) -> dict[str | None, tuple[Any, ...]] | None:
        result = {}
        for item in state.target_observations:
            if item.declaration_group in result:
                return None
            result[item.declaration_group] = (
                item.constraint, item.marker, item.extras, item.direct_reference,
            )
        return result

    prior, later = grouped(before), grouped(after)
    return prior is not None and later is not None and prior == later
