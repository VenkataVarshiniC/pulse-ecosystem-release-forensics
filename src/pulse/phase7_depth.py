"""Bounded Phase 7 evidence-depth collection and offline evaluation."""

from __future__ import annotations

import base64
import hashlib
import json
import re
import time
import tomllib
from collections import Counter
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from datetime import time as datetime_time
from enum import StrEnum
from pathlib import Path
from typing import Any
from urllib.parse import quote
from uuid import uuid4

import httpx
from packaging.utils import canonicalize_name
from pydantic import BaseModel, ConfigDict, Field, model_validator

from pulse.collection.planner import CollectionTask, TaskKind, TaskRequirement
from pulse.collection.raw import CaptureMethod, RawSnapshot, RawSnapshotStore
from pulse.config.cases import load_case
from pulse.dependencies.parsers import parse_dependency_file_with_diagnostics
from pulse.models.case import CaseDefinition, SourceSystem

ROOT = Path(__file__).resolve().parents[2]
TREATMENT_METHOD = "p7-boundary-anchor-depth-v1"
RECONSTRUCTION_VERSION = "repository-boundary-pair-v1"
PREREQUISITE_VERSION = "p7-question-prerequisites-v1"
EVALUATION_VERSION = "p7-evaluation-v1"
ALLOWED_CASES = ("pytest-8.0.0", "urllib3-2.0.0")
ALLOWED_PATHS = ("pyproject.toml", "requirements.txt")
LIFECYCLE_QUESTIONS = (
    "adoption_readiness",
    "observed_adoption",
    "migration_friction",
    "remediation",
    "recovery_signal",
)
_SHA_RE = re.compile(r"^[0-9a-f]{40}(?:[0-9a-f]{24})?$")
_TRANSIENT = {500, 502, 503, 504}


class SourceAvailability(StrEnum):
    NOT_PLANNED = "NOT_PLANNED"
    AVAILABLE = "AVAILABLE"
    NOT_FOUND = "NOT_FOUND"
    INCOMPLETE = "INCOMPLETE"
    SOURCE_UNAVAILABLE = "SOURCE_UNAVAILABLE"
    STRUCTURALLY_UNAVAILABLE = "STRUCTURALLY_UNAVAILABLE"
    CONFLICTING = "CONFLICTING"


class AnchorRole(StrEnum):
    PRE_RELEASE = "PRE_RELEASE"
    OBSERVATION_END = "OBSERVATION_END"


class HistoryState(StrEnum):
    PAIRED = "PAIRED"
    AFTER_ONLY = "AFTER_ONLY"
    UNRESOLVED = "UNRESOLVED"


class SufficiencyState(StrEnum):
    SUFFICIENT = "SUFFICIENT"
    INSUFFICIENT = "INSUFFICIENT"


class FindingState(StrEnum):
    YES = "YES"
    NO_QUALIFYING_EVIDENCE_FOUND = "NO_QUALIFYING_EVIDENCE_FOUND"
    UNKNOWN = "UNKNOWN"


class StopReason(StrEnum):
    BOUNDED_REQUESTS_COMPLETE = "BOUNDED_REQUESTS_COMPLETE"
    ANCHOR_NOT_FOUND = "ANCHOR_NOT_FOUND"
    AFTER_ANCHOR_NOT_AFTER_RELEASE = "AFTER_ANCHOR_NOT_AFTER_RELEASE"
    PATH_NOT_FOUND_AT_REF = "PATH_NOT_FOUND_AT_REF"
    BOTH_PATH_STATES_NOT_FOUND = "BOTH_PATH_STATES_NOT_FOUND"
    SOURCE_ACCESS_STOP = "SOURCE_ACCESS_STOP"
    RESPONSE_INCOMPLETE = "RESPONSE_INCOMPLETE"
    PARSE_INCOMPLETE = "PARSE_INCOMPLETE"
    CONFLICTING_DECLARATIONS = "CONFLICTING_DECLARATIONS"
    SOURCE_NOT_PLANNED = "SOURCE_NOT_PLANNED"


class SourceAttempt(BaseModel):
    model_config = ConfigDict(frozen=True)

    task_id: str
    case_id: str
    repository: str
    source_type: str
    anchor_role: AnchorRole
    path: str | None = None
    ref: str | None = None
    availability: SourceAvailability
    stop_reason: StopReason
    reason: str
    event_time: datetime | None = None
    retrieved_at: datetime
    raw_path: str
    raw_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    content_sha256: str | None = Field(default=None, pattern=r"^[0-9a-f]{64}$")
    retry_count: int = Field(ge=0, le=3)


class BoundaryAnchor(BaseModel):
    model_config = ConfigDict(frozen=True)

    role: AnchorRole
    commit_sha: str = Field(pattern=r"^[0-9a-f]{40}(?:[0-9a-f]{24})?$")
    commit_timestamp: datetime
    source_attempt_id: str


class ExactRefFileState(BaseModel):
    model_config = ConfigDict(frozen=True)

    repository: str
    path: str
    anchor_role: AnchorRole
    ref: str | None
    event_time: datetime | None
    availability: SourceAvailability
    target_declarations: tuple[str, ...] = ()
    diagnostics: tuple[str, ...] = ()
    source_attempt_id: str


class HistoryRecord(BaseModel):
    model_config = ConfigDict(frozen=True)

    case_id: str
    repository: str
    path: str
    baseline_state: HistoryState
    treatment_state: HistoryState
    before: ExactRefFileState
    after: ExactRefFileState
    unresolved_reason: str | None = None
    stop_reason: StopReason
    provenance_attempt_ids: tuple[str, ...]


class PrerequisiteResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    availability: SourceAvailability
    satisfied: bool
    reason_code: str


class QuestionAssessment(BaseModel):
    model_config = ConfigDict(frozen=True)

    case_id: str
    repository: str
    question: str
    contract_version: str = PREREQUISITE_VERSION
    prerequisites: tuple[PrerequisiteResult, ...]
    sufficiency: SufficiencyState
    finding: FindingState
    reason_code: str
    support_attempt_ids: tuple[str, ...] = ()


class MemberChange(BaseModel):
    model_config = ConfigDict(frozen=True)

    case_id: str
    repository: str
    baseline_history: dict[str, int]
    treatment_history: dict[str, int]
    baseline_sufficient: int
    treatment_sufficient: int
    baseline_findings: dict[str, int]
    treatment_findings: dict[str, int]
    new_evidence_paths: tuple[str, ...]
    source_types: tuple[str, ...]
    history_changes: tuple[str, ...]
    sufficiency_changes: tuple[str, ...]
    finding_changes: tuple[str, ...]
    no_change_reason: str | None
    stop_reasons: tuple[StopReason, ...]
    provenance_attempt_ids: tuple[str, ...]


