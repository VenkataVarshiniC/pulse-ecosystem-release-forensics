"""Fail-closed, test-only DRAFT review submission; production has no identity policy."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import NAMESPACE_URL, UUID, uuid5

import psycopg
from psycopg.rows import dict_row

from pulse.api.config import PUBLISHED_SNAPSHOT_IDS, Settings
from pulse.api.errors import ApiError, missing
from pulse.api.schemas import ReviewReceipt, ReviewSubmission


@dataclass(frozen=True)
class ReviewPolicy:
    """Only isolated test fixtures may opt into writes with server-provided identity."""

    trusted_reviewer_identity: str | None = None
    eligible_draft_snapshots: frozenset[UUID] = field(default_factory=frozenset)


def review_gate(
    settings: Settings,
    policy: ReviewPolicy,
    snapshot_id: UUID,
    submission: ReviewSubmission,
    *,
    state: str,
    artifact_selected: bool,
    current_review_id: UUID | None,
) -> None:
    if snapshot_id in PUBLISHED_SNAPSHOT_IDS or state == "PUBLISHED_VALIDATION":
        raise ApiError("PUBLISHED_IMMUTABLE", "Published candidates cannot be reviewed", 409)
    if not submission.reason_code.strip():
        raise ApiError("INVALID_DECISION_REASON", "A nonempty review reason is required", 422)
    if (
        settings.environment != "test"
        or settings.database != "pulse_test"
        or not policy.trusted_reviewer_identity
        or snapshot_id not in policy.eligible_draft_snapshots
    ):
        raise ApiError("REVIEWER_NOT_AUTHORIZED", "Human review authority is not configured", 403)
    if state != "DRAFT":
        raise ApiError("INVALID_SNAPSHOT", "Review target must be an eligible DRAFT", 409)
    if not artifact_selected:
        raise ApiError("PROVENANCE_MISMATCH", "Candidate artifact is outside the snapshot", 409)
    if submission.expected_review_id != current_review_id:
        raise ApiError("STALE_REVIEW", "Review state changed; reload the candidate", 409)


class ReviewWriter:
    def __init__(self, settings: Settings, policy: ReviewPolicy):
        self.settings = settings
        self.policy = policy

    def _preflight(self, snapshot_id: UUID, submission: ReviewSubmission) -> None:
        # Reject all current published data before even opening a write connection.
        if snapshot_id in PUBLISHED_SNAPSHOT_IDS:
            raise ApiError("PUBLISHED_IMMUTABLE", "Published candidates cannot be reviewed", 409)
        if not submission.reason_code.strip():
            raise ApiError("INVALID_DECISION_REASON", "A nonempty review reason is required", 422)
        if (
            self.settings.environment != "test"
            or self.settings.database != "pulse_test"
            or not self.policy.trusted_reviewer_identity
            or snapshot_id not in self.policy.eligible_draft_snapshots
        ):
            raise ApiError(
                "REVIEWER_NOT_AUTHORIZED", "Human review authority is not configured", 403
            )

    def submit(
        self,
        case_version_id: UUID,
        snapshot_id: UUID,
        repository_id: UUID,
        candidate_id: UUID,
        submission: ReviewSubmission,
    ) -> ReviewReceipt:
        self._preflight(snapshot_id, submission)
        with psycopg.connect(
            host=self.settings.host,
            port=self.settings.port,
            dbname=self.settings.database,
            user=self.settings.user,
            password=self.settings.password,
            connect_timeout=3,
            row_factory=dict_row,
        ) as conn:
            return self.submit_in_connection(
                conn, case_version_id, snapshot_id, repository_id, candidate_id, submission
            )

    def submit_in_connection(
        self,
        conn: psycopg.Connection,
        case_version_id: UUID,
        snapshot_id: UUID,
        repository_id: UUID,
        candidate_id: UUID,
        submission: ReviewSubmission,
    ) -> ReviewReceipt:
        """Use an existing transaction in isolated fixture tests; never bypass the gate."""
        self._preflight(snapshot_id, submission)
        review_id = uuid5(
            NAMESPACE_URL, f"pulse:m5.2:{snapshot_id}:{candidate_id}:{submission.idempotency_key}"
        )
        with conn.transaction():
            target = conn.execute(
                """SELECT s.state,c.artifact_id,
                          EXISTS(SELECT 1 FROM core.snapshot_artifact sa
                                 WHERE sa.analysis_snapshot_id=s.analysis_snapshot_id
                                   AND sa.artifact_id=c.artifact_id) AS artifact_selected
                   FROM core.snapshot_candidate sc
                   JOIN core.analysis_snapshot s USING (analysis_snapshot_id)
                   JOIN core.candidate c USING (candidate_id)
                   JOIN core.cohort_membership m ON m.case_version_id=c.case_version_id
                        AND m.repository_id=c.repository_id
                   WHERE sc.analysis_snapshot_id=%s AND c.candidate_id=%s
                     AND c.case_version_id=%s AND c.repository_id=%s
                   FOR UPDATE OF c""",
                (snapshot_id, candidate_id, case_version_id, repository_id),
            ).fetchone()
            if target is None:
                raise missing()
            if target["state"] != "DRAFT":
                raise ApiError("INVALID_SNAPSHOT", "Review target is not an eligible DRAFT", 409)
            previous = conn.execute(
                """SELECT ar.review_id,ar.decision,ar.reason_code,ar.review_note,
                          ar.reviewer_identity,ar.reviewed_at
                   FROM core.analyst_review ar WHERE ar.review_id=%s""",
                (review_id,),
            ).fetchone()
            if previous is not None:
                if (
                    previous["decision"] != submission.decision.value
                    or previous["reason_code"] != submission.reason_code.strip()
                    or previous["review_note"] != submission.review_note
                    or previous["reviewer_identity"] != self.policy.trusted_reviewer_identity
                ):
                    raise ApiError(
                        "IDEMPOTENCY_CONFLICT", "Retry key was used for another review", 409
                    )
                return ReviewReceipt(
                    review_id=review_id,
                    candidate_id=candidate_id,
                    decision=previous["decision"],
                    reason_code=previous["reason_code"],
                    reviewed_at=previous["reviewed_at"],
                    idempotent_replay=True,
                )
            current = conn.execute(
                """SELECT ar.review_id,ar.review_cycle,ar.review_sequence,ar.decision
                   FROM core.snapshot_review sr
                   JOIN core.analyst_review ar USING (review_id)
                   WHERE sr.analysis_snapshot_id=%s AND ar.candidate_id=%s
                   ORDER BY ar.review_cycle DESC,ar.review_sequence DESC,ar.review_id DESC
                   LIMIT 1""",
                (snapshot_id, candidate_id),
            ).fetchone()
            review_gate(
                self.settings,
                self.policy,
                snapshot_id,
                submission,
                state=target["state"],
                artifact_selected=target["artifact_selected"],
                current_review_id=current["review_id"] if current else None,
            )
            if current and current["decision"] in {"ACCEPT", "REJECT"}:
                raise ApiError("STALE_REVIEW", "A terminal review already exists", 409)
            cycle = current["review_cycle"] if current else 1
            sequence = current["review_sequence"] + 1 if current else 1
            inserted = conn.execute(
                """INSERT INTO core.analyst_review
                   (review_id,candidate_id,review_cycle,review_sequence,reviewer_identity,
                    decision,reason_code,review_note,reviewed_at,review_origin)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,now(),'DIRECT')
                   RETURNING reviewed_at""",
                (
                    review_id,
                    candidate_id,
                    cycle,
                    sequence,
                    self.policy.trusted_reviewer_identity,
                    submission.decision.value,
                    submission.reason_code.strip(),
                    submission.review_note,
                ),
            ).fetchone()
            conn.execute(
                """INSERT INTO core.snapshot_review (analysis_snapshot_id,review_id)
                   VALUES (%s,%s)""",
                (snapshot_id, review_id),
            )
            return ReviewReceipt(
                review_id=review_id,
                candidate_id=candidate_id,
                decision=submission.decision,
                reason_code=submission.reason_code.strip(),
                reviewed_at=inserted["reviewed_at"],
                idempotent_replay=False,
            )
