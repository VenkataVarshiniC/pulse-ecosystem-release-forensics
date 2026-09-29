-- M4.1B: additive replay lineage and immutable bounded analytical publication.
BEGIN;

ALTER TABLE core.analysis_snapshot DROP CONSTRAINT analysis_snapshot_state_check;
ALTER TABLE core.analysis_snapshot ADD CONSTRAINT analysis_snapshot_state_check
    CHECK (state IN ('DRAFT','VALIDATED','PUBLISHED','PUBLISHED_VALIDATION','REVOKED'));
ALTER TABLE core.analysis_snapshot
    ADD COLUMN publication_manifest_sha256 char(64)
        CHECK (publication_manifest_sha256 IS NULL OR publication_manifest_sha256 ~ '^[0-9a-f]{64}$'),
    ADD COLUMN publication_fingerprint char(64)
        CHECK (publication_fingerprint IS NULL OR publication_fingerprint ~ '^[0-9a-f]{64}$'),
    ADD COLUMN published_at timestamptz;
ALTER TABLE core.analysis_snapshot ADD CONSTRAINT publication_fields_complete_check
    CHECK (state <> 'PUBLISHED_VALIDATION' OR
           (publication_manifest_sha256 IS NOT NULL AND publication_fingerprint IS NOT NULL
            AND published_at IS NOT NULL));

ALTER TABLE core.analyst_review
    ADD COLUMN review_origin text NOT NULL DEFAULT 'DIRECT'
        CHECK (review_origin IN ('DIRECT','INHERITED')),
    ADD COLUMN inherited_from_review_id uuid REFERENCES core.analyst_review(review_id);
ALTER TABLE core.analyst_review ADD CONSTRAINT inherited_review_reference_check
    CHECK ((review_origin = 'INHERITED') = (inherited_from_review_id IS NOT NULL));

CREATE TABLE core.replay_snapshot_lineage (
    analysis_snapshot_id uuid PRIMARY KEY REFERENCES core.analysis_snapshot(analysis_snapshot_id),
    replay_artifact_sha256 char(64) NOT NULL CHECK (replay_artifact_sha256 ~ '^[0-9a-f]{64}$'),
    input_manifest_sha256 char(64) NOT NULL CHECK (input_manifest_sha256 ~ '^[0-9a-f]{64}$'),
    rule_manifest_sha256 char(64) NOT NULL CHECK (rule_manifest_sha256 ~ '^[0-9a-f]{64}$'),
    rule_release_id text NOT NULL,
    source_git_commit char(40) NOT NULL CHECK (source_git_commit ~ '^[0-9a-f]{40}$'),
    metric_contract_version text NOT NULL,
    metric_registry_sha256 char(64) NOT NULL CHECK (metric_registry_sha256 ~ '^[0-9a-f]{64}$'),
    mart_model_version text NOT NULL,
    mart_model_sha256 char(64) NOT NULL CHECK (mart_model_sha256 ~ '^[0-9a-f]{64}$'),
    release_id text NOT NULL,
    case_id text NOT NULL,
    UNIQUE (release_id, case_id)
);

CREATE TABLE core.replay_candidate_lineage (
    candidate_id uuid PRIMARY KEY REFERENCES core.candidate(candidate_id),
    analysis_snapshot_id uuid NOT NULL REFERENCES core.replay_snapshot_lineage(analysis_snapshot_id),
    replay_candidate_source_id text NOT NULL,
    original_candidate_id uuid NOT NULL REFERENCES core.candidate(candidate_id),
    original_review_id uuid NOT NULL REFERENCES core.analyst_review(review_id),
    replay_review_id uuid NOT NULL UNIQUE REFERENCES core.analyst_review(review_id),
    normalized_fingerprint char(64) NOT NULL CHECK (normalized_fingerprint ~ '^[0-9a-f]{64}$'),
    evidence_content_sha256 char(64) NOT NULL CHECK (evidence_content_sha256 ~ '^[0-9a-f]{64}$'),
    equivalence text NOT NULL CHECK (equivalence = 'EXACT_EQUIVALENT'),
    equivalence_basis text NOT NULL,
    reuse_policy text NOT NULL,
    UNIQUE (analysis_snapshot_id, replay_candidate_source_id)
);