class ExperimentalMetric(BaseModel):
    model_config = ConfigDict(frozen=True)

    metric_id: str
    name: str
    numerator: int | None
    denominator: int | None
    value: float | None
    status: str
    interpretation: str


class CandidateSummary(BaseModel):
    model_config = ConfigDict(frozen=True)

    candidates: int
    accepted: int
    rejected: int
    distinct_artifacts: int


class ResultSummary(BaseModel):
    model_config = ConfigDict(frozen=True)

    declared_members: int
    core_collected_members: int
    historical_records: int
    history_states: dict[str, int]
    eligible_assessments: int
    sufficient: int
    insufficient: int
    findings: dict[str, int]
    support_links: int
    candidates: CandidateSummary


class Phase7RunManifest(BaseModel):
    model_config = ConfigDict(frozen=True)

    run_id: str
    treatment_method: str = TREATMENT_METHOD
    reconstruction_version: str = RECONSTRUCTION_VERSION
    prerequisite_version: str = PREREQUISITE_VERSION
    started_at: datetime
    completed_at: datetime
    case_ids: tuple[str, ...] = ALLOWED_CASES
    baseline_digests: dict[str, str]
    attempts: tuple[SourceAttempt, ...]

    @model_validator(mode="after")
    def exact_population(self) -> Phase7RunManifest:
        if self.case_ids != ALLOWED_CASES:
            raise ValueError("Phase 7 manifest must contain the two frozen cases")
        if self.treatment_method != TREATMENT_METHOD:
            raise ValueError("Phase 7 treatment method version is not frozen")
        if self.reconstruction_version != RECONSTRUCTION_VERSION:
            raise ValueError("Phase 7 reconstruction version is not frozen")
        if self.prerequisite_version != PREREQUISITE_VERSION:
            raise ValueError("Phase 7 prerequisite version is not frozen")
        if len(self.attempts) != 48:
            raise ValueError("Phase 7 manifest must contain exactly 48 bounded attempts")
        anchors = tuple(item for item in self.attempts if item.path is None)
        files = tuple(item for item in self.attempts if item.path is not None)
        if len(anchors) != 16 or len(files) != 32:
            raise ValueError("Phase 7 requires 16 anchor and 32 file attempts")
        if len({item.task_id for item in self.attempts}) != 48:
            raise ValueError("Phase 7 attempt task identities must be unique")
        if any(item.path not in ALLOWED_PATHS for item in files):
            raise ValueError("Phase 7 file attempt left the frozen paths")
        if any(
            Path(item.raw_path).is_absolute()
            or ".." in Path(item.raw_path).parts
            or Path(item.raw_path).parts[:3] != ("data", "raw", "phase-7")
            for item in self.attempts
        ):
            raise ValueError("Phase 7 raw path left the isolated raw root")
        return self


class Phase7Evaluation(BaseModel):
    model_config = ConfigDict(frozen=True)

    evaluation_version: str = EVALUATION_VERSION
    run_id: str
    treatment_method: str
    reconstruction_version: str
    prerequisite_version: str
    baseline_digests: dict[str, str]
    baseline: ResultSummary
    treatment: ResultSummary
    history_delta: dict[str, int]
    finding_delta: dict[str, int]
    unknown_delta: int
    bounded_no_delta: int
    positive_delta: int
    support_link_delta: int
    candidate_invariant: bool
    source_availability_attempts: dict[str, int]
    source_availability_prerequisites: dict[str, int]
    unresolved_history_reasons: dict[str, int]
    unresolved_question_reasons: dict[str, int]
    metrics: tuple[ExperimentalMetric, ...]
    history_records: tuple[HistoryRecord, ...]
    assessments: tuple[QuestionAssessment, ...]
    member_changes: tuple[MemberChange, ...]
    provenance_complete: bool
    baseline_unchanged: bool


class SourceCollectionError(RuntimeError):
    def __init__(self, kind: str, *, status_code: int | None = None) -> None:
        super().__init__(kind)
        self.kind = kind
        self.status_code = status_code


@dataclass(frozen=True, slots=True)
class _Response:
    status_code: int
    content: bytes
    retry_count: int


class Phase7PublicSource:
    """Small public-source client restricted by the frozen Phase 7 caller."""

    def __init__(
        self,
        token: str | None = None,
        *,
        timeout_seconds: float = 30.0,
        max_retries: int = 3,
        max_wait_seconds: float = 60.0,
        client: httpx.Client | None = None,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "pulse-release-forensics/phase7",
        }
        if token and token.strip():
            headers["Authorization"] = f"Bearer {token.strip()}"
        self._owns_client = client is None
        self._client = client or httpx.Client(timeout=timeout_seconds, headers=headers)
        self._max_retries = max_retries
        self._max_wait_seconds = max_wait_seconds
        self._sleep = sleep

    def __enter__(self) -> Phase7PublicSource:
        return self

    def __exit__(self, *_: object) -> None:
        if self._owns_client:
            self._client.close()

    def get(self, url: str, *, params: dict[str, str] | None = None) -> _Response:
        for attempt in range(self._max_retries + 1):
            try:
                response = self._client.get(url, params=params)
            except httpx.TransportError:
                if attempt == self._max_retries:
                    raise SourceCollectionError("transport_failed") from None
                self._sleep(min(2**attempt, self._max_wait_seconds))
                continue
            if response.status_code in _TRANSIENT:
                if attempt == self._max_retries:
                    raise SourceCollectionError(
                        "transient_failed", status_code=response.status_code
                    )
                self._sleep(min(2**attempt, self._max_wait_seconds))
                continue
            if response.status_code in {403, 429}:
                raise SourceCollectionError(
                    "rate_limited_or_forbidden", status_code=response.status_code
                )
            if response.status_code not in {200, 404}:
                raise SourceCollectionError(
                    "source_failed", status_code=response.status_code
                )
            return _Response(response.status_code, response.content, attempt)
        raise AssertionError("unreachable")


def baseline_paths(root: Path = ROOT) -> tuple[Path, ...]:
    return (
        root / "cases/pytest-8.0.0.yaml",
        root / "cases/urllib3-2.0.0.yaml",
        root / "data/processed/phase-2/pytest-8.0.0/forensics.json",
        root / "data/processed/phase-2/urllib3-2.0.0/forensics.json",
        root / "data/processed/m4-1/replay.json",
        root / "data/validation/m4-1b-reconciliation.json",
        root / "data/validation/m4-1b-publication-manifest.json",
    )


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def baseline_digests(root: Path = ROOT) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): file_sha256(path)
        for path in baseline_paths(root)
    }


