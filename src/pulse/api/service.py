"""Case-scoped application assembly and provenance checks."""

from __future__ import annotations

import ipaddress
from collections import defaultdict
from urllib.parse import parse_qsl, urlsplit
from uuid import UUID

from pulse.api.errors import ApiError, missing
from pulse.api.repository import InvestigationRepository
from pulse.api.schemas import (
    ArtifactEvidence,
    Candidate,
    CandidatesResponse,
    EvidencePage,
    Finding,
    FindingsResponse,
    InvestigationDetail,
    InvestigationList,
    InvestigationSummary,
    Member,
    Observation,
    Provenance,
    RepositoryDetail,
    Scope,
    SourceState,
)


def public_url(value: str | None, access_class: str) -> str | None:
    if not value or access_class != "public":
        return None
    parsed = urlsplit(value)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        return None
    if parsed.hostname in {"localhost", "host.docker.internal"}:
        return None
    sensitive = ("token", "key", "auth", "secret", "password", "signature", "credential")
    if any(any(term in key.lower() for term in sensitive) for key, _ in parse_qsl(parsed.query)):
        return None
    try:
        if not ipaddress.ip_address(parsed.hostname).is_global:
            return None
    except ValueError:
        pass
    return value


def _scope(row: dict) -> Scope:
    return Scope.model_validate(row)


def _summary(row: dict) -> InvestigationSummary:
    return InvestigationSummary(scope=_scope(row), **row)


class InvestigationService:
    def __init__(self, repository: InvestigationRepository):
        self.repository = repository

    def list_investigations(self) -> InvestigationList:
        return InvestigationList(items=[_summary(row) for row in self.repository.investigations()])

    def investigation(self, case_version_id: UUID, snapshot_id: UUID) -> InvestigationDetail:
        row = self.repository.scope(case_version_id, snapshot_id)
        members = [
            Member.model_validate(item)
            for item in self.repository.members(case_version_id, snapshot_id)
        ]
        return InvestigationDetail(investigation=_summary(row), members=members)

    def repository_detail(
        self, case_version_id: UUID, snapshot_id: UUID, repository_id: UUID
    ) -> RepositoryDetail:
        row = self.repository.scope(case_version_id, snapshot_id)
        member = Member.model_validate(
            self.repository.member(case_version_id, snapshot_id, repository_id)
        )
        return RepositoryDetail(
            scope=_scope(row),
            member=member,
            source_states=[
                SourceState.model_validate(x)
                for x in self.repository.source_states(case_version_id, snapshot_id, repository_id)
            ],
            observations=[
                Observation.model_validate(x)
                for x in self.repository.observations(case_version_id, snapshot_id, repository_id)
            ],
            historical_pairs=self.repository.historical_pairs(
                case_version_id, snapshot_id, repository_id
            ),
            findings=self._findings(case_version_id, snapshot_id, repository_id),
            candidate_count=member.candidate_count,
        )

    def _findings(
        self, case_version_id: UUID, snapshot_id: UUID, repository_id: UUID
    ) -> list[Finding]:
        require_provenance(
            not self.repository.finding_support_mismatch(
                case_version_id, snapshot_id, repository_id
            )
        )
        return [
            Finding.model_validate(x)
            for x in self.repository.findings(case_version_id, snapshot_id, repository_id)
        ]

    def findings(
        self, case_version_id: UUID, snapshot_id: UUID, repository_id: UUID
    ) -> FindingsResponse:
        row = self.repository.scope(case_version_id, snapshot_id)
        self.repository.member(case_version_id, snapshot_id, repository_id)
        return FindingsResponse(
            scope=_scope(row),
            repository_id=repository_id,
            items=self._findings(case_version_id, snapshot_id, repository_id),
        )

    def finding(
        self, case_version_id: UUID, snapshot_id: UUID, repository_id: UUID, finding_id: UUID
    ) -> Finding:
        for item in self.findings(case_version_id, snapshot_id, repository_id).items:
            if item.finding_id == finding_id:
                return item
        raise missing()

    def candidates(
        self, case_version_id: UUID, snapshot_id: UUID, repository_id: UUID
    ) -> CandidatesResponse:
        row = self.repository.scope(case_version_id, snapshot_id)
        self.repository.member(case_version_id, snapshot_id, repository_id)
        return CandidatesResponse(
            scope=_scope(row),
            repository_id=repository_id,
            items=[
                Candidate.model_validate(x)
                for x in self.repository.candidates(case_version_id, snapshot_id, repository_id)
            ],
        )

    def candidate(
        self, case_version_id: UUID, snapshot_id: UUID, repository_id: UUID, candidate_id: UUID
    ) -> Candidate:
        for item in self.candidates(case_version_id, snapshot_id, repository_id).items:
            if item.candidate_id == candidate_id:
                return item
        raise missing()

    def evidence(
        self,
        case_version_id: UUID,
        snapshot_id: UUID,
        repository_id: UUID,
        cursor: UUID | None,
        limit: int,
        source_type: str | None,
        ref: str | None,
        path: str | None,
    ) -> EvidencePage:
        row = self.repository.scope(case_version_id, snapshot_id)
        self.repository.member(case_version_id, snapshot_id, repository_id)
        artifacts = self.repository.evidence(
            case_version_id, snapshot_id, repository_id, cursor, limit + 1, source_type, ref, path
        )
        has_more = len(artifacts) > limit
        artifacts = artifacts[:limit]
        ids = [x["artifact_id"] for x in artifacts]
        observations = (
            self.repository.observations(case_version_id, snapshot_id, repository_id, ids)
            if ids
            else []
        )
        by_artifact: dict[UUID, list[Observation]] = defaultdict(list)
        for observation in observations:
            by_artifact[observation["artifact_id"]].append(Observation.model_validate(observation))
        return EvidencePage(
            scope=_scope(row),
            repository_id=repository_id,
            items=[
                ArtifactEvidence(**artifact, observations=by_artifact[artifact["artifact_id"]])
                for artifact in artifacts
            ],
            next_cursor=ids[-1] if has_more else None,
        )

    def provenance(
        self, case_version_id: UUID, snapshot_id: UUID, repository_id: UUID, artifact_id: UUID
    ) -> Provenance:
        row = self.repository.scope(case_version_id, snapshot_id)
        self.repository.member(case_version_id, snapshot_id, repository_id)
        artifact = self.repository.artifact(
            case_version_id, snapshot_id, repository_id, artifact_id
        )
        allowed = public_url(artifact.pop("source_locator"), artifact["access_class"])
        external = [
            url
            for raw in artifact.pop("external_locators")
            if (url := public_url(raw, artifact["access_class"]))
        ]
        artifact.pop("access_class")
        return Provenance(
            scope=_scope(row),
            public_locator=allowed,
            external_public_locators=external,
            **artifact,
        )


def require_provenance(condition: bool) -> None:
    if not condition:
        raise ApiError("PROVENANCE_MISMATCH", "Selected evidence lineage is inconsistent", 409)
