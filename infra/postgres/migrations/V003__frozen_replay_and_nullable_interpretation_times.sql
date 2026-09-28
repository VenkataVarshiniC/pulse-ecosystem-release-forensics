-- The frozen report has no assessment/finding creation timestamps. Preserve
-- absence instead of filling these with collection or load time.
BEGIN;
ALTER TABLE core.sufficiency_assessment ALTER COLUMN assessed_at DROP NOT NULL;
ALTER TABLE core.lifecycle_finding ALTER COLUMN created_at DROP NOT NULL;

CREATE TABLE ingestion.replay_attempt (
    case_version_id uuid NOT NULL REFERENCES core.investigation_case(case_version_id),
    attempt_number integer NOT NULL CHECK (attempt_number >= 1),
    matched_frozen_outputs boolean NOT NULL,
    output_sha256 char(64) NOT NULL CHECK (output_sha256 ~ '^[0-9a-f]{64}$'),
    source_manifest_sha256 char(64) NOT NULL
        CHECK (source_manifest_sha256 ~ '^[0-9a-f]{64}$'),
    PRIMARY KEY (case_version_id, attempt_number)
);

INSERT INTO public.schema_migrations(version, description)
VALUES (3, 'frozen replay audit and nullable source-absent interpretation times');
COMMIT;
