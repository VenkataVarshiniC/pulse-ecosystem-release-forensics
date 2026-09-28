-- M2.2 contract correction: release-run upstream probes and historical captures
-- must retain their real scope, without adding upstream repositories to cohorts
-- or inventing historical task attempts.
BEGIN;

ALTER TABLE ingestion.collection_run
    ADD COLUMN run_kind text NOT NULL DEFAULT 'release_collection'
    CHECK (run_kind IN ('release_collection', 'historical_reconstruction'));

ALTER TABLE ingestion.collection_task
    ALTER COLUMN repository_id DROP NOT NULL;
ALTER TABLE ingestion.collection_task
    ADD CONSTRAINT collection_task_upstream_scope_check
    CHECK (repository_id IS NOT NULL
           OR task_type IN ('pypi_version', 'github_releases', 'github_repository'));
ALTER TABLE ingestion.collection_task
    ADD CONSTRAINT collection_task_source_scope_uq
    UNIQUE (collection_task_id, source_id);

ALTER TABLE core.evidence_artifact
    ADD COLUMN history_run_id uuid REFERENCES ingestion.collection_run(collection_run_id);
ALTER TABLE core.evidence_artifact DROP CONSTRAINT evidence_artifact_check;
ALTER TABLE core.evidence_artifact DROP CONSTRAINT evidence_artifact_check1;
ALTER TABLE core.evidence_artifact
    ADD CONSTRAINT evidence_artifact_capture_link_check
    CHECK (
        (capture_method = 'collector'
         AND ((collection_task_id IS NOT NULL) <> (history_run_id IS NOT NULL)))
        OR (capture_method <> 'collector'
            AND collection_task_id IS NULL AND history_run_id IS NULL)
    );
ALTER TABLE core.evidence_artifact
    ADD CONSTRAINT evidence_artifact_task_source_fk
    FOREIGN KEY (collection_task_id, source_id)
    REFERENCES ingestion.collection_task(collection_task_id, source_id);

-- Phase 2 persisted a boolean stage-sufficiency flag, not the complete
-- four-way source-specific classification designed after Phase 2.
-- LEGACY_UNCLASSIFIED preserves false without guessing unavailable vs
-- insufficient vs conflicting. Finding UNKNOWN remains a separate status.
ALTER TABLE core.sufficiency_assessment
    DROP CONSTRAINT sufficiency_assessment_sufficiency_status_check;
ALTER TABLE core.sufficiency_assessment
    ADD CONSTRAINT sufficiency_assessment_sufficiency_status_check
    CHECK (sufficiency_status IN
           ('SUFFICIENT','INSUFFICIENT','SOURCE_UNAVAILABLE','CONFLICTING',
            'LEGACY_UNCLASSIFIED'));

INSERT INTO public.schema_migrations(version, description)
VALUES (2, 'frozen Phase 2 provenance and legacy sufficiency mapping');
COMMIT;
