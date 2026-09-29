"""Versioned FastAPI boundary for bounded release investigations."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Annotated
from uuid import UUID

import psycopg
from fastapi import Depends, FastAPI, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from pulse.api.config import PUBLISHED_SNAPSHOT_IDS, Settings
from pulse.api.errors import ApiError, ErrorBody
from pulse.api.repository import InvestigationRepository, connect_read
from pulse.api.review import ReviewPolicy, ReviewWriter
from pulse.api.schemas import (
    Candidate,
    CandidatesResponse,
    EvidencePage,
    Finding,
    FindingsResponse,
    InvestigationDetail,
    InvestigationList,
    Provenance,
    RepositoryDetail,
    ReviewReceipt,
    ReviewSubmission,
)
from pulse.api.service import InvestigationService

API_PREFIX = "/api/v1"
ERROR_RESPONSES = {
    404: {"model": ErrorBody, "description": "Resource outside selected published scope"},
    409: {"model": ErrorBody, "description": "Snapshot, provenance or review conflict"},
    503: {"model": ErrorBody, "description": "Local database unavailable"},
}


def get_service() -> Iterator[InvestigationService]:
    try:
        settings = Settings.from_environment()
        with connect_read(settings) as conn:
            yield InvestigationService(InvestigationRepository(conn))
    except (ValueError, psycopg.OperationalError) as error:
        raise ApiError(
            "DATABASE_UNAVAILABLE", "Local PULSE database is unavailable", 503
        ) from error


ServiceDep = Annotated[InvestigationService, Depends(get_service)]
SnapshotQuery = Annotated[UUID, Query()]
LimitQuery = Annotated[int, Query(ge=1, le=100)]


def create_app(review_policy: ReviewPolicy | None = None) -> FastAPI:
    application = FastAPI(
        title="PULSE Investigation API",
        version="1.0.0",
        description="Published release-investigation reads and guarded review contract.",
    )
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type"],
    )
    policy = review_policy or ReviewPolicy()

    @application.exception_handler(ApiError)
    async def api_error(_request: Request, error: ApiError) -> JSONResponse:
        return JSONResponse(
            status_code=error.status,
            content=ErrorBody(code=error.code, message=error.message).model_dump(),
        )

    @application.exception_handler(RequestValidationError)
    async def invalid_request(_request: Request, _error: RequestValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content=ErrorBody(
                code="INVALID_REQUEST", message="Request fields are invalid"
            ).model_dump(),
        )

    @application.exception_handler(psycopg.OperationalError)
    async def database_unavailable(_request: Request, _error: psycopg.Error) -> JSONResponse:
        return JSONResponse(
            status_code=503,
            content=ErrorBody(
                code="DATABASE_UNAVAILABLE", message="Local PULSE database is unavailable"
            ).model_dump(),
        )

    @application.exception_handler(psycopg.Error)
    async def database_error(_request: Request, _error: psycopg.Error) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content=ErrorBody(
                code="DATABASE_ERROR", message="Database operation failed"
            ).model_dump(),
        )

    @application.get(f"{API_PREFIX}/health", summary="Check API and database reachability")
    def health(service: ServiceDep) -> dict[str, str | bool]:
        return {
            "status": "ok",
            "api_version": "v1",
            "database_reachable": service.repository.health(),
        }

    @application.get(
        f"{API_PREFIX}/investigations",
        response_model=InvestigationList,
        responses=ERROR_RESPONSES,
        summary="List approved published investigations",
    )
    def investigations(service: ServiceDep) -> InvestigationList:
        return service.list_investigations()

    @application.get(
        f"{API_PREFIX}/investigations/{{case_version_id}}",
        response_model=InvestigationDetail,
        responses=ERROR_RESPONSES,
        summary="Get exact investigation and declared cohort",
    )
    def investigation(
        case_version_id: UUID,
        snapshot_id: SnapshotQuery,
        service: ServiceDep,
    ) -> InvestigationDetail:
        return service.investigation(case_version_id, snapshot_id)

    @application.get(
        f"{API_PREFIX}/investigations/{{case_version_id}}/repositories/{{repository_id}}",
        response_model=RepositoryDetail,
        responses=ERROR_RESPONSES,
        summary="Inspect one declared repository and its literal evidence states",
    )
    def repository_detail(
        case_version_id: UUID,
        repository_id: UUID,
        snapshot_id: SnapshotQuery,
        service: ServiceDep,
    ) -> RepositoryDetail:
        return service.repository_detail(case_version_id, snapshot_id, repository_id)

    @application.get(
        f"{API_PREFIX}/investigations/{{case_version_id}}/repositories/{{repository_id}}/evidence",
        response_model=EvidencePage,
        responses=ERROR_RESPONSES,
        summary="Page selected evidence by immutable artifact ID",
    )
    def evidence(
        case_version_id: UUID,
        repository_id: UUID,
        snapshot_id: SnapshotQuery,
        service: ServiceDep,
        cursor: UUID | None = None,
        limit: LimitQuery = 25,
        source_type: str | None = None,
        ref: str | None = None,
        path: str | None = None,
    ) -> EvidencePage:
        return service.evidence(
            case_version_id, snapshot_id, repository_id, cursor, limit, source_type, ref, path
        )

    @application.get(
        f"{API_PREFIX}/investigations/{{case_version_id}}/repositories/{{repository_id}}"
        "/artifacts/{artifact_id}",
        response_model=Provenance,
        responses=ERROR_RESPONSES,
        summary="Inspect selected artifact and safe public provenance",
    )
    def artifact(
        case_version_id: UUID,
        repository_id: UUID,
        artifact_id: UUID,
        snapshot_id: SnapshotQuery,
        service: ServiceDep,
    ) -> Provenance:
        return service.provenance(case_version_id, snapshot_id, repository_id, artifact_id)

    @application.get(
        f"{API_PREFIX}/investigations/{{case_version_id}}/repositories/{{repository_id}}/findings",
        response_model=FindingsResponse,
        responses=ERROR_RESPONSES,
        summary="List literal selected findings and sufficiency reasons",
    )
    def findings(
        case_version_id: UUID,
        repository_id: UUID,
        snapshot_id: SnapshotQuery,
        service: ServiceDep,
    ) -> FindingsResponse:
        return service.findings(case_version_id, snapshot_id, repository_id)

    @application.get(
        f"{API_PREFIX}/investigations/{{case_version_id}}/repositories/{{repository_id}}"
        "/findings/{finding_id}",
        response_model=Finding,
        responses=ERROR_RESPONSES,
        summary="Get one selected bounded finding",
    )
    def finding(
        case_version_id: UUID,
        repository_id: UUID,
        finding_id: UUID,
        snapshot_id: SnapshotQuery,
        service: ServiceDep,
    ) -> Finding:
        return service.finding(case_version_id, snapshot_id, repository_id, finding_id)

    @application.get(
        f"{API_PREFIX}/investigations/{{case_version_id}}/repositories/{{repository_id}}/candidates",
        response_model=CandidatesResponse,
        responses=ERROR_RESPONSES,
        summary="List selected detector candidates and review lineage",
    )
    def candidates(
        case_version_id: UUID,
        repository_id: UUID,
        snapshot_id: SnapshotQuery,
        service: ServiceDep,
    ) -> CandidatesResponse:
        return service.candidates(case_version_id, snapshot_id, repository_id)

    @application.get(
        f"{API_PREFIX}/investigations/{{case_version_id}}/repositories/{{repository_id}}"
        "/candidates/{candidate_id}",
        response_model=Candidate,
        responses=ERROR_RESPONSES,
        summary="Get one selected candidate and inherited or direct review",
    )
    def candidate(
        case_version_id: UUID,
        repository_id: UUID,
        candidate_id: UUID,
        snapshot_id: SnapshotQuery,
        service: ServiceDep,
    ) -> Candidate:
        return service.candidate(case_version_id, snapshot_id, repository_id, candidate_id)

    @application.post(
        f"{API_PREFIX}/investigations/{{case_version_id}}/repositories/{{repository_id}}"
        "/candidates/{candidate_id}/reviews",
        response_model=ReviewReceipt,
        responses={**ERROR_RESPONSES, 403: {"model": ErrorBody}, 422: {"model": ErrorBody}},
        summary="Submit guarded human review on an eligible test DRAFT only",
    )
    def submit_review(
        case_version_id: UUID,
        repository_id: UUID,
        candidate_id: UUID,
        submission: ReviewSubmission,
        snapshot_id: SnapshotQuery,
    ) -> ReviewReceipt:
        if snapshot_id in PUBLISHED_SNAPSHOT_IDS:
            raise ApiError("PUBLISHED_IMMUTABLE", "Published candidates cannot be reviewed", 409)
        try:
            writer = ReviewWriter(Settings.from_environment(), policy)
        except ValueError as error:
            raise ApiError(
                "DATABASE_UNAVAILABLE", "Local PULSE database is unavailable", 503
            ) from error
        try:
            return writer.submit(
                case_version_id, snapshot_id, repository_id, candidate_id, submission
            )
        except psycopg.errors.UniqueViolation as error:
            raise ApiError(
                "STALE_REVIEW", "Review state changed; reload the candidate", 409
            ) from error

    return application


app = create_app()
