"""Repository-bounded lifecycle reconstruction and defensible cohort metrics."""

from __future__ import annotations

from collections import Counter
from datetime import date
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, computed_field

from pulse.models.case import CaseDefinition
from pulse.models.evidence import Confidence, EvidenceEvent, LifecycleStage
from pulse.models.review import EvidenceStatus, ReviewableEvidence


class EvidenceState(StrEnum):
    YES = "yes"
    NO_QUALIFYING_EVIDENCE = "no_qualifying_evidence_found"
    UNKNOWN = "unknown_insufficient_data"


class StageFinding(BaseModel):
    model_config = ConfigDict(frozen=True)

    state: EvidenceState
    event_ids: tuple[str, ...] = ()
    explanation: str


class RepositoryForensics(BaseModel):
    model_config = ConfigDict(frozen=True)

    repository: str
    observed_adoption: StageFinding
    migration_friction: StageFinding
    remediation: StageFinding
    recovery_signal: StageFinding
    overall_confidence: Confidence | None
    missing_evidence: tuple[str, ...]


class CohortMetric(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    numerator: int = Field(ge=0)
    denominator: int = Field(ge=0)
    observation_window_start: date
    observation_window_end: date
    qualification_rule: str

    @computed_field
    @property
    def value(self) -> float | None:
        return self.numerator / self.denominator if self.denominator else None


class EvidenceCompleteness(BaseModel):
    model_config = ConfigDict(frozen=True)

    repositories_collected: int
    cohort_size: int
    lifecycle_stage_counts: dict[str, int]
    confidence_distribution: dict[str, int]


class ReleaseForensics(BaseModel):
    model_config = ConfigDict(frozen=True)

    case_id: str
    target_package: str
    target_version: str
    cohort_id: str
    cohort_selection_method: str
    cohort_selection_rationale: str
    observation_window_start: date
    observation_window_end: date
    accepted_events: tuple[EvidenceEvent, ...]
    repositories: tuple[RepositoryForensics, ...]
    metrics: tuple[CohortMetric, ...]
    completeness: EvidenceCompleteness
    missing_evidence: tuple[str, ...]
    limitations: tuple[str, ...]


def accepted_to_events(candidates: tuple[ReviewableEvidence, ...]) -> tuple[EvidenceEvent, ...]:
    unique: dict[str, EvidenceEvent] = {}
    for candidate in candidates:
        if candidate.status is not EvidenceStatus.ACCEPTED:
            continue
        unique[candidate.candidate_id] = EvidenceEvent(
            event_id=candidate.candidate_id,
            case_id=candidate.case_id,
            repository=candidate.repository,
            occurred_at=candidate.occurred_at,
            lifecycle_stage=candidate.lifecycle_stage,
            event_type=candidate.event_type,
            title=candidate.title,
            target_package=candidate.target_package,
            target_release=candidate.target_release,
            evidence=candidate.evidence,
            confidence=candidate.confidence,
            evidence_reason=(
                f"Rule {candidate.classification_rule}: {candidate.classification_reason} "
                f"Review: {candidate.reviewer_note}"
            ),
        )
    return tuple(sorted(unique.values(), key=lambda item: (item.occurred_at, item.event_id or "")))


def build_forensics(
    definition: CaseDefinition,
    candidates: tuple[ReviewableEvidence, ...],
    *,
    repositories_with_sufficient_collection: set[str],
    recovery_eligible_repositories: set[str] | None = None,
) -> ReleaseForensics:
    events = accepted_to_events(candidates)
    by_repository: dict[str, list[EvidenceEvent]] = {}
    for event in events:
        slug = _repository_slug(str(event.repository))
        by_repository.setdefault(slug.casefold(), []).append(event)

    summaries = []
    for member in definition.cohort.repositories:
        key = member.repository.casefold()
        repository_events = by_repository.get(key, [])
        sufficient = key in {item.casefold() for item in repositories_with_sufficient_collection}
        summaries.append(_repository_summary(member.repository, repository_events, sufficient))

    metrics = _metrics(definition, summaries, recovery_eligible_repositories)
    confidence_counts = Counter(event.confidence.value for event in events)
    stage_counts = Counter(event.lifecycle_stage.value for event in events)
    missing = tuple(
        f"{summary.repository}: {item}"
        for summary in summaries
        for item in summary.missing_evidence
    )
    return ReleaseForensics(
        case_id=definition.case.case_id,
        target_package=definition.case.target_package,
        target_version=definition.case.target_version,
        cohort_id=definition.cohort.cohort_id,
        cohort_selection_method=definition.cohort.selection_method.value,
        cohort_selection_rationale=definition.cohort.selection_rationale,
        observation_window_start=definition.case.observation_window_start,
        observation_window_end=definition.case.observation_window_end,
        accepted_events=events,
        repositories=tuple(summaries),
        metrics=metrics,
        completeness=EvidenceCompleteness(
            repositories_collected=sum(
                member.repository.casefold()
                in {item.casefold() for item in repositories_with_sufficient_collection}
                for member in definition.cohort.repositories
            ),
            cohort_size=len(definition.cohort.repositories),
            lifecycle_stage_counts=dict(stage_counts),
            confidence_distribution=dict(confidence_counts),
        ),
        missing_evidence=missing,
        limitations=(
            "Metrics describe only the declared cohort and observation window.",
            "No qualifying evidence found does not prove that no event occurred.",
            "Accepted evidence supports association unless a source demonstrates causality.",
        ),
    )


def _repository_summary(
    repository: str, events: list[EvidenceEvent], sufficient: bool
) -> RepositoryForensics:
    def finding(stage: LifecycleStage) -> StageFinding:
        selected = [item for item in events if item.lifecycle_stage is stage]
        if selected:
            return StageFinding(
                state=EvidenceState.YES,
                event_ids=tuple(item.event_id or "legacy-event" for item in selected),
                explanation=f"{len(selected)} accepted {stage.value} event(s).",
            )
        state = (
            EvidenceState.NO_QUALIFYING_EVIDENCE if sufficient else EvidenceState.UNKNOWN
        )
        explanation = (
            "Collection was sufficient, but no qualifying accepted event was found."
            if sufficient
            else "Collection was incomplete or unavailable, so the stage is unknown."
        )
        return StageFinding(state=state, explanation=explanation)

    confidence = None
    if events:
        confidence = min((event.confidence for event in events), key=_confidence_rank)
    missing = []
    if not sufficient:
        missing.append("sufficient public artifacts were not collected")
    for stage in (
        LifecycleStage.OBSERVED_ADOPTION,
        LifecycleStage.MIGRATION_FRICTION,
        LifecycleStage.REMEDIATION,
        LifecycleStage.RECOVERY_SIGNAL,
    ):
        if not any(item.lifecycle_stage is stage for item in events):
            missing.append(f"no accepted {stage.value} evidence")
    return RepositoryForensics(
        repository=repository,
        observed_adoption=finding(LifecycleStage.OBSERVED_ADOPTION),
        migration_friction=finding(LifecycleStage.MIGRATION_FRICTION),
        remediation=finding(LifecycleStage.REMEDIATION),
        recovery_signal=finding(LifecycleStage.RECOVERY_SIGNAL),
        overall_confidence=confidence,
        missing_evidence=tuple(missing),
    )


def _metrics(
    definition: CaseDefinition,
    summaries: list[RepositoryForensics],
    recovery_eligible: set[str] | None,
) -> tuple[CohortMetric, ...]:
    window = {
        "observation_window_start": definition.case.observation_window_start,
        "observation_window_end": definition.case.observation_window_end,
    }
    adopted = [item for item in summaries if item.observed_adoption.state is EvidenceState.YES]
    friction = [item for item in summaries if item.migration_friction.state is EvidenceState.YES]
    metrics = [
        CohortMetric(
            name="observed_adoption_coverage",
            numerator=len(adopted),
            denominator=len(summaries),
            qualification_rule="Accepted observed-adoption event / declared cohort repositories.",
            **window,
        ),
        CohortMetric(
            name="friction_incidence",
            numerator=sum(item.migration_friction.state is EvidenceState.YES for item in adopted),
            denominator=len(adopted),
            qualification_rule="Accepted friction event / repositories with observed adoption.",
            **window,
        ),
        CohortMetric(
            name="remediation_coverage",
            numerator=sum(item.remediation.state is EvidenceState.YES for item in friction),
            denominator=len(friction),
            qualification_rule="Accepted remediation event / repositories with accepted friction.",
            **window,
        ),
    ]
    if recovery_eligible is not None:
        eligible = {item.casefold() for item in recovery_eligible}
        metrics.append(
            CohortMetric(
                name="bounded_recovery_coverage",
                numerator=sum(
                    item.repository.casefold() in eligible
                    and item.recovery_signal.state is EvidenceState.YES
                    for item in summaries
                ),
                denominator=len(eligible),
                qualification_rule="Accepted recovery event / explicitly eligible repositories.",
                **window,
            )
        )
    return tuple(metrics)


def _repository_slug(url: str) -> str:
    return url.removeprefix("https://github.com/").rstrip("/")


def _confidence_rank(confidence: Confidence) -> int:
    return {Confidence.LOW: 0, Confidence.MEDIUM: 1, Confidence.HIGH: 2}[confidence]
