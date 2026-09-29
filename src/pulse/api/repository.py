"""Parameterized, snapshot-scoped PostgreSQL reads. No SQL lives in HTTP routes."""

from __future__ import annotations

from typing import Any
from uuid import UUID

import psycopg
from psycopg.rows import dict_row

from pulse.api.config import PUBLISHED_SNAPSHOT_IDS, Settings
from pulse.api.errors import ApiError, missing


def connect_read(settings: Settings) -> psycopg.Connection[Any]:
    return psycopg.connect(
        host=settings.host,
        port=settings.port,
        dbname=settings.database,
        user=settings.user,
        password=settings.password,
        connect_timeout=3,
        options="-c default_transaction_read_only=on",
        row_factory=dict_row,
    )


class InvestigationRepository:
    def __init__(self, conn: psycopg.Connection[Any]):
        self.conn = conn

    def all(self, query: str, params: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
        return list(self.conn.execute(query, params).fetchall())

    def one(self, query: str, params: tuple[Any, ...] = ()) -> dict[str, Any] | None:
        return self.conn.execute(query, params).fetchone()

    def health(self) -> bool:
        return self.one("SELECT 1 AS available") is not None

    def investigations(self) -> list[dict[str, Any]]:
        return self.all(
            """SELECT c.case_id,c.case_version_id,c.case_version,c.case_name,
                      c.window_start,c.window_end,r.package_name_normalized AS package_name,
                      r.package_ecosystem,r.version AS release_version,
                      s.analysis_snapshot_id,s.state AS snapshot_state,s.rule_version,
                      s.metric_definition_version,s.model_version,
                      (SELECT count(*) FROM core.cohort_membership m
                       WHERE m.case_version_id=c.case_version_id) AS member_count
               FROM core.analysis_snapshot s
               JOIN core.publication_record p USING (analysis_snapshot_id)
               JOIN core.investigation_case c USING (case_version_id)
               JOIN core.dependency_release r ON r.release_id=c.target_release_id
               WHERE s.state='PUBLISHED_VALIDATION'
                 AND s.analysis_snapshot_id=ANY(%s::uuid[])
               ORDER BY r.package_name_normalized,c.case_version,s.analysis_snapshot_id""",
            (list(PUBLISHED_SNAPSHOT_IDS),),
        )

    def scope(self, case_version_id: UUID, snapshot_id: UUID) -> dict[str, Any]:
        if snapshot_id not in PUBLISHED_SNAPSHOT_IDS:
            raise ApiError(
                "INVALID_SNAPSHOT", "Snapshot is not approved for application reads", 404
            )
        row = self.one(
            """SELECT c.case_id,c.case_version_id,c.case_version,c.case_name,
                      c.window_start,c.window_end,r.package_name_normalized AS package_name,
                      r.package_ecosystem,r.version AS release_version,
                      s.analysis_snapshot_id,s.state AS snapshot_state,s.rule_version,
                      s.metric_definition_version,s.model_version,
                      (SELECT count(*) FROM core.cohort_membership m
                       WHERE m.case_version_id=c.case_version_id) AS member_count
               FROM core.analysis_snapshot s
               JOIN core.publication_record p USING (analysis_snapshot_id)
               JOIN core.investigation_case c USING (case_version_id)
               JOIN core.dependency_release r ON r.release_id=c.target_release_id
               WHERE s.analysis_snapshot_id=%s AND c.case_version_id=%s
                 AND s.state='PUBLISHED_VALIDATION'""",
            (snapshot_id, case_version_id),
        )
        if row is None:
            raise ApiError(
                "INVALID_SNAPSHOT", "Snapshot does not belong to this published case", 404
            )
        return row

    def members(self, case_version_id: UUID, snapshot_id: UUID) -> list[dict[str, Any]]:
        return self.all(
            """SELECT m.repository_id,r.canonical_full_name AS repository_name,
                      r.identity_status,m.selection_method,m.eligibility_status,
                      (SELECT count(*) FROM core.snapshot_candidate sc
                       JOIN core.candidate c USING (candidate_id)
                       WHERE sc.analysis_snapshot_id=%s AND c.case_version_id=m.case_version_id
                         AND c.repository_id=m.repository_id) AS candidate_count,
                      (SELECT count(*) FROM core.snapshot_finding sf
                       JOIN core.lifecycle_finding f USING (finding_id)
                       WHERE sf.analysis_snapshot_id=%s AND f.case_version_id=m.case_version_id
                         AND f.repository_id=m.repository_id AND f.finding_status='UNKNOWN')
                         AS unknown_count,
                      (SELECT count(*) FROM core.snapshot_finding sf
                       JOIN core.lifecycle_finding f USING (finding_id)
                       WHERE sf.analysis_snapshot_id=%s AND f.case_version_id=m.case_version_id
                         AND f.repository_id=m.repository_id
                         AND f.finding_status='NO_QUALIFYING_EVIDENCE_FOUND')
                         AS bounded_no_count,
                      (SELECT count(*) FROM core.snapshot_finding sf
                       JOIN core.lifecycle_finding f USING (finding_id)
                       WHERE sf.analysis_snapshot_id=%s AND f.case_version_id=m.case_version_id
                         AND f.repository_id=m.repository_id
                         AND f.finding_status='QUALIFYING_EVIDENCE') AS qualifying_count
               FROM core.cohort_membership m
               JOIN core.repository r USING (repository_id)
               WHERE m.case_version_id=%s
               ORDER BY r.canonical_full_name,m.repository_id""",
            (snapshot_id, snapshot_id, snapshot_id, snapshot_id, case_version_id),
        )

    def member(
        self, case_version_id: UUID, snapshot_id: UUID, repository_id: UUID
    ) -> dict[str, Any]:
        for row in self.members(case_version_id, snapshot_id):
            if row["repository_id"] == repository_id:
                return row
        raise missing()

    def source_states(
        self, case_version_id: UUID, snapshot_id: UUID, repository_id: UUID
    ) -> list[dict[str, Any]]:
        return self.all(
            """SELECT t.collection_task_id,s.source_type,t.task_type,t.required_flag AS required,
                      t.terminal_status,t.error_class
               FROM core.snapshot_run sr
               JOIN ingestion.collection_run cr USING (collection_run_id)
               JOIN ingestion.collection_task t ON t.collection_run_id=cr.collection_run_id
               JOIN ingestion.source_registry s ON s.source_id=t.source_id
               WHERE sr.analysis_snapshot_id=%s AND cr.case_version_id=%s
                 AND t.case_version_id=%s AND t.repository_id=%s
               ORDER BY t.plan_task_key,t.collection_task_id""",
            (snapshot_id, case_version_id, case_version_id, repository_id),
        )

    def observations(
        self,
        case_version_id: UUID,
        snapshot_id: UUID,
        repository_id: UUID,
        artifact_ids: list[UUID] | None = None,
    ) -> list[dict[str, Any]]:
        return self.all(
            """SELECT o.observation_id,o.artifact_id,o.observation_type,o.declared_constraint,
                      o.resolved_version,o.repository_ref,o.path_ref,o.observation_time,
                      o.historical_position,o.quality_status
               FROM core.dependency_observation o
               JOIN core.snapshot_artifact sa ON sa.artifact_id=o.artifact_id
               WHERE sa.analysis_snapshot_id=%s AND o.case_version_id=%s
                 AND o.repository_id=%s AND (%s::uuid[] IS NULL OR o.artifact_id=ANY(%s::uuid[]))
               ORDER BY o.observation_id""",
            (snapshot_id, case_version_id, repository_id, artifact_ids, artifact_ids),
        )

    def historical_pairs(
        self, case_version_id: UUID, snapshot_id: UUID, repository_id: UUID
    ) -> list[dict[str, Any]]:
        return self.all(
            """SELECT h.historical_pair_id,h.pair_status,h.path_ref,
                      h.before_observation_id,h.after_observation_id,h.reason,h.method_version
               FROM core.historical_pair h
               WHERE h.case_version_id=%s AND h.repository_id=%s
                 AND (h.before_observation_id IS NULL OR EXISTS
                      (SELECT 1 FROM core.dependency_observation o
                       JOIN core.snapshot_artifact sa ON sa.artifact_id=o.artifact_id
                       WHERE o.observation_id=h.before_observation_id
                         AND sa.analysis_snapshot_id=%s))
                 AND (h.after_observation_id IS NULL OR EXISTS
                      (SELECT 1 FROM core.dependency_observation o
                       JOIN core.snapshot_artifact sa ON sa.artifact_id=o.artifact_id
                       WHERE o.observation_id=h.after_observation_id
                         AND sa.analysis_snapshot_id=%s))
               ORDER BY h.path_ref,h.historical_pair_id""",
            (case_version_id, repository_id, snapshot_id, snapshot_id),
        )

    def findings(
        self, case_version_id: UUID, snapshot_id: UUID, repository_id: UUID
    ) -> list[dict[str, Any]]:
        return self.all(
            """SELECT f.finding_id,f.lifecycle_category,f.question_id,f.finding_status,
                      f.reason_code,f.confidence_level,f.rule_version,
                      a.sufficiency_status,a.reason_code AS sufficiency_reason_code,
                      a.required_source_set_version,
                      COALESCE((SELECT jsonb_agg(jsonb_build_object(
                          'source_type',sr.source_type,'reason_code',ar.reason_code,
                          'required',ar.required_flag) ORDER BY sr.source_type,ar.reason_code)
                          FROM core.assessment_source_reason ar
                          JOIN ingestion.source_registry sr USING (source_id)
                          WHERE ar.assessment_id=a.assessment_id),'[]'::jsonb)
                          AS source_reasons,
                      ARRAY(SELECT fas.artifact_id FROM core.finding_artifact_support fas
                            WHERE fas.finding_id=f.finding_id ORDER BY fas.artifact_id)
                          AS artifact_support_ids,
                      ARRAY(SELECT fos.observation_id FROM core.finding_observation_support fos
                            WHERE fos.finding_id=f.finding_id ORDER BY fos.observation_id)
                          AS observation_support_ids,
                      ARRAY(SELECT frs.review_id FROM core.finding_review_support frs
                            WHERE frs.finding_id=f.finding_id ORDER BY frs.review_id)
                          AS review_support_ids
               FROM core.snapshot_finding sf
               JOIN core.lifecycle_finding f USING (finding_id)
               JOIN core.snapshot_assessment sa ON sa.assessment_id=f.sufficiency_assessment_id
                    AND sa.analysis_snapshot_id=sf.analysis_snapshot_id
               JOIN core.sufficiency_assessment a ON a.assessment_id=sa.assessment_id
               WHERE sf.analysis_snapshot_id=%s AND f.case_version_id=%s
                 AND f.repository_id=%s
               ORDER BY f.lifecycle_category,f.question_id,f.finding_id""",
            (snapshot_id, case_version_id, repository_id),
        )

    def finding_support_mismatch(
        self, case_version_id: UUID, snapshot_id: UUID, repository_id: UUID
    ) -> bool:
        row = self.one(
            """SELECT (
                 EXISTS(SELECT 1 FROM core.snapshot_finding sf
                        JOIN core.lifecycle_finding f USING (finding_id)
                        JOIN core.finding_artifact_support x USING (finding_id)
                        JOIN core.evidence_artifact a ON a.artifact_id=x.artifact_id
                        WHERE sf.analysis_snapshot_id=%s AND f.case_version_id=%s
                          AND f.repository_id=%s AND
                          (a.repository_id IS DISTINCT FROM f.repository_id
                           AND a.repository_id IS NOT NULL
                           OR NOT EXISTS (SELECT 1 FROM core.snapshot_artifact sa
                                          WHERE sa.analysis_snapshot_id=sf.analysis_snapshot_id
                                            AND sa.artifact_id=x.artifact_id)))
                 OR EXISTS(SELECT 1 FROM core.snapshot_finding sf
                           JOIN core.lifecycle_finding f USING (finding_id)
                           JOIN core.finding_observation_support x USING (finding_id)
                           JOIN core.dependency_observation o USING (observation_id)
                           WHERE sf.analysis_snapshot_id=%s AND f.case_version_id=%s
                             AND f.repository_id=%s AND
                             (o.repository_id<>f.repository_id
                              OR NOT EXISTS (SELECT 1 FROM core.snapshot_artifact sa
                                             WHERE sa.analysis_snapshot_id=sf.analysis_snapshot_id
                                               AND sa.artifact_id=o.artifact_id)))
                 OR EXISTS(SELECT 1 FROM core.snapshot_finding sf
                           JOIN core.lifecycle_finding f USING (finding_id)
                           JOIN core.finding_review_support x USING (finding_id)
                           JOIN core.analyst_review ar USING (review_id)
                           JOIN core.candidate c USING (candidate_id)
                           WHERE sf.analysis_snapshot_id=%s AND f.case_version_id=%s
                             AND f.repository_id=%s AND
                             (c.repository_id<>f.repository_id
                              OR NOT EXISTS (SELECT 1 FROM core.snapshot_review sr
                                             WHERE sr.analysis_snapshot_id=sf.analysis_snapshot_id
                                               AND sr.review_id=x.review_id)))
               ) AS mismatch""",
            (
                snapshot_id,
                case_version_id,
                repository_id,
                snapshot_id,
                case_version_id,
                repository_id,
                snapshot_id,
                case_version_id,
                repository_id,
            ),
        )
        return bool(row["mismatch"])

    def candidates(
        self, case_version_id: UUID, snapshot_id: UUID, repository_id: UUID
    ) -> list[dict[str, Any]]:
        return self.all(
            """SELECT c.candidate_id,c.artifact_id,c.candidate_fingerprint,
                      c.lifecycle_category,c.candidate_rule_id,c.candidate_rule_version,
                      c.source_origin,c.candidate_status,c.candidate_reason,c.span_ref,
                      CASE WHEN rv.review_id IS NULL THEN NULL ELSE
                           jsonb_build_object('review_id',rv.review_id,'decision',rv.decision,
                             'reason_code',rv.reason_code,'review_note',rv.review_note,
                             'reviewed_at',rv.reviewed_at,'review_origin',rv.review_origin,
                             'inherited_from_review_id',rv.inherited_from_review_id,
                             'reviewer_identity',rv.reviewer_identity) END AS review,
                      l.original_candidate_id,l.original_review_id
               FROM core.snapshot_candidate sc
               JOIN core.candidate c USING (candidate_id)
               JOIN core.snapshot_artifact sa ON sa.analysis_snapshot_id=sc.analysis_snapshot_id
                    AND sa.artifact_id=c.artifact_id
               LEFT JOIN LATERAL (
                   SELECT ar.* FROM core.snapshot_review sr
                   JOIN core.analyst_review ar USING (review_id)
                   WHERE sr.analysis_snapshot_id=sc.analysis_snapshot_id
                     AND ar.candidate_id=c.candidate_id
                   ORDER BY ar.review_cycle DESC,ar.review_sequence DESC,ar.review_id DESC
                   LIMIT 1
               ) rv ON true
               LEFT JOIN core.replay_candidate_lineage l ON l.candidate_id=c.candidate_id
                    AND l.analysis_snapshot_id=sc.analysis_snapshot_id
               WHERE sc.analysis_snapshot_id=%s AND c.case_version_id=%s
                 AND c.repository_id=%s
               ORDER BY c.candidate_id""",
            (snapshot_id, case_version_id, repository_id),
        )

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
    ) -> list[dict[str, Any]]:
        return self.all(
            """SELECT a.artifact_id,a.artifact_type,s.source_type,a.capture_method,
                      a.repository_ref,a.source_event_time,a.retrieved_at,a.content_sha256
               FROM core.snapshot_artifact sa
               JOIN core.evidence_artifact a USING (artifact_id)
               JOIN ingestion.source_registry s ON s.source_id=a.source_id
               WHERE sa.analysis_snapshot_id=%s AND a.repository_id=%s
                 AND (%s::uuid IS NULL OR a.artifact_id>%s::uuid)
                 AND (%s::text IS NULL OR s.source_type=%s)
                 AND (%s::text IS NULL OR a.repository_ref=%s)
                 AND (%s::text IS NULL OR EXISTS
                     (SELECT 1 FROM core.dependency_observation o
                      WHERE o.artifact_id=a.artifact_id AND o.case_version_id=%s
                        AND o.repository_id=%s AND o.path_ref=%s))
               ORDER BY a.artifact_id LIMIT %s""",
            (
                snapshot_id,
                repository_id,
                cursor,
                cursor,
                source_type,
                source_type,
                ref,
                ref,
                path,
                case_version_id,
                repository_id,
                path,
                limit,
            ),
        )

    def artifact(
        self, case_version_id: UUID, snapshot_id: UUID, repository_id: UUID, artifact_id: UUID
    ) -> dict[str, Any]:
        row = self.one(
            """SELECT a.artifact_id,a.repository_id,a.artifact_type,s.source_type,
                      s.provider AS source_provider,s.access_class,a.source_locator,
                      a.repository_ref,a.capture_method,a.source_event_time,a.retrieved_at,
                      a.content_sha256,a.collection_task_id,
                      COALESCE(cr.collection_run_id,hr.collection_run_id)
                          AS collection_run_id,
                      COALESCE(cr.run_kind,hr.run_kind) AS collection_run_kind,
                      t.terminal_status AS task_status,
                      COALESCE(cr.run_status,hr.run_status) AS run_status,
                      ARRAY(SELECT c.candidate_id FROM core.snapshot_candidate sc
                            JOIN core.candidate c USING (candidate_id)
                            WHERE sc.analysis_snapshot_id=sa.analysis_snapshot_id
                              AND c.artifact_id=a.artifact_id AND c.repository_id=%s
                            ORDER BY c.candidate_id) AS linked_candidate_ids,
                      ARRAY(SELECT DISTINCT linked.finding_id FROM (
                                SELECT fs.finding_id FROM core.finding_artifact_support fs
                                WHERE fs.artifact_id=a.artifact_id
                                UNION
                                SELECT os.finding_id FROM core.finding_observation_support os
                                JOIN core.dependency_observation o USING (observation_id)
                                WHERE o.artifact_id=a.artifact_id
                            ) linked
                            JOIN core.snapshot_finding sf ON sf.finding_id=linked.finding_id
                            JOIN core.lifecycle_finding f ON f.finding_id=sf.finding_id
                            WHERE sf.analysis_snapshot_id=sa.analysis_snapshot_id
                              AND f.repository_id=%s
                            ORDER BY linked.finding_id) AS linked_finding_ids,
                      ARRAY(SELECT er.object_locator FROM core.external_evidence_reference er
                            WHERE er.artifact_id=a.artifact_id
                            ORDER BY er.external_ref_id) AS external_locators
               FROM core.snapshot_artifact sa
               JOIN core.evidence_artifact a USING (artifact_id)
               JOIN ingestion.source_registry s ON s.source_id=a.source_id
               LEFT JOIN ingestion.collection_task t ON t.collection_task_id=a.collection_task_id
               LEFT JOIN ingestion.collection_run cr ON cr.collection_run_id=t.collection_run_id
               LEFT JOIN ingestion.collection_run hr ON hr.collection_run_id=a.history_run_id
               WHERE sa.analysis_snapshot_id=%s AND a.artifact_id=%s
                 AND a.repository_id=%s""",
            (repository_id, repository_id, snapshot_id, artifact_id, repository_id),
        )
        if row is None:
            raise missing("PROVENANCE_MISMATCH")
        return row