def _task(
    definition: CaseDefinition,
    repository: str,
    kind: TaskKind,
    source: SourceSystem,
    **parameters: Any,
) -> CollectionTask:
    identity = {
        "case_id": definition.case.case_id,
        "repository": repository,
        "kind": kind.value,
        "source": source.value,
        "parameters": parameters,
    }
    task_id = hashlib.sha256(
        json.dumps(identity, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()[:20]
    return CollectionTask(
        task_id=task_id,
        case_id=definition.case.case_id,
        source=source,
        kind=kind,
        repository=repository,
        parameters=parameters,
        requirement=TaskRequirement.REQUIRED,
    )


def _save_raw(
    store: RawSnapshotStore,
    root: Path,
    task: CollectionTask,
    payload: dict[str, Any],
    retrieved_at: datetime,
    run_id: str,
) -> tuple[str, str]:
    path = store.save(
        task,
        payload,
        retrieved_at,
        run_id=run_id,
        attempt_id=uuid4().hex,
    )
    return path.relative_to(root).as_posix(), file_sha256(path)


def _failure_availability(kind: str) -> SourceAvailability:
    return (
        SourceAvailability.SOURCE_UNAVAILABLE
        if kind in {"rate_limited_or_forbidden", "source_failed"}
        else SourceAvailability.INCOMPLETE
    )


def _parse_commit(payload: Any) -> tuple[str, datetime] | None:
    if not isinstance(payload, list) or not payload:
        return None
    if len(payload) != 1 or not isinstance(payload[0], dict):
        raise ValueError("anchor response must contain one commit")
    item = payload[0]
    sha = item.get("sha")
    raw_date = item.get("commit", {}).get("committer", {}).get("date")
    if not isinstance(sha, str) or not _SHA_RE.fullmatch(sha) or not isinstance(raw_date, str):
        raise ValueError("anchor response lacks stable SHA or committer time")
    timestamp = datetime.fromisoformat(raw_date.replace("Z", "+00:00"))
    if timestamp.tzinfo is None:
        raise ValueError("anchor timestamp lacks timezone")
    return sha, timestamp.astimezone(UTC)


def _collect_anchor(
    definition: CaseDefinition,
    repository: str,
    role: AnchorRole,
    until: datetime,
    client: Phase7PublicSource,
    store: RawSnapshotStore,
    root: Path,
    run_id: str,
) -> tuple[BoundaryAnchor | None, SourceAttempt]:
    retrieved_at = datetime.now(UTC)
    url = f"https://api.github.com/repos/{repository}/commits"
    task = _task(
        definition,
        repository,
        TaskKind.GITHUB_COMMITS,
        SourceSystem.GITHUB,
        until=until.isoformat(),
        per_page=1,
        anchor_role=role.value,
        method_version=TREATMENT_METHOD,
    )
    try:
        response = client.get(url, params={"until": until.isoformat(), "per_page": "1"})
        body = json.loads(response.content)
        parsed = _parse_commit(body)
        payload = {"status_code": response.status_code, "url": url, "body": body}
        raw_path, raw_sha = _save_raw(store, root, task, payload, retrieved_at, run_id)
        if parsed is None:
            attempt = SourceAttempt(
                task_id=task.task_id,
                case_id=definition.case.case_id,
                repository=repository,
                source_type="repository_commits",
                anchor_role=role,
                availability=SourceAvailability.STRUCTURALLY_UNAVAILABLE,
                stop_reason=StopReason.ANCHOR_NOT_FOUND,
                reason="No repository commit was returned at or before the bounded anchor.",
                retrieved_at=retrieved_at,
                raw_path=raw_path,
                raw_sha256=raw_sha,
                retry_count=response.retry_count,
            )
            return None, attempt
        sha, event_time = parsed
        if role is AnchorRole.OBSERVATION_END and event_time <= definition.case.release_timestamp:
            attempt = SourceAttempt(
                task_id=task.task_id,
                case_id=definition.case.case_id,
                repository=repository,
                source_type="repository_commits",
                anchor_role=role,
                ref=sha,
                availability=SourceAvailability.STRUCTURALLY_UNAVAILABLE,
                stop_reason=StopReason.AFTER_ANCHOR_NOT_AFTER_RELEASE,
                reason="Latest bounded observation-end commit did not occur after release.",
                event_time=event_time,
                retrieved_at=retrieved_at,
                raw_path=raw_path,
                raw_sha256=raw_sha,
                retry_count=response.retry_count,
            )
            return None, attempt
        attempt = SourceAttempt(
            task_id=task.task_id,
            case_id=definition.case.case_id,
            repository=repository,
            source_type="repository_commits",
            anchor_role=role,
            ref=sha,
            availability=SourceAvailability.AVAILABLE,
            stop_reason=StopReason.BOUNDED_REQUESTS_COMPLETE,
            reason="Latest repository commit at or before the frozen anchor was retrieved.",
            event_time=event_time,
            retrieved_at=retrieved_at,
            raw_path=raw_path,
            raw_sha256=raw_sha,
            retry_count=response.retry_count,
        )
        return BoundaryAnchor(
            role=role,
            commit_sha=sha,
            commit_timestamp=event_time,
            source_attempt_id=task.task_id,
        ), attempt
    except (SourceCollectionError, ValueError, json.JSONDecodeError) as exc:
        kind = exc.kind if isinstance(exc, SourceCollectionError) else "invalid_response"
        payload = {"url": url, "failure_kind": kind}
        raw_path, raw_sha = _save_raw(store, root, task, payload, retrieved_at, run_id)
        attempt = SourceAttempt(
            task_id=task.task_id,
            case_id=definition.case.case_id,
            repository=repository,
            source_type="repository_commits",
            anchor_role=role,
            availability=_failure_availability(kind),
            stop_reason=(
                StopReason.SOURCE_ACCESS_STOP
                if _failure_availability(kind) is SourceAvailability.SOURCE_UNAVAILABLE
                else StopReason.RESPONSE_INCOMPLETE
            ),
            reason=f"Bounded anchor retrieval stopped ({kind}).",
            retrieved_at=retrieved_at,
            raw_path=raw_path,
            raw_sha256=raw_sha,
            retry_count=3 if kind in {"transport_failed", "transient_failed"} else 0,
        )
        return None, attempt


def _manifest_diagnostics(content: str, path: str, unparsed: tuple[str, ...]) -> tuple[str, ...]:
    notes: list[str] = []
    if unparsed:
        notes.append("Unparsed dependency declarations prevent exhaustive comparison.")
    if path == "requirements.txt" and re.search(r"(?m)^\s*-(?:r|c|-[a-z-]+)\b", content):
        notes.append("Requirements indirection or options prevent exhaustive comparison.")
    if path == "pyproject.toml":
        project = tomllib.loads(content).get("project", {})
        dynamic = project.get("dynamic", [])
        if set(dynamic) & {"dependencies", "optional-dependencies"}:
            notes.append("Dynamic dependency metadata prevents exhaustive comparison.")
    return tuple(notes)


def _target_declarations(
    observations: tuple[Any, ...], target_package: str
) -> tuple[tuple[str, ...], bool]:
    """Return display declarations and detect incompatible duplicates by parser group."""
    target = canonicalize_name(target_package)
    selected = tuple(item for item in observations if item.package == target)
    declarations = tuple(
        sorted(item.raw_requirement or item.constraint for item in selected)
    )
    by_group: dict[str, set[tuple[Any, ...]]] = {}
    for item in selected:
        group = item.declaration_group or "__ungrouped__"
        signature = (
            item.constraint,
            item.marker,
            tuple(item.extras),
            item.direct_reference,
        )
        by_group.setdefault(group, set()).add(signature)
    conflicting = any(len(signatures) > 1 for signatures in by_group.values())
    return declarations, conflicting


def _virtual_file_attempt(
    definition: CaseDefinition,
    repository: str,
    path: str,
    role: AnchorRole,
    anchor_attempt: SourceAttempt,
    store: RawSnapshotStore,
    root: Path,
    run_id: str,
) -> tuple[ExactRefFileState, SourceAttempt]:
    retrieved_at = datetime.now(UTC)
    task = _task(
        definition,
        repository,
        TaskKind.GITHUB_FILE,
        SourceSystem.REPOSITORY_FILE,
        path=path,
        anchor_role=role.value,
        method_version=TREATMENT_METHOD,
        blocked_by=anchor_attempt.task_id,
    )
    availability = anchor_attempt.availability
    if availability is SourceAvailability.AVAILABLE:
        raise ValueError("virtual file attempt requires unavailable anchor")
    payload = {
        "request_performed": False,
        "blocked_by": anchor_attempt.task_id,
        "availability": availability.value,
    }
    raw_path, raw_sha = _save_raw(store, root, task, payload, retrieved_at, run_id)
    attempt = SourceAttempt(
        task_id=task.task_id,
        case_id=definition.case.case_id,
        repository=repository,
        source_type="repository_file",
        anchor_role=role,
        path=path,
        availability=availability,
        stop_reason=anchor_attempt.stop_reason,
        reason="Exact-ref file request was not planned after the anchor stop.",
        retrieved_at=retrieved_at,
        raw_path=raw_path,
        raw_sha256=raw_sha,
        retry_count=0,
    )
    return ExactRefFileState(
        repository=repository,
        path=path,
        anchor_role=role,
        ref=None,
        event_time=None,
        availability=availability,
        diagnostics=(attempt.reason,),
        source_attempt_id=task.task_id,
    ), attempt


def _collect_file(
    definition: CaseDefinition,
    repository: str,
    path: str,
    anchor: BoundaryAnchor,
    client: Phase7PublicSource,
    store: RawSnapshotStore,
    root: Path,
    run_id: str,
) -> tuple[ExactRefFileState, SourceAttempt]:
    retrieved_at = datetime.now(UTC)
    encoded = quote(path, safe="/")
    url = f"https://raw.githubusercontent.com/{repository}/{anchor.commit_sha}/{encoded}"
    task = _task(
        definition,
        repository,
        TaskKind.GITHUB_FILE,
        SourceSystem.REPOSITORY_FILE,
        path=path,
        ref=anchor.commit_sha,
        anchor_role=anchor.role.value,
        method_version=TREATMENT_METHOD,
    )
    try:
        response = client.get(url)
        payload = {
            "status_code": response.status_code,
            "url": url,
            "content_base64": base64.b64encode(response.content).decode(),
        }
        raw_path, raw_sha = _save_raw(store, root, task, payload, retrieved_at, run_id)
        if response.status_code == 404:
            attempt = SourceAttempt(
                task_id=task.task_id,
                case_id=definition.case.case_id,
                repository=repository,
                source_type="repository_file",
                anchor_role=anchor.role,
                path=path,
                ref=anchor.commit_sha,
                availability=SourceAvailability.NOT_FOUND,
                stop_reason=StopReason.PATH_NOT_FOUND_AT_REF,
                reason="Approved path returned 404 at the exact bounded ref.",
                event_time=anchor.commit_timestamp,
                retrieved_at=retrieved_at,
                raw_path=raw_path,
                raw_sha256=raw_sha,
                retry_count=response.retry_count,
            )
            return ExactRefFileState(
                repository=repository,
                path=path,
                anchor_role=anchor.role,
                ref=anchor.commit_sha,
                event_time=anchor.commit_timestamp,
                availability=SourceAvailability.NOT_FOUND,
                diagnostics=(attempt.reason,),
                source_attempt_id=task.task_id,
            ), attempt
        content_sha = hashlib.sha256(response.content).hexdigest()
        try:
            content = response.content.decode("utf-8")
            observations, unparsed = parse_dependency_file_with_diagnostics(
                repository=repository,
                file_path=path,
                content=content,
                commit_reference=anchor.commit_sha,
                observed_at=anchor.commit_timestamp,
                source=url,
            )
            diagnostics = _manifest_diagnostics(content, path, unparsed)
            declarations, conflicting = _target_declarations(
                observations, definition.case.target_package
            )
            if conflicting:
                diagnostics = (*diagnostics, "Conflicting target declarations share a group.")
                availability = SourceAvailability.CONFLICTING
                stop_reason = StopReason.CONFLICTING_DECLARATIONS
                reason = "Conflicting target declarations prevent a single bounded state."
            elif diagnostics:
                availability = SourceAvailability.INCOMPLETE
                stop_reason = StopReason.PARSE_INCOMPLETE
                reason = (
                    "Manifest parsing was incomplete; no exhaustive comparison is allowed."
                )
            else:
                availability = SourceAvailability.AVAILABLE
                stop_reason = StopReason.BOUNDED_REQUESTS_COMPLETE
                reason = "Approved path was retrieved and parsed at the exact bounded ref."
        except (UnicodeError, ValueError, TypeError, tomllib.TOMLDecodeError) as exc:
            declarations = ()
            diagnostics = (f"Manifest parse failed ({type(exc).__name__}).",)
            availability = SourceAvailability.INCOMPLETE
            stop_reason = StopReason.PARSE_INCOMPLETE
            reason = "Manifest parsing failed; absence and sufficiency remain unresolved."
        attempt = SourceAttempt(
            task_id=task.task_id,
            case_id=definition.case.case_id,
            repository=repository,
            source_type="repository_file",
            anchor_role=anchor.role,
            path=path,
            ref=anchor.commit_sha,
            availability=availability,
            stop_reason=stop_reason,
            reason=reason,
            event_time=anchor.commit_timestamp,
            retrieved_at=retrieved_at,
            raw_path=raw_path,
            raw_sha256=raw_sha,
            content_sha256=content_sha,
            retry_count=response.retry_count,
        )
        return ExactRefFileState(
            repository=repository,
            path=path,
            anchor_role=anchor.role,
            ref=anchor.commit_sha,
            event_time=anchor.commit_timestamp,
            availability=availability,
            target_declarations=declarations,
            diagnostics=diagnostics,
            source_attempt_id=task.task_id,
        ), attempt
    except SourceCollectionError as exc:
        payload = {"url": url, "failure_kind": exc.kind}
        raw_path, raw_sha = _save_raw(store, root, task, payload, retrieved_at, run_id)
        availability = _failure_availability(exc.kind)
        attempt = SourceAttempt(
            task_id=task.task_id,
            case_id=definition.case.case_id,
            repository=repository,
            source_type="repository_file",
            anchor_role=anchor.role,
            path=path,
            ref=anchor.commit_sha,
            availability=availability,
            stop_reason=(
                StopReason.SOURCE_ACCESS_STOP
                if availability is SourceAvailability.SOURCE_UNAVAILABLE
                else StopReason.RESPONSE_INCOMPLETE
            ),
            reason=f"Exact-ref file retrieval stopped ({exc.kind}).",
            event_time=anchor.commit_timestamp,
            retrieved_at=retrieved_at,
            raw_path=raw_path,
            raw_sha256=raw_sha,
            retry_count=3 if exc.kind in {"transport_failed", "transient_failed"} else 0,
        )
        return ExactRefFileState(
            repository=repository,
            path=path,
            anchor_role=anchor.role,
            ref=anchor.commit_sha,
            event_time=anchor.commit_timestamp,
            availability=availability,
            diagnostics=(attempt.reason,),
            source_attempt_id=task.task_id,
        ), attempt


def collect_phase7(
    output_root: Path,
    *,
    token: str | None = None,
    client: Phase7PublicSource | None = None,
) -> Path:
    root = output_root.resolve()
    started = datetime.now(UTC)
    run_id = uuid4().hex
    store = RawSnapshotStore(
        root / "data/raw/phase-7", capture_method=CaptureMethod.COLLECTOR
    )
    own_client = client is None
    source = client or Phase7PublicSource(token)
    attempts: list[SourceAttempt] = []
    try:
        for case_id in ALLOWED_CASES:
            definition = load_case(root / f"cases/{case_id}.yaml")
            paths = tuple(sorted({
                path
                for rule in definition.case.collection_rules
                for path in rule.file_paths
                if path in ALLOWED_PATHS
            }))
            if paths != ALLOWED_PATHS:
                raise ValueError(f"{case_id} does not match the frozen Phase 7 paths")
            end = datetime.combine(
                definition.case.observation_window_end,
                datetime_time.max,
                tzinfo=UTC,
            )
            for member in definition.cohort.repositories:
                repository = member.repository
                before, before_attempt = _collect_anchor(
                    definition,
                    repository,
                    AnchorRole.PRE_RELEASE,
                    definition.case.release_timestamp,
                    source,
                    store,
                    root,
                    run_id,
                )
                after, after_attempt = _collect_anchor(
                    definition,
                    repository,
                    AnchorRole.OBSERVATION_END,
                    end,
                    source,
                    store,
                    root,
                    run_id,
                )
                attempts.extend((before_attempt, after_attempt))
                for path in paths:
                    for anchor, anchor_attempt, role in (
                        (before, before_attempt, AnchorRole.PRE_RELEASE),
                        (after, after_attempt, AnchorRole.OBSERVATION_END),
                    ):
                        _, attempt = (
                            _collect_file(
                                definition,
                                repository,
                                path,
                                anchor,
                                source,
                                store,
                                root,
                                run_id,
                            )
                            if anchor is not None
                            else _virtual_file_attempt(
                                definition,
                                repository,
                                path,
                                role,
                                anchor_attempt,
                                store,
                                root,
                                run_id,
                            )
                        )
                        attempts.append(attempt)
    finally:
        if own_client:
            source.__exit__(None, None, None)
    manifest = Phase7RunManifest(
        run_id=run_id,
        started_at=started,
        completed_at=datetime.now(UTC),
        baseline_digests=baseline_digests(root),
        attempts=tuple(attempts),
    )
    directory = root / "data/validation/phase-7" / run_id
    directory.mkdir(parents=True, exist_ok=False)
    path = directory / "run-manifest.json"
    path.write_text(manifest.model_dump_json(indent=2) + "\n", encoding="utf-8")
    return path


def _baseline_reports(root: Path) -> dict[str, dict[str, Any]]:
    return {
        case_id: json.loads(
            (root / f"data/processed/phase-2/{case_id}/forensics.json").read_text(
                encoding="utf-8"
            )
        )
        for case_id in ALLOWED_CASES
    }


def _baseline_state(path: dict[str, Any]) -> HistoryState:
    if path["pair_status"] == "paired":
        return HistoryState.PAIRED
    if path["pair_status"] == "missing_before":
        return HistoryState.AFTER_ONLY
    return HistoryState.UNRESOLVED


def _load_raw_attempt(
    root: Path, attempt: SourceAttempt, expected_run_id: str | None = None
) -> RawSnapshot:
    path = root / attempt.raw_path
    if file_sha256(path) != attempt.raw_sha256:
        raise ValueError(f"Phase 7 raw digest drift: {attempt.raw_path}")
    snapshot = RawSnapshot.model_validate_json(path.read_text(encoding="utf-8"))
    if (
        snapshot.task_id != attempt.task_id
        or snapshot.case_id != attempt.case_id
        or snapshot.source_identifier != attempt.repository
        or snapshot.capture_method is not CaptureMethod.COLLECTOR
        or snapshot.run_id is None
        or (expected_run_id is not None and snapshot.run_id != expected_run_id)
    ):
        raise ValueError("Phase 7 raw identity mismatch")
    return snapshot


def _state_from_attempt(root: Path, attempt: SourceAttempt) -> ExactRefFileState:
    snapshot = _load_raw_attempt(root, attempt)
    declarations: tuple[str, ...] = ()
    diagnostics: tuple[str, ...] = ()
    if attempt.availability in {
        SourceAvailability.AVAILABLE,
        SourceAvailability.INCOMPLETE,
        SourceAvailability.CONFLICTING,
    }:
        payload = snapshot.payload
        if not isinstance(payload, dict) or "content_base64" not in payload:
            raise ValueError("Phase 7 file raw payload is incomplete")
        content_bytes = base64.b64decode(payload["content_base64"], validate=True)
        if hashlib.sha256(content_bytes).hexdigest() != attempt.content_sha256:
            raise ValueError("Phase 7 exact-ref content digest drift")
        content = content_bytes.decode("utf-8")
        definition = load_case(root / f"cases/{attempt.case_id}.yaml")
        observations, unparsed = parse_dependency_file_with_diagnostics(
            repository=attempt.repository,
            file_path=attempt.path or "",
            content=content,
            commit_reference=attempt.ref or "",
            observed_at=attempt.event_time or attempt.retrieved_at,
            source=f"https://raw.githubusercontent.com/{attempt.repository}/"
            f"{attempt.ref}/{attempt.path}",
        )
        declarations, conflicting = _target_declarations(
            observations, definition.case.target_package
        )
        diagnostics = _manifest_diagnostics(content, attempt.path or "", unparsed)
        if conflicting:
            diagnostics = (*diagnostics, "Conflicting target declarations share a group.")
        expected_availability = (
            SourceAvailability.CONFLICTING
            if conflicting
            else SourceAvailability.INCOMPLETE
            if diagnostics
            else SourceAvailability.AVAILABLE
        )
        if attempt.availability is not expected_availability:
            raise ValueError("Phase 7 source classification drift")
    elif attempt.availability is not SourceAvailability.NOT_FOUND:
        diagnostics = (attempt.reason,)
    return ExactRefFileState(
        repository=attempt.repository,
        path=attempt.path or "",
        anchor_role=attempt.anchor_role,
        ref=attempt.ref,
        event_time=attempt.event_time,
        availability=attempt.availability,
        target_declarations=declarations,
        diagnostics=diagnostics,
        source_attempt_id=attempt.task_id,
    )


def _history_state(before: ExactRefFileState, after: ExactRefFileState) -> tuple[
    HistoryState, str | None, StopReason
]:
    if (
        before.availability is SourceAvailability.AVAILABLE
        and after.availability is SourceAvailability.AVAILABLE
    ):
        return HistoryState.PAIRED, None, StopReason.BOUNDED_REQUESTS_COMPLETE
    if (
        before.availability is SourceAvailability.NOT_FOUND
        and after.availability is SourceAvailability.AVAILABLE
    ):
        return (
            HistoryState.AFTER_ONLY,
            "Approved path was absent at the exact pre-release ref and available after release.",
            StopReason.PATH_NOT_FOUND_AT_REF,
        )
    availabilities = {before.availability, after.availability}
    if availabilities == {SourceAvailability.NOT_FOUND}:
        return (
            HistoryState.UNRESOLVED,
            "Approved path was absent at both bounded refs; other paths were not searched.",
            StopReason.BOTH_PATH_STATES_NOT_FOUND,
        )
    if SourceAvailability.CONFLICTING in availabilities:
        stop = StopReason.CONFLICTING_DECLARATIONS
    elif SourceAvailability.INCOMPLETE in availabilities:
        stop = StopReason.PARSE_INCOMPLETE
    elif SourceAvailability.SOURCE_UNAVAILABLE in availabilities:
        stop = StopReason.SOURCE_ACCESS_STOP
    else:
        stop = StopReason.ANCHOR_NOT_FOUND
    return (
        HistoryState.UNRESOLVED,
        "At least one bounded exact-ref state was unavailable or ineligible for comparison.",
        stop,
    )


def _result_summary(
    reports: dict[str, dict[str, Any]],
    history: tuple[HistoryRecord, ...],
    assessments: tuple[QuestionAssessment, ...],
    candidates: CandidateSummary,
    *,
    baseline: bool,
) -> ResultSummary:
    if baseline:
        history_counts = Counter(item.baseline_state.value for item in history)
        finding_counts: Counter[str] = Counter()
        sufficient = 0
        for report in reports.values():
            for repository in report["repositories"]:
                sufficient += sum(repository["stage_sufficiency"].values())
                for finding in repository["stage_findings"].values():
                    state = finding["state"]
                    finding_counts[
                        "UNKNOWN" if state == "unknown_insufficient_data"
                        else "NO_QUALIFYING_EVIDENCE_FOUND"
                        if state == "no_qualifying_evidence_found"
                        else "YES"
                    ] += 1
    else:
        history_counts = Counter(item.treatment_state.value for item in history)
        sufficient = sum(
            item.sufficiency is SufficiencyState.SUFFICIENT for item in assessments
        )
        finding_counts = Counter(item.finding.value for item in assessments)
    return ResultSummary(
        declared_members=8,
        core_collected_members=8,
        historical_records=len(history),
        history_states={state.value: history_counts[state.value] for state in HistoryState},
        eligible_assessments=40,
        sufficient=sufficient,
        insufficient=40 - sufficient,
        findings={state.value: finding_counts[state.value] for state in FindingState},
        support_links=0,
        candidates=candidates,
    )


def _question_assessments(
    reports: dict[str, dict[str, Any]],
    history: tuple[HistoryRecord, ...],
) -> tuple[QuestionAssessment, ...]:
    by_member: dict[tuple[str, str], list[HistoryRecord]] = {}
    for item in history:
        by_member.setdefault((item.case_id, item.repository), []).append(item)
    assessments: list[QuestionAssessment] = []
    for case_id, report in reports.items():
        for repository in report["repositories"]:
            name = repository["repository"]
            records = by_member[(case_id, name)]
            core_complete = all(
                repository["collection_coverage"][key]["state"] == "complete"
                for key in (
                    "repository_metadata",
                    "issues",
                    "pull_requests",
                    "commits",
                    "reviewed_candidates",
                )
            )
            historical_target = any(
                item.treatment_state is HistoryState.PAIRED
                and bool(item.before.target_declarations)
                for item in records
            )
            history_availability = (
                SourceAvailability.AVAILABLE
                if historical_target
                else SourceAvailability.SOURCE_UNAVAILABLE
                if any(
                    SourceAvailability.SOURCE_UNAVAILABLE
                    in {item.before.availability, item.after.availability}
                    for item in records
                )
                else SourceAvailability.INCOMPLETE
                if any(
                    SourceAvailability.INCOMPLETE
                    in {item.before.availability, item.after.availability}
                    for item in records
                )
                else SourceAvailability.NOT_FOUND
            )
            for question in LIFECYCLE_QUESTIONS:
                if question in {"migration_friction", "remediation"}:
                    prerequisites = (
                        PrerequisiteResult(
                            name="core_and_review_sources",
                            availability=(
                                SourceAvailability.AVAILABLE
                                if core_complete
                                else SourceAvailability.INCOMPLETE
                            ),
                            satisfied=core_complete,
                            reason_code=(
                                "CORE_AND_REVIEW_COMPLETE"
                                if core_complete
                                else "CORE_OR_REVIEW_INCOMPLETE"
                            ),
                        ),
                        PrerequisiteResult(
                            name="paired_pre_release_target_declaration",
                            availability=history_availability,
                            satisfied=historical_target,
                            reason_code=(
                                "PAIRED_PRE_RELEASE_TARGET_DECLARATION"
                                if historical_target
                                else "PRE_RELEASE_TARGET_DECLARATION_UNAVAILABLE"
                            ),
                        ),
                    )
                    sufficient = all(item.satisfied for item in prerequisites)
                    finding = (
                        FindingState.NO_QUALIFYING_EVIDENCE_FOUND
                        if sufficient
                        else FindingState.UNKNOWN
                    )
                    reason = (
                        "NO_ACCEPTED_QUALIFYING_EVIDENCE_WITHIN_BOUNDED_METHOD"
                        if sufficient
                        else "REQUIRED_EVIDENCE_PREREQUISITE_UNMET"
                    )
                elif question in {"adoption_readiness", "observed_adoption"}:
                    prerequisites = (
                        PrerequisiteResult(
                            name="qualified_resolved_or_installed_version",
                            availability=SourceAvailability.NOT_PLANNED,
                            satisfied=False,
                            reason_code="RESOLVED_VERSION_SOURCE_NOT_PLANNED",
                        ),
                    )
                    sufficient = False
                    finding = FindingState.UNKNOWN
                    reason = "RESOLVED_VERSION_EVIDENCE_UNAVAILABLE"
                else:
                    prerequisites = (
                        PrerequisiteResult(
                            name="eligible_downstream_recovery_source_and_window",
                            availability=SourceAvailability.NOT_PLANNED,
                            satisfied=False,
                            reason_code="RECOVERY_SOURCE_NOT_PLANNED",
                        ),
                    )
                    sufficient = False
                    finding = FindingState.UNKNOWN
                    reason = "RECOVERY_ELIGIBILITY_UNAVAILABLE"
                assessments.append(QuestionAssessment(
                    case_id=case_id,
                    repository=name,
                    question=question,
                    prerequisites=prerequisites,
                    sufficiency=(
                        SufficiencyState.SUFFICIENT
                        if sufficient
                        else SufficiencyState.INSUFFICIENT
                    ),
                    finding=finding,
                    reason_code=reason,
                ))
    return tuple(assessments)


def _metric(
    metric_id: str,
    name: str,
    numerator: int | None,
    denominator: int | None,
    interpretation: str,
) -> ExperimentalMetric:
    available = denominator is not None and denominator > 0 and numerator is not None
    return ExperimentalMetric(
        metric_id=metric_id,
        name=name,
        numerator=numerator,
        denominator=denominator,
        value=(numerator / denominator if available else None),
        status="EXPERIMENTAL" if available else "UNAVAILABLE_ZERO_DENOMINATOR",
        interpretation=interpretation,
    )


def _member_changes(
    reports: dict[str, dict[str, Any]],
    history: tuple[HistoryRecord, ...],
    assessments: tuple[QuestionAssessment, ...],
) -> tuple[MemberChange, ...]:
    changes: list[MemberChange] = []
    for case_id, report in reports.items():
        for repository in report["repositories"]:
            name = repository["repository"]
            records = tuple(
                item for item in history
                if item.case_id == case_id and item.repository == name
            )
            member_assessments = tuple(
                item for item in assessments
                if item.case_id == case_id and item.repository == name
            )
            baseline_history = Counter(item.baseline_state.value for item in records)
            treatment_history = Counter(item.treatment_state.value for item in records)
            history_changes = tuple(
                f"{item.path}: {item.baseline_state.value} -> {item.treatment_state.value}"
                for item in records
                if item.baseline_state is not item.treatment_state
            )
            baseline_finding_counts: Counter[str] = Counter()
            baseline_by_question: dict[str, str] = {}
            for question, finding in repository["stage_findings"].items():
                state = (
                    "UNKNOWN" if finding["state"] == "unknown_insufficient_data"
                    else "NO_QUALIFYING_EVIDENCE_FOUND"
                    if finding["state"] == "no_qualifying_evidence_found"
                    else "YES"
                )
                baseline_by_question[question] = state
                baseline_finding_counts[state] += 1
            treatment_finding_counts = Counter(item.finding.value for item in member_assessments)
            sufficiency_changes = tuple(
                f"{item.question}: INSUFFICIENT -> SUFFICIENT"
                for item in member_assessments
                if item.sufficiency is SufficiencyState.SUFFICIENT
                and not repository["stage_sufficiency"][item.question]
            )
            finding_changes = tuple(
                f"{item.question}: {baseline_by_question[item.question]} -> {item.finding.value}"
                for item in member_assessments
                if baseline_by_question[item.question] != item.finding.value
            )
            new_paths = tuple(
                item.path for item in records
                if item.baseline_state is not HistoryState.PAIRED
                and item.treatment_state is HistoryState.PAIRED
            )
            changes.append(MemberChange(
                case_id=case_id,
                repository=name,
                baseline_history={
                    state.value: baseline_history[state.value] for state in HistoryState
                },
                treatment_history={
                    state.value: treatment_history[state.value] for state in HistoryState
                },
                baseline_sufficient=sum(repository["stage_sufficiency"].values()),
                treatment_sufficient=sum(
                    item.sufficiency is SufficiencyState.SUFFICIENT
                    for item in member_assessments
                ),
                baseline_findings={
                    state.value: baseline_finding_counts[state.value] for state in FindingState
                },
                treatment_findings={
                    state.value: treatment_finding_counts[state.value] for state in FindingState
                },
                new_evidence_paths=new_paths,
                source_types=("github_repository_commits", "github_exact_ref_file"),
                history_changes=history_changes,
                sufficiency_changes=sufficiency_changes,
                finding_changes=finding_changes,
                no_change_reason=(
                    None
                    if history_changes or sufficiency_changes or finding_changes
                    else "Treatment evidence did not change a bounded history or finding state."
                ),
                stop_reasons=tuple(sorted({item.stop_reason for item in records}, key=str)),
                provenance_attempt_ids=tuple(sorted({
                    attempt_id
                    for item in records
                    for attempt_id in item.provenance_attempt_ids
                })),
            ))
    return tuple(changes)


def evaluate_phase7(manifest_path: Path, *, root: Path = ROOT) -> Phase7Evaluation:
    root = root.resolve()
    manifest = Phase7RunManifest.model_validate_json(
        manifest_path.read_text(encoding="utf-8")
    )
    for attempt in manifest.attempts:
        _load_raw_attempt(root, attempt, manifest.run_id)
    current_digests = baseline_digests(root)
    if current_digests != manifest.baseline_digests:
        raise ValueError("Phase 7 baseline digest drift")
    reports = _baseline_reports(root)
    file_attempts = [item for item in manifest.attempts if item.path is not None]
    lookup = {
        (item.case_id, item.repository, item.path, item.anchor_role): item
        for item in file_attempts
    }
    history: list[HistoryRecord] = []
    for case_id, report in reports.items():
        for repository in report["repositories"]:
            name = repository["repository"]
            baseline_paths = {item["path"]: item for item in repository["historical_paths"]}
            if set(baseline_paths) != set(ALLOWED_PATHS):
                raise ValueError("Baseline historical paths left the frozen population")
            for path in ALLOWED_PATHS:
                before_attempt = lookup[(case_id, name, path, AnchorRole.PRE_RELEASE)]
                after_attempt = lookup[(case_id, name, path, AnchorRole.OBSERVATION_END)]
                before = _state_from_attempt(root, before_attempt)
                after = _state_from_attempt(root, after_attempt)
                treatment_state, reason, stop = _history_state(before, after)
                history.append(HistoryRecord(
                    case_id=case_id,
                    repository=name,
                    path=path,
                    baseline_state=_baseline_state(baseline_paths[path]),
                    treatment_state=treatment_state,
                    before=before,
                    after=after,
                    unresolved_reason=reason,
                    stop_reason=stop,
                    provenance_attempt_ids=(before_attempt.task_id, after_attempt.task_id),
                ))
    history_records = tuple(history)
    assessments = _question_assessments(reports, history_records)
    candidates = CandidateSummary(candidates=2, accepted=0, rejected=2, distinct_artifacts=1)
    baseline = _result_summary(
        reports, history_records, assessments, candidates, baseline=True
    )
    treatment = _result_summary(
        reports, history_records, assessments, candidates, baseline=False
    )
    attempt_distribution = Counter(item.availability.value for item in manifest.attempts)
    prerequisite_distribution = Counter(
        prerequisite.availability.value
        for item in assessments
        for prerequisite in item.prerequisites
    )
    unresolved_history = Counter(
        item.unresolved_reason or "RESOLVED"
        for item in history_records
        if item.treatment_state is HistoryState.UNRESOLVED
    )
    unresolved_questions = Counter(
        item.reason_code for item in assessments if item.finding is FindingState.UNKNOWN
    )
    provenance_complete = all(
        (root / item.raw_path).is_file()
        and file_sha256(root / item.raw_path) == item.raw_sha256
        and bool(item.reason)
        for item in manifest.attempts
    )
    positive_denominator = treatment.findings[FindingState.YES.value]
    changed_history = sum(
        item.baseline_state is not item.treatment_state for item in history_records
    )
    metrics = (
        _metric("P7-M01", "Prerequisite coverage", treatment.sufficient, 40,
                "Member-question assessments with every required prerequisite."),
        _metric("P7-M02", "Paired historical-context availability",
                treatment.history_states[HistoryState.PAIRED.value], 16,
                "Exact-ref before/after path states, not adoption."),
        _metric("P7-M03", "Lifecycle-question sufficiency", treatment.sufficient, 40,
                "Questions eligible for a bounded answer."),
        _metric("P7-M04", "Bounded decision availability",
                treatment.findings[FindingState.YES.value]
                + treatment.findings[FindingState.NO_QUALIFYING_EVIDENCE_FOUND.value],
                40, "Supported positive or bounded NO findings."),
        _metric("P7-M05", "Support-link completeness",
                treatment.support_links if positive_denominator else None,
                positive_denominator, "Positive findings with intact support paths."),
        _metric("P7-M06", "UNKNOWN reason coverage",
                sum(unresolved_questions.values()),
                treatment.findings[FindingState.UNKNOWN.value],
                "UNKNOWN findings with controlled reasons."),
        _metric("P7-M07", "Historical method delta", changed_history, 16,
                "Comparable member-path records whose state changed."),
        _metric("P7-M08", "Provenance completeness",
                len(manifest.attempts) if provenance_complete else None,
                len(manifest.attempts), "Treatment attempts with intact provenance."),
    )
    return Phase7Evaluation(
        run_id=manifest.run_id,
        treatment_method=manifest.treatment_method,
        reconstruction_version=manifest.reconstruction_version,
        prerequisite_version=manifest.prerequisite_version,
        baseline_digests=manifest.baseline_digests,
        baseline=baseline,
        treatment=treatment,
        history_delta={
            state.value: treatment.history_states[state.value]
            - baseline.history_states[state.value]
            for state in HistoryState
        },
        finding_delta={
            state.value: treatment.findings[state.value] - baseline.findings[state.value]
            for state in FindingState
        },
        unknown_delta=(
            treatment.findings[FindingState.UNKNOWN.value]
            - baseline.findings[FindingState.UNKNOWN.value]
        ),
        bounded_no_delta=(
            treatment.findings[FindingState.NO_QUALIFYING_EVIDENCE_FOUND.value]
            - baseline.findings[FindingState.NO_QUALIFYING_EVIDENCE_FOUND.value]
        ),
        positive_delta=(
            treatment.findings[FindingState.YES.value]
            - baseline.findings[FindingState.YES.value]
        ),
        support_link_delta=treatment.support_links - baseline.support_links,
        candidate_invariant=treatment.candidates == baseline.candidates,
        source_availability_attempts={
            state.value: attempt_distribution[state.value] for state in SourceAvailability
        },
        source_availability_prerequisites={
            state.value: prerequisite_distribution[state.value]
            for state in SourceAvailability
        },
        unresolved_history_reasons=dict(sorted(unresolved_history.items())),
        unresolved_question_reasons=dict(sorted(unresolved_questions.items())),
        metrics=metrics,
        history_records=history_records,
        assessments=assessments,
        member_changes=_member_changes(reports, history_records, assessments),
        provenance_complete=provenance_complete,
        baseline_unchanged=current_digests == manifest.baseline_digests,
    )


def write_evaluation(
    evaluation: Phase7Evaluation,
    *,
    root: Path = ROOT,
    exclusive: bool = True,
) -> Path:
    directory = root / "data/processed/phase-7" / evaluation.run_id
    directory.mkdir(parents=True, exist_ok=not exclusive)
    path = directory / "evaluation.json"
    mode = "x" if exclusive else "w"
    with path.open(mode, encoding="utf-8") as handle:
        handle.write(evaluation.model_dump_json(indent=2) + "\n")
    return path


def verify_replay(manifest_path: Path, expected_path: Path, *, root: Path = ROOT) -> None:
    evaluation = evaluate_phase7(manifest_path, root=root)
    expected = Phase7Evaluation.model_validate_json(
        expected_path.read_text(encoding="utf-8")
    )
    if evaluation != expected:
        raise ValueError("Phase 7 offline replay does not match expected evaluation")
