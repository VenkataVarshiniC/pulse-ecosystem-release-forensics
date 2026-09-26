"""Deterministic normalization, detection, and explicit review decisions."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from pydantic import BaseModel, ConfigDict

from pulse.collection.raw import RawSnapshot
from pulse.evidence.detectors import ArtifactType, TextArtifact, detect_text_candidates
from pulse.models.case import CaseDefinition
from pulse.models.review import EvidenceStatus, ReviewableEvidence


class ReviewDecision(BaseModel):
    model_config = ConfigDict(frozen=True)

    source_identifier: str
    classification_rule: str
    status: EvidenceStatus
    reviewer_note: str
    reviewed_at: datetime


def detect_raw_candidates(
    definition: CaseDefinition, raw_root: Path
) -> tuple[ReviewableEvidence, ...]:
    """Detect candidates from preserved normalized GitHub payloads."""
    candidates: dict[str, ReviewableEvidence] = {}
    for path in sorted(raw_root.rglob("*.json")):
        snapshot = RawSnapshot.model_validate_json(path.read_text(encoding="utf-8"))
        kind = snapshot.query.get("kind")
        artifact_type = {
            "github_issues": ArtifactType.ISSUE,
            "github_pull_requests": ArtifactType.PULL_REQUEST,
            "github_releases": ArtifactType.RELEASE,
            "github_commits": ArtifactType.COMMIT,
        }.get(kind)
        if artifact_type is None:
            continue
        records = snapshot.payload if isinstance(snapshot.payload, list) else [snapshot.payload]
        for record in records:
            if not isinstance(record, dict):
                continue
            repository = record.get("repository") or snapshot.source_identifier
            if repository.casefold() not in {
                item.repository.casefold() for item in definition.cohort.repositories
            }:
                continue
            artifact = TextArtifact(
                repository=repository,
                artifact_type=artifact_type,
                source_url=record["url"],
                source_identifier=str(record["number"]),
                title=record["title"],
                body=record.get("body") or "",
                occurred_at=record["occurred_at"],
                observed_at=snapshot.retrieved_at,
            )
            for candidate in detect_text_candidates(definition.case, artifact):
                candidates[candidate.candidate_id] = candidate
    return tuple(sorted(candidates.values(), key=lambda item: item.candidate_id))


def load_review_decisions(path: Path) -> tuple[ReviewDecision, ...]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return tuple(ReviewDecision.model_validate(item) for item in payload)


def apply_review_decisions(
    candidates: tuple[ReviewableEvidence, ...], decisions: tuple[ReviewDecision, ...]
) -> tuple[ReviewableEvidence, ...]:
    lookup = {
        (decision.source_identifier, decision.classification_rule): decision
        for decision in decisions
    }
    reviewed = []
    for candidate in candidates:
        key = (candidate.evidence[0].source_identifier or "", candidate.classification_rule)
        decision = lookup.get(key)
        if decision is None:
            reviewed.append(candidate)
            continue
        reviewed.append(
            candidate.transition(
                decision.status,
                note=decision.reviewer_note,
                reviewed_at=decision.reviewed_at,
            )
        )
    return tuple(reviewed)