CREATE TABLE core.publication_record (
    analysis_snapshot_id uuid PRIMARY KEY REFERENCES core.analysis_snapshot(analysis_snapshot_id),
    publication_manifest_sha256 char(64) NOT NULL CHECK (publication_manifest_sha256 ~ '^[0-9a-f]{64}$'),
    publication_fingerprint char(64) NOT NULL CHECK (publication_fingerprint ~ '^[0-9a-f]{64}$'),
    metric_output_sha256 char(64) NOT NULL CHECK (metric_output_sha256 ~ '^[0-9a-f]{64}$'),
    mart_output_sha256 char(64) NOT NULL CHECK (mart_output_sha256 ~ '^[0-9a-f]{64}$'),
    metric_output jsonb NOT NULL,
    mart_row_fingerprints jsonb NOT NULL,
    published_at timestamptz NOT NULL
);

CREATE FUNCTION core.guard_published_snapshot() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
    IF OLD.state = 'PUBLISHED_VALIDATION' THEN
        RAISE EXCEPTION 'published validation snapshot is immutable';
    END IF;
    IF TG_OP = 'DELETE' THEN RETURN OLD; END IF;
    IF NEW.state = 'PUBLISHED_VALIDATION' AND NOT EXISTS (
        SELECT 1 FROM core.publication_record p
        WHERE p.analysis_snapshot_id = NEW.analysis_snapshot_id
          AND p.publication_manifest_sha256 = NEW.publication_manifest_sha256
          AND p.publication_fingerprint = NEW.publication_fingerprint
          AND p.published_at = NEW.published_at
    ) THEN
        RAISE EXCEPTION 'publication record must precede snapshot transition';
    END IF;
    RETURN NEW;
END $$;
CREATE TRIGGER guard_published_snapshot
    BEFORE UPDATE OR DELETE ON core.analysis_snapshot
    FOR EACH ROW EXECUTE FUNCTION core.guard_published_snapshot();

CREATE FUNCTION core.guard_published_selection() RETURNS trigger LANGUAGE plpgsql AS $$
DECLARE selected_snapshot uuid;
BEGIN
    selected_snapshot := CASE WHEN TG_OP = 'INSERT' THEN NEW.analysis_snapshot_id
                              ELSE OLD.analysis_snapshot_id END;
    IF EXISTS (SELECT 1 FROM core.analysis_snapshot
               WHERE analysis_snapshot_id = selected_snapshot
                 AND state = 'PUBLISHED_VALIDATION') THEN
        RAISE EXCEPTION 'published validation selection is immutable';
    END IF;
    IF TG_OP = 'UPDATE' AND NEW.analysis_snapshot_id <> OLD.analysis_snapshot_id
       AND EXISTS (SELECT 1 FROM core.analysis_snapshot
                   WHERE analysis_snapshot_id = NEW.analysis_snapshot_id
                     AND state = 'PUBLISHED_VALIDATION') THEN
        RAISE EXCEPTION 'cannot move selection into published validation snapshot';
    END IF;
    IF TG_OP = 'DELETE' THEN RETURN OLD; END IF;
    RETURN NEW;
END $$;
CREATE TRIGGER guard_published_snapshot_run BEFORE INSERT OR UPDATE OR DELETE
    ON core.snapshot_run FOR EACH ROW EXECUTE FUNCTION core.guard_published_selection();
CREATE TRIGGER guard_published_snapshot_artifact BEFORE INSERT OR UPDATE OR DELETE
    ON core.snapshot_artifact FOR EACH ROW EXECUTE FUNCTION core.guard_published_selection();
CREATE TRIGGER guard_published_snapshot_candidate BEFORE INSERT OR UPDATE OR DELETE
    ON core.snapshot_candidate FOR EACH ROW EXECUTE FUNCTION core.guard_published_selection();
CREATE TRIGGER guard_published_snapshot_review BEFORE INSERT OR UPDATE OR DELETE
    ON core.snapshot_review FOR EACH ROW EXECUTE FUNCTION core.guard_published_selection();
CREATE TRIGGER guard_published_snapshot_assessment BEFORE INSERT OR UPDATE OR DELETE
    ON core.snapshot_assessment FOR EACH ROW EXECUTE FUNCTION core.guard_published_selection();
