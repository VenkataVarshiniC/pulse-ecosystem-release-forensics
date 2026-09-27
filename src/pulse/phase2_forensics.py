"""Deterministic Phase 2 forensics from frozen, verified collection artifacts."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import date, datetime
from enum import StrEnum
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from pulse.analysis.forensics import EvidenceState, StageFinding, accepted_to_events
from pulse.collection.journal import (
    AttemptRecord,
    _verified_optional_not_found,
    _verified_snapshot,
    case_fingerprint,
)
from pulse.collection.manifest import LiveCollectionManifest, TaskOutcomeStatus
from pulse.collection.planner import CollectionTask, TaskKind, plan_collection
from pulse.detector_evaluation import ReviewedCandidate, historical_context, load_verified_baseline
from pulse.history.models import HistoricalRun
from pulse.models.case import CaseDefinition, SourceSystem
from pulse.models.evidence import Confidence, EvidenceEvent, LifecycleStage
from pulse.models.review import EvidenceStatus


class Availability(StrEnum):
    COMPLETE = "complete"
    PARTIAL = "partial"
    UNAVAILABLE = "unavailable"
    NOT_COLLECTED = "not_collected"


class SourceCoverage(BaseModel):
    model_config = ConfigDict(frozen=True)

    state: Availability
    planned: int = Field(ge=0)
    succeeded: int = Field(ge=0)
    optional_not_found: int = Field(ge=0)
    reason: str


class RepositoryResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    repository: str
    historical_dependency_context: str
    historical_paths: tuple[dict, ...]
    collection_coverage: dict[str, SourceCoverage]
    stage_sufficiency: dict[str, bool]
    stage_findings: dict[str, StageFinding]
    accepted_event_ids: tuple[str, ...]
    emitted_candidate_count: int
    rejected_candidate_count: int
    needs_review_count: int
    unknowns: tuple[str, ...]
    missing_sources: tuple[str, ...]
    confidence: Confidence | None


class BoundedMetric(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    numerator: int = Field(ge=0)
    denominator: int = Field(gt=0)
    meaning: str

    @property
    def value(self) -> float:
        return self.numerator / self.denominator


class RejectedCandidate(BaseModel):
    model_config = ConfigDict(frozen=True)

    candidate_id: str
    repository: str
    rule: str
    reason_code: str
    analyst_note: str
    source_url: str


class Phase2Report(BaseModel):
    model_config = ConfigDict(frozen=True)

    case_id: str
    target_package: str
    target_version: str
    release_timestamp: datetime
    cohort_id: str
    selection_method: str
    selection_rationale: str
    observation_window_start: date
    observation_window_end: date
    collection_run_id: str
    collection_operational_status: str
    collection_task_counts: dict[str, int]
    upstream_collection: dict[str, SourceCoverage]
    history_run_id: str
    frozen_cohort: tuple[str, ...]
    repositories: tuple[RepositoryResult, ...]
    emitted_candidate_count: int
    accepted_candidate_count: int
    rejected_candidate_count: int
    needs_review_count: int
    rejected_candidates: tuple[RejectedCandidate, ...]
    accepted_events: tuple[EvidenceEvent, ...]
    metrics: tuple[BoundedMetric, ...]
    unavailable_metrics: tuple[str, ...]
    missing_sources: tuple[str, ...]
    limitations: tuple[str, ...]


def _read_collection(
    definition: CaseDefinition,
    path: Path,
) -> tuple[LiveCollectionManifest, dict[str, AttemptRecord]]:
    manifest = LiveCollectionManifest.model_validate_json(path.read_text(encoding="utf-8"))
    expected = plan_collection(definition)
    fingerprint = case_fingerprint(definition)
    run = json.loads((path.parent / "run.json").read_text(encoding="utf-8"))
    if (
        manifest.case_id != definition.case.case_id
        or manifest.observation_window_start != str(definition.case.observation_window_start)
        or manifest.observation_window_end != str(definition.case.observation_window_end)
        or manifest.run_id != run.get("run_id")
        or run.get("case_fingerprint") != fingerprint
        or run.get("definition") != definition.model_dump(mode="json")
        or run.get("plan") != expected.model_dump(mode="json")
        or manifest.planned_tasks != expected.tasks
    ):
        raise ValueError("collection case, cohort, window, or fingerprint mismatch")
    attempts = tuple(
        AttemptRecord.model_validate_json(item.read_text(encoding="utf-8"))
        for item in sorted(path.parent.glob("*.attempt.json"))
    )
    records: dict[str, AttemptRecord] = {}
    outcomes = {item.task_id: item for item in manifest.outcomes}
    for record in attempts:
        if (
            record.run_id != manifest.run_id
            or record.case_fingerprint != fingerprint
            or record.task not in expected.tasks
            or record.outcome != outcomes.get(record.task.task_id)
            or record.task.task_id in records
            or record.observation_window_start != manifest.observation_window_start
            or record.observation_window_end != manifest.observation_window_end
        ):
            raise ValueError("collection attempt does not match the frozen run")
        if record.outcome.status is TaskOutcomeStatus.SUCCEEDED:
            if not _verified_snapshot(record, definition):
                raise ValueError("successful collection snapshot failed verification")
        elif (
            record.outcome.status is TaskOutcomeStatus.NOT_FOUND
            and record.task.kind is TaskKind.GITHUB_FILE
            and not _verified_optional_not_found(record)
        ):
            raise ValueError("optional 404 probe failed verification")
        records[record.task.task_id] = record
    if set(records) != set(outcomes):
        raise ValueError("collection outcomes lack matching attempt records")
    return manifest, records


def _read_history(definition: CaseDefinition, path: Path) -> HistoricalRun:
    history = HistoricalRun.model_validate_json(path.read_text(encoding="utf-8"))
    paths = sorted(
        {
            name
            for rule in definition.case.collection_rules
            if rule.source in {SourceSystem.GITHUB, SourceSystem.REPOSITORY_FILE}
            for name in rule.file_paths
        }
    )
    expected = {
        (member.repository.casefold(), name)
        for member in definition.cohort.repositories
        for name in paths
    }
    observed = [
        (item.pair.repository.casefold(), item.pair.manifest_path) for item in history.results
    ]
    if (
        history.case_id != definition.case.case_id
        or set(observed) != expected
        or len(observed) != len(expected)
    ):
        raise ValueError("history case or frozen cohort mismatch")
    for item in history.results:
        pair = item.pair
        if (
            pair.case_id != history.case_id
            or pair.observation_window_start != definition.case.observation_window_start
            or pair.observation_window_end != definition.case.observation_window_end
            or pair.release_timestamp != definition.case.release_timestamp
        ):
            raise ValueError("historical observation window or release mismatch")
    return history


def _read_reviews(
    definition: CaseDefinition,
    ledger_path: Path,
    baseline_path: Path,
    baseline_manifest: Path,
    collection_run_id: str,
    history_run_id: str,
) -> tuple[ReviewedCandidate, ...]:
    metadata = json.loads(baseline_manifest.read_text(encoding="utf-8"))
    if (
        metadata.get("case_id") != definition.case.case_id
        or metadata.get("collection_run_id") != collection_run_id
        or metadata.get("history_run_id") != history_run_id
    ):
        raise ValueError("candidate baseline belongs to a different case or run")
    baseline = load_verified_baseline(baseline_path, baseline_manifest)
    reviewed = tuple(
        ReviewedCandidate.model_validate_json(line)
        for line in ledger_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
        if json.loads(line)["candidate"]["case_id"] == definition.case.case_id
    )
    all_rows = [
        json.loads(line)
        for line in ledger_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    ids = [row.candidate.candidate_id for row in reviewed]
    if len(ids) != len(set(ids)) or set(ids) != {item.candidate_id for item in baseline}:
        raise ValueError("review ledger does not cover each baseline candidate exactly once")
    if any(
        row["candidate"]["case_id"] not in {"pytest-8.0.0", "urllib3-2.0.0"} for row in all_rows
    ):
        raise ValueError("review ledger contains an unknown case")
    members = {member.repository.casefold() for member in definition.cohort.repositories}
    by_id = {item.candidate_id: item for item in baseline}
    for item in reviewed:
        candidate = item.candidate
        original = by_id[candidate.candidate_id]
        frozen_fields = original.model_dump(exclude={"status", "reviewer_note", "reviewed_at"})
        if (
            candidate.model_dump(exclude={"status", "reviewer_note", "reviewed_at"})
            != frozen_fields
            or candidate.status is EvidenceStatus.CANDIDATE
            or str(candidate.repository).removeprefix("https://github.com/").rstrip("/").casefold()
            not in members
            or candidate.target_package != definition.case.target_package
            or candidate.target_release != definition.case.target_version
            or not definition.case.observation_window_start
            <= candidate.occurred_at.date()
            <= definition.case.observation_window_end
        ):
            raise ValueError("reviewed candidate differs from frozen case evidence")
    return reviewed


def _coverage(tasks: list[CollectionTask], attempts: dict[str, AttemptRecord]) -> SourceCoverage:
    if not tasks:
        return SourceCoverage(
            state=Availability.NOT_COLLECTED,
            planned=0,
            succeeded=0,
            optional_not_found=0,
            reason="No task was planned for this source.",
        )
    statuses = [attempts[item.task_id].outcome.status for item in tasks]
    succeeded = statuses.count(TaskOutcomeStatus.SUCCEEDED)
    optional_404 = sum(
        task.kind is TaskKind.GITHUB_FILE and status is TaskOutcomeStatus.NOT_FOUND
        for task, status in zip(tasks, statuses, strict=True)
    )
    complete = succeeded + optional_404 == len(tasks)
    return SourceCoverage(
        state=(
            Availability.COMPLETE
            if complete
            else Availability.PARTIAL
            if succeeded + optional_404
            else Availability.UNAVAILABLE
        ),
        planned=len(tasks),
        succeeded=succeeded,
        optional_not_found=optional_404,
        reason=(
            "All planned tasks succeeded or optional current-file probes returned verified 404s."
            if complete
            else "One or more planned tasks failed or ended without complete collection."
        ),
    )


def _finding(
    stage: LifecycleStage,
    events: tuple[EvidenceEvent, ...],
    sufficient: bool,
) -> StageFinding:
    selected = tuple(item for item in events if item.lifecycle_stage is stage)
    if selected:
        return StageFinding(
            state=EvidenceState.YES,
            event_ids=tuple(item.event_id or "legacy-event" for item in selected),
            explanation=f"{len(selected)} accepted qualifying event(s).",
        )
    if sufficient:
        return StageFinding(
            state=EvidenceState.NO_QUALIFYING_EVIDENCE,
            explanation=(
                "Required sources were completely collected and emitted candidates "
                "were reviewed; no accepted qualifying evidence was found. "
                "This does not prove the event did not happen."
            ),
        )
    return StageFinding(
        state=EvidenceState.UNKNOWN,
        explanation=(
            "Required evidence or historical context is incomplete; "
            "a negative finding is unsupported."
        ),
    )


def _metric(name: str, numerator: int, denominator: int, meaning: str) -> BoundedMetric:
    return BoundedMetric(name=name, numerator=numerator, denominator=denominator, meaning=meaning)


def _release_boundary_dependency_supported(paths: list[dict]) -> bool:
    """Require a parsed pre-release declaration in a complete path pair for negative findings."""
    return any(
        path["pair_status"] == "paired"
        and path["before_file_status"] == "parsed"
        and bool(path["before_target"])
        for path in paths
    )


def build_phase2_report(
    definition: CaseDefinition,
    collection_path: Path,
    history_path: Path,
    baseline_path: Path,
    baseline_manifest: Path,
    review_ledger: Path,
) -> Phase2Report:
    collection, attempts = _read_collection(definition, collection_path)
    history = _read_history(definition, history_path)
    reviewed = _read_reviews(
        definition,
        review_ledger,
        baseline_path,
        baseline_manifest,
        collection.run_id,
        history.run_id,
    )
    context = historical_context(definition, history)
    upstream_tasks = [
        task
        for task in collection.planned_tasks
        if task.repository == definition.case.upstream_repository
    ]
    upstream_collection = {
        "pypi_version": _coverage(
            [task for task in collection.planned_tasks if task.kind is TaskKind.PYPI_VERSION],
            attempts,
        ),
        "upstream_repository": _coverage(
            [task for task in upstream_tasks if task.kind is TaskKind.GITHUB_REPOSITORY],
            attempts,
        ),
        "upstream_releases": _coverage(
            [task for task in upstream_tasks if task.kind is TaskKind.GITHUB_RELEASES],
            attempts,
        ),
    }
    accepted = tuple(
        item.candidate for item in reviewed if item.candidate.status is EvidenceStatus.ACCEPTED
    )
    events = accepted_to_events(accepted)
    results = []
    for member in definition.cohort.repositories:
        repo = member.repository
        tasks = [task for task in collection.planned_tasks if task.repository == repo]
        categories = {
            "repository_metadata": _coverage(
                [task for task in tasks if task.kind is TaskKind.GITHUB_REPOSITORY], attempts
            ),
            "issues": _coverage(
                [task for task in tasks if task.kind is TaskKind.GITHUB_ISSUES], attempts
            ),
            "pull_requests": _coverage(
                [task for task in tasks if task.kind is TaskKind.GITHUB_PULL_REQUESTS], attempts
            ),
            "commits": _coverage(
                [task for task in tasks if task.kind is TaskKind.GITHUB_COMMITS], attempts
            ),
            "current_manifest_probes": _coverage(
                [task for task in tasks if task.kind is TaskKind.GITHUB_FILE], attempts
            ),
        }
        paths = context[repo]["paths"]
        historical_status = context[repo]["status"]
        history_complete = historical_status == "historically_supported" and all(
            path["pair_status"] == "paired"
            and path["before_file_status"] == "parsed"
            and path["after_file_status"] == "parsed"
            for path in paths
        )
        # A partial path-scoped history cannot support a negative historical claim.
        categories["historical_dependency"] = SourceCoverage(
            state=Availability.COMPLETE if history_complete else Availability.PARTIAL,
            planned=len(paths),
            succeeded=sum(path["pair_status"] == "paired" for path in paths),
            optional_not_found=0,
            reason=(
                "All configured paths have parsed exact-ref pairs."
                if history_complete
                else "Historical target-version eligibility is unresolved in one or more paths."
            ),
        )
        repo_reviews = tuple(
            item
            for item in reviewed
            if str(item.candidate.repository).rstrip("/").casefold()
            == f"https://github.com/{repo}".casefold()
        )
        unresolved = sum(
            item.candidate.status is EvidenceStatus.NEEDS_REVIEW for item in repo_reviews
        )
        categories["reviewed_candidates"] = SourceCoverage(
            state=Availability.PARTIAL if unresolved else Availability.COMPLETE,
            planned=len(repo_reviews),
            succeeded=len(repo_reviews) - unresolved,
            optional_not_found=0,
            reason=(
                "Some emitted candidates remain unresolved."
                if unresolved
                else "Every emitted candidate has an analyst review outcome; zero is valid."
            ),
        )
        categories["downstream_releases"] = _coverage([], attempts)
        repo_events = tuple(
            event
            for event in events
            if str(event.repository).rstrip("/").casefold()
            == f"https://github.com/{repo}".casefold()
        )
        source_complete = all(
            categories[name].state is Availability.COMPLETE
            for name in (
                "repository_metadata",
                "issues",
                "pull_requests",
                "commits",
                "reviewed_candidates",
            )
        )
        stage_sufficiency = {
            LifecycleStage.ADOPTION_READINESS.value: False,
            LifecycleStage.OBSERVED_ADOPTION.value: False,
            LifecycleStage.MIGRATION_FRICTION.value: (
                source_complete and _release_boundary_dependency_supported(paths)
            ),
            LifecycleStage.REMEDIATION.value: (
                source_complete and _release_boundary_dependency_supported(paths)
            ),
            LifecycleStage.RECOVERY_SIGNAL.value: False,
        }
        findings = {
            stage.value: _finding(stage, repo_events, stage_sufficiency[stage.value])
            for stage in (
                LifecycleStage.ADOPTION_READINESS,
                LifecycleStage.OBSERVED_ADOPTION,
                LifecycleStage.MIGRATION_FRICTION,
                LifecycleStage.REMEDIATION,
                LifecycleStage.RECOVERY_SIGNAL,
            )
        }
        missing = tuple(
            name
            for name, category in categories.items()
            if category.state is not Availability.COMPLETE
        )
        unknowns = tuple(
            name for name, finding in findings.items() if finding.state is EvidenceState.UNKNOWN
        )
        confidence = min(
            (item.confidence for item in repo_events),
            key=lambda item: {Confidence.LOW: 0, Confidence.MEDIUM: 1, Confidence.HIGH: 2}[item],
            default=None,
        )
        results.append(
            RepositoryResult(
                repository=repo,
                historical_dependency_context=historical_status,
                historical_paths=tuple(paths),
                collection_coverage=categories,
                stage_sufficiency=stage_sufficiency,
                stage_findings=findings,
                accepted_event_ids=tuple(event.event_id or "legacy-event" for event in repo_events),
                emitted_candidate_count=len(repo_reviews),
                rejected_candidate_count=sum(
                    item.candidate.status is EvidenceStatus.REJECTED for item in repo_reviews
                ),
                needs_review_count=unresolved,
                unknowns=unknowns,
                missing_sources=missing,
                confidence=confidence,
            )
        )
    cohort_size = len(results)
    supported = sum(
        item.historical_dependency_context == "historically_supported" for item in results
    )
    candidate_repos = sum(item.emitted_candidate_count > 0 for item in results)
    collected = sum(
        all(
            item.collection_coverage[name].state is Availability.COMPLETE
            for name in ("repository_metadata", "issues", "pull_requests", "commits")
        )
        for item in results
    )
    friction_eligible = [
        item for item in results if item.stage_sufficiency[LifecycleStage.MIGRATION_FRICTION.value]
    ]
    metrics = (
        _metric(
            "core_collection_coverage",
            collected,
            cohort_size,
            "Repositories with complete metadata, issues, PRs, and commits / frozen cohort.",
        ),
        _metric(
            "historical_dependency_evidence_coverage",
            supported,
            cohort_size,
            "Repositories with an exact-ref target-package declaration / frozen cohort; "
            "not adoption.",
        ),
        _metric(
            "candidate_emission_coverage",
            candidate_repos,
            cohort_size,
            "Repositories with at least one emitted candidate / frozen cohort; "
            "not impact incidence.",
        ),
        _metric(
            "accepted_evidence_coverage",
            sum(bool(item.accepted_event_ids) for item in results),
            cohort_size,
            "Repositories with accepted evidence / frozen cohort; not event incidence.",
        ),
        *(
            ()
            if not friction_eligible
            else (
                _metric(
                    "bounded_friction_finding_coverage",
                    sum(
                        item.stage_findings[LifecycleStage.MIGRATION_FRICTION.value].state
                        is EvidenceState.YES
                        for item in friction_eligible
                    ),
                    len(friction_eligible),
                    "Accepted friction evidence / repositories sufficient for a "
                    "stage-level finding; "
                    "not ecosystem incidence.",
                ),
            )
        ),
    )
    return Phase2Report(
        case_id=definition.case.case_id,
        target_package=definition.case.target_package,
        target_version=definition.case.target_version,
        release_timestamp=definition.case.release_timestamp,
        cohort_id=definition.cohort.cohort_id,
        selection_method=definition.cohort.selection_method.value,
        selection_rationale=definition.cohort.selection_rationale,
        observation_window_start=definition.case.observation_window_start,
        observation_window_end=definition.case.observation_window_end,
        collection_run_id=collection.run_id,
        collection_operational_status=collection.status,
        collection_task_counts={
            "planned": len(collection.planned_tasks),
            **collection.outcome_breakdown,
        },
        upstream_collection=upstream_collection,
        history_run_id=history.run_id,
        frozen_cohort=tuple(item.repository for item in definition.cohort.repositories),
        repositories=tuple(results),
        emitted_candidate_count=len(reviewed),
        accepted_candidate_count=len(accepted),
        rejected_candidate_count=sum(
            item.candidate.status is EvidenceStatus.REJECTED for item in reviewed
        ),
        needs_review_count=sum(
            item.candidate.status is EvidenceStatus.NEEDS_REVIEW for item in reviewed
        ),
        rejected_candidates=tuple(
            RejectedCandidate(
                candidate_id=item.candidate.candidate_id,
                repository=str(item.candidate.repository),
                rule=item.candidate.classification_rule,
                reason_code=item.reason_code.value,
                analyst_note=item.candidate.reviewer_note or "",
                source_url=str(item.candidate.evidence[0].url),
            )
            for item in reviewed
            if item.candidate.status is EvidenceStatus.REJECTED
        ),
        accepted_events=events,
        metrics=metrics,
        unavailable_metrics=(
            "observed_adoption_rate: no target-version installation or runtime denominator",
            "remediation_coverage: no accepted qualifying friction denominator"
            if not any(item.lifecycle_stage is LifecycleStage.MIGRATION_FRICTION for item in events)
            else "remediation_coverage: requires a separately defined eligible set",
            "recovery_rate: downstream releases not collected and recovery-eligible set undefined",
            *(
                ()
                if friction_eligible
                else (
                    "bounded_friction_finding_coverage: no repository has sufficient "
                    "stage evidence",
                )
            ),
        ),
        missing_sources=(
            "Downstream release collection was not planned; text.support_release had no input.",
            "Target-version lockfile selection and runtime/CI resolution were not collected.",
            "Path-scoped historical manifest reconstruction is incomplete for some repositories.",
        ),
        limitations=(
            "Cohort selection used current declarations, not proven historical target-version use.",
            "Path-scoped history can miss earlier declarations and cross-file migrations.",
            "No qualifying evidence found describes this bounded method, "
            "not proof no event occurred.",
            "Zero emitted candidates does not establish absence of release impact "
            "or detector recall.",
            "Lifecycle stages are evidence categories, not a required chronology or causal chain.",
            "These frozen convenience cohorts are not ecosystem-representative.",
        ),
    )


def render_phase2_markdown(report: Phase2Report) -> str:
    lines = [
        f"# Release forensics: {report.target_package} {report.target_version}",
        "",
        f"Case `{report.case_id}`; release boundary {report.release_timestamp.isoformat()}; "
        f"observation window {report.observation_window_start} to {report.observation_window_end}.",
        "",
        "## Frozen cohort and selection",
        "",
        f"`{report.cohort_id}` ({report.selection_method}). {report.selection_rationale}",
        "",
        *(f"- `{name}`" for name in report.frozen_cohort),
        "",
        "## Collection and review",
        "",
        f"Collector run `{report.collection_run_id}`: {report.collection_operational_status}; "
        f"historical run `{report.history_run_id}`.",
        "Collection tasks: "
        + ", ".join(f"{name}={count}" for name, count in report.collection_task_counts.items())
        + ".",
        "Upstream sources: "
        + ", ".join(
            f"{name}=`{coverage.state.value}`"
            for name, coverage in report.upstream_collection.items()
        )
        + ".",
        f"Detector candidates: {report.emitted_candidate_count}; accepted: "
        f"{report.accepted_candidate_count}; rejected: {report.rejected_candidate_count}; "
        f"needs review: {report.needs_review_count}.",
        "Rejected candidate output is detector-quality evidence, not accepted lifecycle evidence.",
        "",
        "## Historical dependency context and repository findings",
        "",
    ]
    for repo in report.repositories:
        lines.extend(
            [
                f"### {repo.repository}",
                "",
                f"Historical context: `{repo.historical_dependency_context}`. "
                "A declaration does not establish target-version installation or adoption.",
                "Historical paths: "
                + "; ".join(
                    f"`{path['path']}` {path['pair_status']} "
                    f"(before {', '.join(path['before_target']) or 'unavailable'}; "
                    f"after {', '.join(path['after_target']) or 'unavailable'}; "
                    f"transition {path['change_status']})"
                    for path in repo.historical_paths
                )
                + ".",
                f"Candidates emitted/rejected/unresolved: {repo.emitted_candidate_count}/"
                f"{repo.rejected_candidate_count}/{repo.needs_review_count}.",
                f"Accepted-event confidence: "
                f"`{repo.confidence.value if repo.confidence else 'unavailable'}`.",
                "Source coverage: "
                + ", ".join(
                    f"{name}=`{source.state.value}` "
                    f"({source.succeeded}/{source.planned} succeeded, "
                    f"{source.optional_not_found} optional 404)"
                    for name, source in repo.collection_coverage.items()
                )
                + ".",
            ]
        )
        for stage, finding in repo.stage_findings.items():
            lines.append(f"- {stage}: **{finding.state.value}** — {finding.explanation}")
        lines.append("Missing sources: " + (", ".join(repo.missing_sources) or "none") + ".")
        lines.append("Unknown stages: " + (", ".join(repo.unknowns) or "none") + ".")
        lines.append("")
    lines.extend(
        [
            "## Accepted evidence timeline",
            "",
            "Events are ordered by evidence timestamp. Stages are categories, not a required "
            "chronological or causal sequence.",
            "",
        ]
    )
    if report.accepted_events:
        for item in report.accepted_events:
            lines.append(
                f"- {item.occurred_at.isoformat()} — {item.lifecycle_stage.value}: "
                f"{item.title} (`{item.event_id}`)."
            )
    else:
        lines.append(
            "No candidate event in this validation case passed the preregistered "
            "analyst review criteria. This is not evidence that no event occurred."
        )
    lines.extend(["", "## Rejected detector candidates", ""])
    if report.rejected_candidates:
        for item in report.rejected_candidates:
            lines.append(
                f"- `{item.candidate_id}` / `{item.rule}` / `{item.reason_code}`: "
                f"{item.analyst_note} [Collected source]({item.source_url})."
            )
    else:
        lines.append("No rejected detector candidates were emitted in this case.")
    lines.extend(["", "## Denominator-aware cohort metrics", ""])
    for item in report.metrics:
        lines.append(
            f"- **{item.name}:** {item.numerator}/{item.denominator} "
            f"({item.value:.1%}). {item.meaning}"
        )
    lines.extend(["", "## Unavailable metrics", ""])
    lines.extend(f"- {item}" for item in report.unavailable_metrics)
    lines.extend(["", "## Missing evidence", ""])
    lines.extend(f"- {item}" for item in report.missing_sources)
    lines.extend(["", "## Limitations", ""])
    lines.extend(f"- {item}" for item in report.limitations)
    lines.append("")
    return "\n".join(lines)


def write_phase2_report(report: Phase2Report, output_root: Path) -> tuple[Path, Path]:
    json_path = output_root / "data/processed/phase-2" / report.case_id / "forensics.json"
    ledger_path = json_path.with_name("accepted-evidence.jsonl")
    markdown_path = output_root / "docs/phase-2/generated" / f"{report.case_id}-forensics.md"
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(report.model_dump_json(indent=2) + "\n", encoding="utf-8")
    ledger_path.write_text(
        "".join(item.model_dump_json() + "\n" for item in report.accepted_events),
        encoding="utf-8",
    )
    markdown_path.write_text(render_phase2_markdown(report), encoding="utf-8")
    return json_path, markdown_path


def digest_reports(paths: tuple[Path, ...]) -> str:
    """Stable digest useful for replay checks without runtime metadata."""
    return hashlib.sha256(b"".join(path.read_bytes() for path in paths)).hexdigest()


def validation_summary(reports: tuple[Phase2Report, ...]) -> dict:
    if len({item.case_id for item in reports}) != len(reports):
        raise ValueError("duplicate case in validation summary")
    cases = {}
    for report in sorted(reports, key=lambda item: item.case_id):
        historical = Counter(item.historical_dependency_context for item in report.repositories)
        stages = {
            stage.value: dict(
                Counter(
                    item.stage_findings[stage.value].state.value for item in report.repositories
                )
            )
            for stage in (
                LifecycleStage.ADOPTION_READINESS,
                LifecycleStage.OBSERVED_ADOPTION,
                LifecycleStage.MIGRATION_FRICTION,
                LifecycleStage.REMEDIATION,
                LifecycleStage.RECOVERY_SIGNAL,
            )
        }
        cases[report.case_id] = {
            "cohort_size": len(report.repositories),
            "collection_operational_status": report.collection_operational_status,
            "historical_context_counts": dict(sorted(historical.items())),
            "candidate_counts": {
                "emitted": report.emitted_candidate_count,
                "accepted": report.accepted_candidate_count,
                "rejected": report.rejected_candidate_count,
                "needs_review": report.needs_review_count,
            },
            "zero_candidate_repositories": [
                item.repository for item in report.repositories if item.emitted_candidate_count == 0
            ],
            "stage_findings": stages,
            "metrics": [item.model_dump(mode="json") for item in report.metrics],
            "unavailable_metrics": report.unavailable_metrics,
            "missing_sources": report.missing_sources,
            "report_paths": {
                "json": f"data/processed/phase-2/{report.case_id}/forensics.json",
                "accepted_ledger": (
                    f"data/processed/phase-2/{report.case_id}/accepted-evidence.jsonl"
                ),
                "markdown": f"docs/phase-2/generated/{report.case_id}-forensics.md",
            },
        }
    return {
        "cases": cases,
        "scope": "Two frozen convenience cohorts; no pooled incidence statistic.",
    }
