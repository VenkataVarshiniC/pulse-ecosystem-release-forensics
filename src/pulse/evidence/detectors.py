"""Transparent rules that produce reviewable candidate evidence."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from enum import StrEnum

from packaging.utils import canonicalize_name
from pydantic import BaseModel, ConfigDict, HttpUrl

from pulse.dependencies.models import DependencyTransition, TransitionKind
from pulse.models.case import ReleaseCase
from pulse.models.evidence import (
    Confidence,
    DownstreamEventType,
    EvidenceReference,
    LifecycleStage,
)
from pulse.models.review import EvidenceStatus, ReviewableEvidence

_FRICTION_TERMS = {"error", "fail", "failure", "break", "incompatible", "migration"}
_REMEDIATION_TERMS = {"fix", "support", "pin", "downgrade", "revert", "migrate", "compatible"}


class ArtifactType(StrEnum):
    ISSUE = "issue"
    PULL_REQUEST = "pull_request"
    RELEASE = "release"
    COMMIT = "commit"


class TextArtifact(BaseModel):
    model_config = ConfigDict(frozen=True)

    repository: str
    artifact_type: ArtifactType
    source_url: HttpUrl
    source_identifier: str
    title: str
    body: str = ""
    occurred_at: datetime
    observed_at: datetime


def detect_text_candidates(
    case: ReleaseCase, artifact: TextArtifact
) -> tuple[ReviewableEvidence, ...]:
    text = f"{artifact.title}\n{artifact.body}".casefold()
    package_names = {
        case.target_package.casefold(),
        canonicalize_name(case.target_package).replace("-", " "),
    }
    names_target = any(name in text for name in package_names)
    version_target = case.target_version.casefold() in text
    if not names_target or not version_target:
        return ()
    candidates = []
    if any(term in text for term in _FRICTION_TERMS):
        candidates.append(
            _text_candidate(
                case,
                artifact,
                stage=LifecycleStage.MIGRATION_FRICTION,
                event_type=DownstreamEventType.COMPATIBILITY_ISSUE,
                rule="text.version_specific_friction",
                reason=(
                    "The artifact names the target package and version and contains a "
                    "friction term. "
                    "Human review must verify that the surrounding context is qualifying evidence."
                ),
            )
        )
    if any(term in text for term in _REMEDIATION_TERMS):
        candidates.append(
            _text_candidate(
                case,
                artifact,
                stage=LifecycleStage.REMEDIATION,
                event_type=(
                    DownstreamEventType.MIGRATION_PR
                    if artifact.artifact_type is ArtifactType.PULL_REQUEST
                    else DownstreamEventType.WORKAROUND
                ),
                rule="text.version_specific_remediation",
                reason=(
                    "The artifact names the target package and version and contains a remediation "
                    "term. Human review must confirm the described action."
                ),
            )
        )
    if artifact.artifact_type is ArtifactType.RELEASE and "support" in text:
        candidates.append(
            _text_candidate(
                case,
                artifact,
                stage=LifecycleStage.RECOVERY_SIGNAL,
                event_type=DownstreamEventType.COMPATIBILITY_DECLARATION,
                rule="text.support_release",
                reason=(
                    "A downstream release names support for the target package and version. "
                    "Cohort eligibility still requires review."
                ),
            )
        )
    return _deduplicate(candidates)


def detect_transition_candidate(
    case: ReleaseCase, transition: DependencyTransition
) -> ReviewableEvidence | None:
    if canonicalize_name(transition.package) != canonicalize_name(case.target_package):
        return None
    observation = transition.after or transition.before
    if observation is None:
        return None
    if transition.kind is TransitionKind.TARGET_EXCLUDED:
        stage = LifecycleStage.REMEDIATION
        event_type = DownstreamEventType.VERSION_PIN
        rule = "dependency.target_excluded"
    elif transition.kind is TransitionKind.TARGET_ACCEPTED:
        stage = LifecycleStage.OBSERVED_ADOPTION
        event_type = DownstreamEventType.DEPENDENCY_UPGRADE
        rule = "dependency.target_accepted"
    else:
        return None
    source = str(observation.source)
    identity = _candidate_id(case.case_id, observation.repository, source, rule)
    return ReviewableEvidence(
        candidate_id=identity,
        case_id=case.case_id,
        repository=f"https://github.com/{observation.repository}",
        occurred_at=observation.observed_at,
        lifecycle_stage=stage,
        event_type=event_type,
        title=f"Dependency constraint {transition.kind.value.replace('_', ' ')}",
        target_package=case.target_package,
        target_release=case.target_version,
        evidence=(
            EvidenceReference(
                url=observation.source,
                observed_at=observation.observed_at,
                excerpt=f"constraint: {observation.constraint or '(unconstrained)'}",
                source_type="repository_file",
                source_identifier=observation.commit_reference,
            ),
        ),
        classification_rule=rule,
        classification_reason=transition.reason,
        confidence=Confidence.HIGH,
        status=EvidenceStatus.NEEDS_REVIEW,
    )


def _text_candidate(
    case: ReleaseCase,
    artifact: TextArtifact,
    *,
    stage: LifecycleStage,
    event_type: DownstreamEventType,
    rule: str,
    reason: str,
) -> ReviewableEvidence:
    source = str(artifact.source_url)
    return ReviewableEvidence(
        candidate_id=_candidate_id(case.case_id, artifact.repository, source, rule),
        case_id=case.case_id,
        repository=f"https://github.com/{artifact.repository}",
        occurred_at=artifact.occurred_at,
        lifecycle_stage=stage,
        event_type=event_type,
        title=artifact.title,
        target_package=case.target_package,
        target_release=case.target_version,
        evidence=(
            EvidenceReference(
                url=artifact.source_url,
                observed_at=artifact.observed_at,
                excerpt=artifact.body[:500] or artifact.title[:500],
                content_sha256=hashlib.sha256(
                    f"{artifact.title}\n{artifact.body}".encode()
                ).hexdigest(),
                source_type=artifact.artifact_type.value,
                source_identifier=artifact.source_identifier,
            ),
        ),
        classification_rule=rule,
        classification_reason=reason,
        confidence=Confidence.MEDIUM,
        status=EvidenceStatus.NEEDS_REVIEW,
    )


def _candidate_id(case_id: str, repository: str, source: str, rule: str) -> str:
    payload = json.dumps([case_id, repository.casefold(), source, rule], separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()[:24]


def _deduplicate(candidates: list[ReviewableEvidence]) -> tuple[ReviewableEvidence, ...]:
    return tuple({candidate.candidate_id: candidate for candidate in candidates}.values())