CREATE TRIGGER guard_published_snapshot_finding BEFORE INSERT OR UPDATE OR DELETE
    ON core.snapshot_finding FOR EACH ROW EXECUTE FUNCTION core.guard_published_selection();
CREATE TRIGGER guard_published_replay_lineage BEFORE INSERT OR UPDATE OR DELETE
    ON core.replay_snapshot_lineage FOR EACH ROW EXECUTE FUNCTION core.guard_published_selection();
CREATE TRIGGER guard_published_candidate_lineage BEFORE INSERT OR UPDATE OR DELETE
    ON core.replay_candidate_lineage FOR EACH ROW EXECUTE FUNCTION core.guard_published_selection();

CREATE FUNCTION core.guard_published_selected_row() RETURNS trigger LANGUAGE plpgsql AS $$
DECLARE selected_id uuid;
DECLARE protected boolean;
BEGIN
    selected_id := (to_jsonb(OLD)->>CASE TG_TABLE_NAME
        WHEN 'candidate' THEN 'candidate_id'
        WHEN 'analyst_review' THEN 'review_id'
        WHEN 'sufficiency_assessment' THEN 'assessment_id'
        WHEN 'lifecycle_finding' THEN 'finding_id' END)::uuid;
    IF TG_TABLE_NAME = 'candidate' THEN
        SELECT EXISTS (SELECT 1 FROM core.snapshot_candidate x JOIN core.analysis_snapshot s
            USING (analysis_snapshot_id) WHERE x.candidate_id = selected_id
            AND s.state = 'PUBLISHED_VALIDATION') INTO protected;
    ELSIF TG_TABLE_NAME = 'analyst_review' THEN
        SELECT EXISTS (SELECT 1 FROM core.snapshot_review x JOIN core.analysis_snapshot s
            USING (analysis_snapshot_id) WHERE x.review_id = selected_id
            AND s.state = 'PUBLISHED_VALIDATION') INTO protected;
    ELSIF TG_TABLE_NAME = 'sufficiency_assessment' THEN
        SELECT EXISTS (SELECT 1 FROM core.snapshot_assessment x JOIN core.analysis_snapshot s
            USING (analysis_snapshot_id) WHERE x.assessment_id = selected_id
            AND s.state = 'PUBLISHED_VALIDATION') INTO protected;
    ELSE
        SELECT EXISTS (SELECT 1 FROM core.snapshot_finding x JOIN core.analysis_snapshot s
            USING (analysis_snapshot_id) WHERE x.finding_id = selected_id
            AND s.state = 'PUBLISHED_VALIDATION') INTO protected;
    END IF;
    IF protected THEN RAISE EXCEPTION 'published validation result row is immutable'; END IF;
    IF TG_OP = 'DELETE' THEN RETURN OLD; END IF;
    RETURN NEW;
END $$;
CREATE TRIGGER guard_published_candidate BEFORE UPDATE OR DELETE ON core.candidate
    FOR EACH ROW EXECUTE FUNCTION core.guard_published_selected_row();
CREATE TRIGGER guard_published_review BEFORE UPDATE OR DELETE ON core.analyst_review
    FOR EACH ROW EXECUTE FUNCTION core.guard_published_selected_row();
CREATE TRIGGER guard_published_assessment BEFORE UPDATE OR DELETE ON core.sufficiency_assessment
    FOR EACH ROW EXECUTE FUNCTION core.guard_published_selected_row();
CREATE TRIGGER guard_published_finding BEFORE UPDATE OR DELETE ON core.lifecycle_finding
    FOR EACH ROW EXECUTE FUNCTION core.guard_published_selected_row();

CREATE FUNCTION core.guard_publication_record() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
    RAISE EXCEPTION 'publication record is immutable';
END $$;
CREATE TRIGGER guard_publication_record BEFORE UPDATE OR DELETE ON core.publication_record
    FOR EACH ROW EXECUTE FUNCTION core.guard_publication_record();

INSERT INTO public.schema_migrations(version, description)
VALUES (5, 'governed replay snapshot lineage and immutable validation publication');
COMMIT;
