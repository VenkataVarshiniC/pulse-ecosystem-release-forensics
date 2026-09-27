"""Independent analyst decisions and bounded emitted-candidate metrics."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import datetime
from enum import StrEnum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator

from pulse.collection.journal import AttemptRecord
from pulse.collection.manifest import LiveCollectionManifest
from pulse.collection.raw import CaptureMethod
from pulse.history.models import FileStateStatus, HistoricalRun, PairStatus
from pulse.models.case import CaseDefinition
from pulse.models.evidence import LifecycleStage
from pulse.models.review import EvidenceStatus, ReviewableEvidence

RULES = (
    "text.version_specific_friction", "text.version_specific_remediation",
    "text.support_release", "dependency.target_excluded", "dependency.target_accepted",
)


class ReviewReason(StrEnum):
    DIRECT_STAGE_EVIDENCE = "direct_stage_evidence"
    TARGET_VERSION_NOT_IMPLICATED = "target_version_not_implicated"
    GENERIC_DEPENDENCY_MENTION = "generic_dependency_mention"
    TEMPORAL_COINCIDENCE_ONLY = "temporal_coincidence_only"
    MENTIONS_OTHER_REMEDIATION = "mentions_other_remediation"
    BOT_OR_DEPENDENCY_UPDATE_NOISE = "bot_or_dependency_update_noise"
    UNRELATED_FAILURE = "unrelated_failure"
    WRONG_LIFECYCLE_STAGE = "wrong_lifecycle_stage"
    DUPLICATE_EVIDENCE = "duplicate_evidence"
    OUTSIDE_WINDOW = "outside_window"
    HISTORICAL_DEPENDENCY_NOT_ESTABLISHED = "historical_dependency_not_established"
    OTHER_DOCUMENTED_REASON = "other_documented_reason"
    INSUFFICIENT_SOURCE_CONTEXT = "insufficient_source_context"
    HISTORICAL_DEPENDENCY_UNKNOWN = "historical_dependency_unknown"
    SOURCE_UNAVAILABLE = "source_unavailable"


UNRESOLVED_REASONS = {
    ReviewReason.INSUFFICIENT_SOURCE_CONTEXT,
    ReviewReason.HISTORICAL_DEPENDENCY_UNKNOWN,
    ReviewReason.SOURCE_UNAVAILABLE,
}


class AnalystDecision(BaseModel):
    model_config = ConfigDict(frozen=True)

    candidate_id: str = Field(min_length=12)
    status: EvidenceStatus
    reason_code: ReviewReason
    note: str = Field(min_length=20)
    reviewed_at: datetime
    source_basis: str = Field(min_length=20)

    @model_validator(mode="after")
    def valid_outcome(self) -> AnalystDecision:
        if self.reviewed_at.tzinfo is None:
            raise ValueError("review timestamp must include a timezone")
        if self.status in {EvidenceStatus.CANDIDATE}:
            raise ValueError("every candidate needs a review outcome")
        if (
            self.status is EvidenceStatus.ACCEPTED
            and self.reason_code is not ReviewReason.DIRECT_STAGE_EVIDENCE
        ):
            raise ValueError("accepted evidence requires direct stage evidence")
        if self.status is EvidenceStatus.REJECTED and self.reason_code in (
            {ReviewReason.DIRECT_STAGE_EVIDENCE} | UNRESOLVED_REASONS
        ):
            raise ValueError("rejected evidence requires a rejection reason")
        if (
            self.status is EvidenceStatus.NEEDS_REVIEW
            and self.reason_code not in UNRESOLVED_REASONS
        ):
            raise ValueError("unresolved evidence requires an unresolved reason")
        return self


class ReviewedCandidate(BaseModel):
    model_config = ConfigDict(frozen=True)

    candidate: ReviewableEvidence
    reason_code: ReviewReason
    source_basis: str


def load_verified_baseline(path: Path, manifest_path: Path) -> tuple[ReviewableEvidence, ...]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != manifest["baseline_sha256"]:
        raise ValueError("baseline digest mismatch")
    candidates = tuple(
        ReviewableEvidence.model_validate_json(line)
        for line in raw.decode("utf-8").splitlines() if line.strip()
    )
    ids = [item.candidate_id for item in candidates]
    if (
        ids != manifest["candidate_ids"] or len(ids) != manifest["candidate_count"]
        or len(ids) != len(set(ids))
        or any(item.case_id != manifest["case_id"] for item in candidates)
        or any(item.status is not EvidenceStatus.NEEDS_REVIEW for item in candidates)
    ):
        raise ValueError("baseline identities do not match its manifest")
    return candidates


def apply_analyst_decisions(
    candidates: tuple[ReviewableEvidence, ...],
    decisions: tuple[AnalystDecision, ...],
) -> tuple[ReviewedCandidate, ...]:
    identifiers = [item.candidate_id for item in candidates]
    decision_ids = [item.candidate_id for item in decisions]
    if len(identifiers) != len(set(identifiers)) or len(decision_ids) != len(set(decision_ids)):
        raise ValueError("duplicate candidate or decision identity")
    if set(identifiers) != set(decision_ids):
        raise ValueError("each baseline candidate requires exactly one analyst decision")
    lookup = {item.candidate_id: item for item in decisions}
    reviewed = []
    for item in candidates:
        decision = lookup[item.candidate_id]
        if decision.status is EvidenceStatus.NEEDS_REVIEW:
            candidate = ReviewableEvidence.model_validate({
                **item.model_dump(), "status": decision.status,
                "reviewer_note": decision.note, "reviewed_at": decision.reviewed_at,
            })
        else:
            candidate = item.transition(
                decision.status, note=decision.note, reviewed_at=decision.reviewed_at
            )
        reviewed.append(ReviewedCandidate(
            candidate=candidate, reason_code=decision.reason_code,
            source_basis=decision.source_basis,
        ))
    return tuple(reviewed)


def counts(records: tuple[ReviewedCandidate, ...]) -> dict[str, Any]:
    if any(item.candidate.status is EvidenceStatus.CANDIDATE for item in records):
        raise ValueError("unreviewed candidate cannot enter precision metrics")
    statuses = Counter(item.candidate.status for item in records)
    accepted = statuses[EvidenceStatus.ACCEPTED]
    rejected = statuses[EvidenceStatus.REJECTED]
    unresolved = statuses[EvidenceStatus.NEEDS_REVIEW]
    denominator = accepted + rejected
    return {
        "emitted": len(records), "accepted": accepted, "rejected": rejected,
        "needs_review": unresolved, "reviewed": denominator,
        "precision_numerator": accepted, "precision_denominator": denominator,
        "reviewed_candidate_precision": accepted / denominator if denominator else None,
    }


def grouped_counts(
    records: tuple[ReviewedCandidate, ...],
) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    by_stage = {
        stage.value: counts(tuple(
            item for item in records if item.candidate.lifecycle_stage is stage
        )) for stage in LifecycleStage if stage.value != "release"
    }
    by_rule = {
        rule: counts(tuple(
            item for item in records if item.candidate.classification_rule == rule
        )) for rule in RULES
    }
    return by_stage, by_rule


def historical_context(
    definition: CaseDefinition, history: HistoricalRun,
) -> dict[str, Any]:
    if history.case_id != definition.case.case_id:
        raise ValueError("history case mismatch")
    for item in history.results:
        for state in (item.before_state, item.after_state):
            if state is not None and state.capture_method is not CaptureMethod.COLLECTOR:
                raise ValueError("historical context requires collector file states")
    result: dict[str, Any] = {}
    for member in definition.cohort.repositories:
        paths = [item for item in history.results
                 if item.pair.repository.casefold() == member.repository.casefold()]
        supported = any(
            state is not None and state.status is FileStateStatus.PARSED
            and state.target_observations
            for item in paths for state in (item.before_state, item.after_state)
        )
        complete_absence = bool(paths) and all(
            item.pair.status is PairStatus.PAIRED
            and item.before_state is not None
            and item.after_state is not None
            and item.before_state.status is FileStateStatus.PARSED
            and item.after_state.status is FileStateStatus.PARSED
            and not item.before_state.target_observations
            and not item.after_state.target_observations
            for item in paths
        )
        status = (
            "historically_supported" if supported else
            "historically_not_established" if complete_absence else
            "historically_unknown"
        )
        result[member.repository] = {
            "status": status,
            "paths": [
                {
                    "path": item.pair.manifest_path,
                    "pair_status": item.pair.status.value,
                    "before_sha": item.pair.before.commit_sha if item.pair.before else None,
                    "after_sha": item.pair.after.commit_sha if item.pair.after else None,
                    "before_target": [
                        obs.raw_requirement for obs in (
                            item.before_state.target_observations if item.before_state else ()
                        )
                    ],
                    "after_target": [
                        obs.raw_requirement for obs in (
                            item.after_state.target_observations if item.after_state else ()
                        )
                    ],
                    "before_file_status": (
                        item.before_state.status.value if item.before_state else None
                    ),
                    "after_file_status": (
                        item.after_state.status.value if item.after_state else None
                    ),
                    "change_status": item.change_status.value,
                }
                for item in paths
            ],
        }
    return result


def collection_summary(path: Path) -> dict[str, Any]:
    manifest = LiveCollectionManifest.model_validate_json(path.read_text(encoding="utf-8"))
    attempts = [
        AttemptRecord.model_validate_json(item.read_text(encoding="utf-8"))
        for item in path.parent.glob("*.attempt.json")
    ]
    if len(attempts) != len(manifest.outcomes):
        raise ValueError("attempt count does not match planned collection outcomes")
    return {
        "run_id": manifest.run_id, "operational_status": manifest.status,
        "planned_tasks": len(manifest.planned_tasks),
        "outcomes": manifest.outcome_breakdown,
        "file_probe_availability": manifest.file_probe_availability.value,
        "pages_requested": sum(item.stats.pages_requested for item in attempts),
        "pages_completed": sum(item.stats.pages_completed for item in attempts),
        "requests_recorded": sum(len(item.stats.requests) for item in attempts),
        "retries": sum(item.stats.retry_count for item in attempts),
    }


def aggregate(
    definitions: tuple[CaseDefinition, ...],
    records: tuple[ReviewedCandidate, ...],
    histories: dict[str, HistoricalRun],
    collections: dict[str, Path],
) -> dict[str, Any]:
    unknown_rules = {
        item.candidate.classification_rule for item in records
    } - set(RULES)
    if unknown_rules:
        raise ValueError(f"unregistered detector rule in review ledger: {sorted(unknown_rules)}")
    cases = {}
    repositories = {}
    for definition in definitions:
        case_id = definition.case.case_id
        subset = tuple(item for item in records if item.candidate.case_id == case_id)
        by_repo = {}
        for member in definition.cohort.repositories:
            selected = tuple(
                item for item in subset
                if str(item.candidate.repository).rstrip("/").casefold()
                == f"https://github.com/{member.repository}".casefold()
            )
            by_repo[member.repository] = counts(selected)
            repositories[f"{case_id}/{member.repository}"] = by_repo[member.repository]
        cases[case_id] = {
            "cohort_size": len(definition.cohort.repositories),
            "collection": collection_summary(collections[case_id]),
            "history_run_id": histories[case_id].run_id,
            "historical_context": historical_context(definition, histories[case_id]),
            "candidates": counts(subset),
            "repositories": by_repo,
            "zero_candidate_repositories": [
                repo for repo, values in by_repo.items() if values["emitted"] == 0
            ],
        }
    if sum(item["candidates"]["emitted"] for item in cases.values()) != len(records):
        raise ValueError("review ledger contains candidates outside the declared cases")
    if sum(
        value["emitted"] for item in cases.values() for value in item["repositories"].values()
    ) != len(records):
        raise ValueError("review ledger contains candidates outside the frozen cohorts")
    by_stage, by_rule = grouped_counts(records)
    return {
        "overall": counts(records), "cases": cases,
        "by_lifecycle_stage": by_stage, "by_rule": by_rule,
        "review_burden_by_repository": repositories,
        "rejection_reasons": dict(Counter(
            item.reason_code.value for item in records
            if item.candidate.status is EvidenceStatus.REJECTED
        )),
        "limitations": [
            "Reviewed-candidate precision covers emitted candidates only; recall is unmeasured.",
            "Current cohort declarations do not establish historical target-version use.",
            "Zero emitted candidates do not establish absence of release impact.",
            "These frozen convenience cohorts are not ecosystem-representative.",
        ],
    }
