"""API contract tests that do not need a running database."""

from __future__ import annotations

from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from pulse.api.app import app
from pulse.api.config import PUBLISHED_SNAPSHOT_IDS, Settings
from pulse.api.errors import ApiError
from pulse.api.review import ReviewPolicy, review_gate
from pulse.api.schemas import ReviewSubmission
from pulse.api.service import public_url


def _settings() -> Settings:
    return Settings("127.0.0.1", 55432, "pulse_test", "pulse_local", "fixture", "test")


def _submission(**overrides: object) -> ReviewSubmission:
    data = {
        "decision": "REJECT",
        "reason_code": "copied upstream",
        "idempotency_key": "fixture-request-1",
        "expected_review_id": None,
    }
    data.update(overrides)
    return ReviewSubmission.model_validate(data)


def test_openapi_and_local_cors_are_bounded() -> None:
    spec = app.openapi()
    paths = spec["paths"]
    assert "/api/v1/investigations" in paths
    assert any(path.endswith("/reviews") for path in paths)
    assert not any("sql" in path or "search" in path for path in paths)
    client = TestClient(app)
    allowed = client.options(
        "/api/v1/investigations",
        headers={"Origin": "http://localhost:5173", "Access-Control-Request-Method": "GET"},
    )
    assert allowed.headers["access-control-allow-origin"] == "http://localhost:5173"
    denied = client.options(
        "/api/v1/investigations",
        headers={"Origin": "https://other.example", "Access-Control-Request-Method": "GET"},
    )
    assert "access-control-allow-origin" not in denied.headers


@pytest.mark.parametrize(
    "value",
    [
        "file:///C:/secret",
        "http://github.com/example",
        "https://localhost/data",
        "https://127.0.0.1/data",
        "https://user:pass@github.com/data",
        "https://github.com/data?api_key=secret",
        "C:/local/path",
    ],
)
def test_provenance_locator_rejects_internal_or_credentialed_urls(value: str) -> None:
    assert public_url(value, "public") is None


def test_public_locator_requires_public_source() -> None:
    assert public_url("https://github.com/example/repo", "public") == (
        "https://github.com/example/repo"
    )
    assert public_url("https://github.com/example/repo", "restricted") is None


@pytest.mark.parametrize(
    "condition,code",
    [
        ({"state": "PUBLISHED_VALIDATION"}, "PUBLISHED_IMMUTABLE"),
        ({"artifact_selected": False}, "PROVENANCE_MISMATCH"),
        ({"current_review_id": uuid4()}, "STALE_REVIEW"),
        ({"state": "REVOKED"}, "INVALID_SNAPSHOT"),
    ],
)
def test_review_gate_fails_closed(condition: dict, code: str) -> None:
    snapshot = uuid4()
    policy = ReviewPolicy("fixture-reviewer", frozenset({snapshot}))
    fields = {"state": "DRAFT", "artifact_selected": True, "current_review_id": None}
    fields.update(condition)
    with pytest.raises(ApiError) as error:
        review_gate(_settings(), policy, snapshot, _submission(), **fields)
    assert error.value.code == code


def test_review_gate_requires_reason_and_trusted_identity() -> None:
    snapshot = uuid4()
    with pytest.raises(ApiError) as error:
        review_gate(
            _settings(),
            ReviewPolicy("fixture-reviewer", frozenset({snapshot})),
            snapshot,
            _submission(reason_code="  "),
            state="DRAFT",
            artifact_selected=True,
            current_review_id=None,
        )
    assert error.value.code == "INVALID_DECISION_REASON"
    with pytest.raises(ApiError) as error:
        review_gate(
            _settings(),
            ReviewPolicy(None, frozenset({snapshot})),
            snapshot,
            _submission(),
            state="DRAFT",
            artifact_selected=True,
            current_review_id=None,
        )
    assert error.value.code == "REVIEWER_NOT_AUTHORIZED"


def test_published_candidate_post_rejected_without_database_write() -> None:
    snapshot = next(iter(PUBLISHED_SNAPSHOT_IDS))
    response = TestClient(app).post(
        f"/api/v1/investigations/{uuid4()}/repositories/{uuid4()}/candidates/{uuid4()}/reviews",
        params={"snapshot_id": str(snapshot)},
        json=_submission().model_dump(mode="json"),
    )
    assert response.status_code == 409
    assert response.json()["code"] == "PUBLISHED_IMMUTABLE"


def test_invalid_request_returns_typed_error() -> None:
    response = TestClient(app).get(
        "/api/v1/investigations/not-a-uuid", params={"snapshot_id": str(uuid4())}
    )
    assert response.status_code == 422
    assert response.json()["code"] == "INVALID_REQUEST"
