-- PULSE M2.1: PostgreSQL 16 relational foundation. No analytical/frozen evidence rows.
BEGIN;

CREATE SCHEMA ingestion;
CREATE SCHEMA core;
CREATE TABLE public.schema_migrations (
    version integer PRIMARY KEY,
    description text NOT NULL,
    applied_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE ingestion.source_registry (
    source_id uuid PRIMARY KEY,
    provider text NOT NULL,
    source_type text NOT NULL,
    source_version text NOT NULL,
    base_locator text,
    access_class text NOT NULL CHECK (access_class IN ('public', 'restricted', 'unknown')),
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (provider, source_type, source_version)
);

CREATE TABLE core.dependency_release (
    release_id uuid PRIMARY KEY,
    package_ecosystem text NOT NULL,
    package_name_normalized text NOT NULL,
    version text NOT NULL,
    release_time timestamptz,
    release_time_unresolved_reason text,
    release_source_id uuid NOT NULL REFERENCES ingestion.source_registry(source_id),
    release_artifact_id uuid,
    CHECK (release_time IS NOT NULL OR release_time_unresolved_reason IS NOT NULL),
    UNIQUE (package_ecosystem, package_name_normalized, version)
);

CREATE TABLE core.repository (
    repository_id uuid PRIMARY KEY,
    provider text NOT NULL,
    provider_repository_id text,
    canonical_full_name text NOT NULL,
    identity_status text NOT NULL CHECK (identity_status IN ('verified', 'provisional')),
    created_at timestamptz NOT NULL DEFAULT now(),
    CHECK ((identity_status = 'verified') = (provider_repository_id IS NOT NULL))
);
CREATE UNIQUE INDEX repository_provider_id_uq
    ON core.repository(provider, provider_repository_id)
    WHERE provider_repository_id IS NOT NULL;
CREATE TABLE core.repository_alias (
    alias_id uuid PRIMARY KEY,
    repository_id uuid NOT NULL REFERENCES core.repository(repository_id),
    full_name text NOT NULL,
    observed_from timestamptz,
    observed_until timestamptz,
    supporting_artifact_id uuid,
    CHECK (observed_until IS NULL OR observed_from IS NULL OR observed_until >= observed_from)
);

CREATE TABLE core.investigation_case (
    case_version_id uuid PRIMARY KEY,
    case_id uuid NOT NULL,
    case_version integer NOT NULL CHECK (case_version >= 1),
    case_name text NOT NULL,
    target_release_id uuid NOT NULL REFERENCES core.dependency_release(release_id),
    window_start timestamptz NOT NULL,
    window_end timestamptz NOT NULL,
    source_plan_version text NOT NULL,
    rule_version text NOT NULL,
    question_set_version text,
    status text NOT NULL CHECK (status IN ('DRAFT', 'FROZEN')),
    created_at timestamptz NOT NULL DEFAULT now(),
    CHECK (window_end >= window_start),
    UNIQUE (case_id, case_version)
);
CREATE TABLE core.cohort_membership (
    case_version_id uuid NOT NULL REFERENCES core.investigation_case(case_version_id),
    repository_id uuid NOT NULL REFERENCES core.repository(repository_id),
    selection_method text NOT NULL,
    eligibility_status text NOT NULL,
    selection_rationale text,
    included_at timestamptz NOT NULL,
    PRIMARY KEY (case_version_id, repository_id)
);

CREATE FUNCTION core.guard_frozen_case() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
    IF TG_OP = 'DELETE' THEN
        IF OLD.status = 'FROZEN' THEN
            RAISE EXCEPTION 'frozen case definition is immutable';
        END IF;
        RETURN OLD;
    END IF;
    IF OLD.status = 'FROZEN' THEN
        RAISE EXCEPTION 'frozen case definition is immutable';
    END IF;
    IF NEW.status = 'FROZEN'
       AND NOT EXISTS (
          SELECT 1 FROM core.cohort_membership m
          WHERE m.case_version_id = NEW.case_version_id
       ) THEN
        RAISE EXCEPTION 'cannot freeze a case without declared members';
    END IF;
    RETURN NEW;
END $$;
CREATE TRIGGER guard_frozen_case
    BEFORE UPDATE OR DELETE ON core.investigation_case
    FOR EACH ROW EXECUTE FUNCTION core.guard_frozen_case();
CREATE FUNCTION core.guard_frozen_membership() RETURNS trigger LANGUAGE plpgsql AS $$
DECLARE v_case_version_id uuid;
BEGIN
    v_case_version_id := CASE WHEN TG_OP = 'INSERT' THEN NEW.case_version_id ELSE OLD.case_version_id END;
    IF (SELECT status FROM core.investigation_case WHERE case_version_id = v_case_version_id) = 'FROZEN' THEN
        RAISE EXCEPTION 'frozen cohort membership is immutable';
    END IF;
    IF TG_OP = 'UPDATE' AND NEW.case_version_id <> OLD.case_version_id
       AND (SELECT status FROM core.investigation_case
            WHERE case_version_id = NEW.case_version_id) = 'FROZEN' THEN
        RAISE EXCEPTION 'cannot move membership into frozen case';
    END IF;
    IF TG_OP = 'DELETE' THEN RETURN OLD; END IF;
    RETURN NEW;
END $$;
CREATE TRIGGER guard_frozen_membership
    BEFORE INSERT OR UPDATE OR DELETE ON core.cohort_membership
    FOR EACH ROW EXECUTE FUNCTION core.guard_frozen_membership();

CREATE TABLE ingestion.collection_run (
    collection_run_id uuid PRIMARY KEY,
    case_version_id uuid NOT NULL REFERENCES core.investigation_case(case_version_id),
    collector_version text NOT NULL,
    source_plan_version text NOT NULL,
    started_at timestamptz NOT NULL,
    completed_at timestamptz,
    run_status text NOT NULL CHECK (run_status IN ('running', 'complete', 'incomplete', 'failed')),
    resume_of_run_id uuid REFERENCES ingestion.collection_run(collection_run_id),
    created_at timestamptz NOT NULL DEFAULT now(),
    CHECK (completed_at IS NULL OR completed_at >= started_at),
    UNIQUE (collection_run_id, case_version_id)
);
CREATE TABLE ingestion.collection_task (
    collection_task_id uuid PRIMARY KEY,
    collection_run_id uuid NOT NULL,
    case_version_id uuid NOT NULL,
    repository_id uuid NOT NULL,
    source_id uuid NOT NULL REFERENCES ingestion.source_registry(source_id),
    plan_task_key text NOT NULL,
    task_type text NOT NULL,
    required_flag boolean NOT NULL,
    request_locator text NOT NULL,
    attempt_count integer NOT NULL DEFAULT 0 CHECK (attempt_count >= 0),
    terminal_status text NOT NULL CHECK (
        terminal_status IN ('pending','succeeded','partial','rate_limited',
                            'not_found','unauthorized','failed')
    ),
    started_at timestamptz,
    completed_at timestamptz,
    error_class text,
    FOREIGN KEY (collection_run_id, case_version_id)
        REFERENCES ingestion.collection_run(collection_run_id, case_version_id),
    FOREIGN KEY (case_version_id, repository_id)
        REFERENCES core.cohort_membership(case_version_id, repository_id),
    CHECK (completed_at IS NULL OR started_at IS NULL OR completed_at >= started_at),
    UNIQUE (collection_run_id, plan_task_key)
);
ALTER TABLE ingestion.collection_task
    ADD CONSTRAINT collection_task_capture_scope_uq
    UNIQUE (collection_task_id, source_id, repository_id);
CREATE TABLE ingestion.task_attempt (
    collection_task_id uuid NOT NULL REFERENCES ingestion.collection_task(collection_task_id),
    attempt_number integer NOT NULL CHECK (attempt_number >= 1),
    outcome text NOT NULL CHECK (
        outcome IN ('succeeded','partial','rate_limited','not_found','unauthorized','failed')
    ),
    attempted_at timestamptz NOT NULL,
    source_status text,
    artifact_digest char(64) CHECK (
        artifact_digest IS NULL OR artifact_digest ~ '^[0-9a-f]{64}$'
    ),
    PRIMARY KEY (collection_task_id, attempt_number)
);
CREATE TABLE ingestion.load_audit (
    load_id uuid PRIMARY KEY,
    idempotency_key text NOT NULL,
    input_artifact_id uuid,
    input_digest char(64) NOT NULL CHECK (input_digest ~ '^[0-9a-f]{64}$'),
    target_relation text NOT NULL,
    loader_version text NOT NULL,
    loaded_count integer NOT NULL CHECK (loaded_count >= 0),
    rejected_count integer NOT NULL CHECK (rejected_count >= 0),
    loaded_at timestamptz NOT NULL DEFAULT now(),
    result text NOT NULL CHECK (result IN ('succeeded','rejected','quarantined')),
    quarantine_ref text
);
CREATE UNIQUE INDEX load_audit_success_key_uq
    ON ingestion.load_audit(idempotency_key, target_relation)
    WHERE result = 'succeeded';

CREATE TABLE core.evidence_artifact (
    artifact_id uuid PRIMARY KEY,
    capture_fingerprint char(64) NOT NULL UNIQUE
        CHECK (capture_fingerprint ~ '^[0-9a-f]{64}$'),
    source_id uuid NOT NULL REFERENCES ingestion.source_registry(source_id),
    repository_id uuid REFERENCES core.repository(repository_id),
    collection_task_id uuid REFERENCES ingestion.collection_task(collection_task_id),
    artifact_type text NOT NULL,
    source_locator text NOT NULL,
    repository_ref text,
    source_event_time timestamptz,
    retrieved_at timestamptz NOT NULL,
    capture_method text NOT NULL
        CHECK (capture_method IN ('collector','connector_assisted','fixture')),
    content_sha256 char(64) NOT NULL CHECK (content_sha256 ~ '^[0-9a-f]{64}$'),
    raw_snapshot_uri text NOT NULL,
    media_type text NOT NULL,
    parser_version text,
    CHECK ((capture_method = 'collector') = (collection_task_id IS NOT NULL)),
    CHECK (capture_method <> 'collector' OR repository_id IS NOT NULL),
    FOREIGN KEY (collection_task_id, source_id, repository_id)
        REFERENCES ingestion.collection_task(collection_task_id, source_id, repository_id),
    UNIQUE (artifact_id, repository_id)
);
ALTER TABLE core.dependency_release
    ADD CONSTRAINT dependency_release_artifact_fk
    FOREIGN KEY (release_artifact_id) REFERENCES core.evidence_artifact(artifact_id);
ALTER TABLE core.repository_alias
    ADD CONSTRAINT repository_alias_artifact_fk
    FOREIGN KEY (supporting_artifact_id) REFERENCES core.evidence_artifact(artifact_id);
ALTER TABLE ingestion.load_audit
    ADD CONSTRAINT load_audit_artifact_fk
    FOREIGN KEY (input_artifact_id) REFERENCES core.evidence_artifact(artifact_id);
CREATE TABLE core.external_evidence_reference (
    external_ref_id uuid PRIMARY KEY,
    artifact_id uuid NOT NULL REFERENCES core.evidence_artifact(artifact_id),
    provider text NOT NULL,
    source_object_type text NOT NULL,
    provider_object_id text NOT NULL,
    object_locator text NOT NULL,
    repository_ref text,
    environment_ref text,
    observed_at timestamptz,
    UNIQUE (artifact_id, provider, source_object_type, provider_object_id)
);
CREATE FUNCTION core.guard_immutable_artifact() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
    RAISE EXCEPTION 'captured artifact provenance is immutable';
END $$;
CREATE TRIGGER guard_immutable_artifact
    BEFORE UPDATE OR DELETE ON core.evidence_artifact
    FOR EACH ROW EXECUTE FUNCTION core.guard_immutable_artifact();

CREATE TABLE core.dependency_observation (
    observation_id uuid PRIMARY KEY,
    observation_fingerprint char(64) NOT NULL UNIQUE
        CHECK (observation_fingerprint ~ '^[0-9a-f]{64}$'),
    case_version_id uuid NOT NULL,
    repository_id uuid NOT NULL,
    artifact_id uuid NOT NULL,
    observation_type text NOT NULL CHECK (
        observation_type IN ('CURRENT_DECLARATION','HISTORICAL_DECLARATION',
                             'RESOLVED_VERSION','PATH_STATE','COMPATIBILITY_CONTEXT')
    ),
    package_name text NOT NULL,
    declared_constraint text,
    resolved_version text,
    repository_ref text,
    path_ref text,
    observation_time timestamptz,
    historical_position text CHECK (
        historical_position IN ('BEFORE_RELEASE','AFTER_RELEASE','UNRESOLVED')
    ),
    environment_ref text,
    parser_version text NOT NULL,
    quality_status text NOT NULL,
    FOREIGN KEY (case_version_id, repository_id)
        REFERENCES core.cohort_membership(case_version_id, repository_id),
    FOREIGN KEY (artifact_id, repository_id)
        REFERENCES core.evidence_artifact(artifact_id, repository_id),
    CHECK (
        (observation_type IN ('CURRENT_DECLARATION','HISTORICAL_DECLARATION')
          AND declared_constraint IS NOT NULL AND resolved_version IS NULL)
        OR (observation_type = 'RESOLVED_VERSION'
          AND resolved_version IS NOT NULL AND declared_constraint IS NULL)
        OR (observation_type IN ('PATH_STATE','COMPATIBILITY_CONTEXT')
          AND declared_constraint IS NULL AND resolved_version IS NULL)
    ),
    CHECK (observation_type <> 'HISTORICAL_DECLARATION'
        OR (repository_ref IS NOT NULL AND path_ref IS NOT NULL))
);
CREATE TABLE core.historical_pair (
    historical_pair_id uuid PRIMARY KEY,
    case_version_id uuid NOT NULL,
    repository_id uuid NOT NULL,
    package_name text NOT NULL,
    path_ref text NOT NULL,
    before_observation_id uuid REFERENCES core.dependency_observation(observation_id),
    after_observation_id uuid REFERENCES core.dependency_observation(observation_id),
    pair_status text NOT NULL CHECK (
        pair_status IN ('PAIRED','AFTER_ONLY','UNRESOLVED','CROSS_FILE_AMBIGUITY')
    ),
    pair_version integer NOT NULL CHECK (pair_version >= 1),
    method_version text NOT NULL,
    reason text NOT NULL,
    FOREIGN KEY (case_version_id, repository_id)
        REFERENCES core.cohort_membership(case_version_id, repository_id),
    CHECK (
        (pair_status = 'PAIRED'
          AND before_observation_id IS NOT NULL AND after_observation_id IS NOT NULL
          AND before_observation_id <> after_observation_id)
        OR (pair_status = 'AFTER_ONLY'
          AND before_observation_id IS NULL AND after_observation_id IS NOT NULL)
        OR pair_status IN ('UNRESOLVED','CROSS_FILE_AMBIGUITY')
    ),
    UNIQUE (case_version_id, repository_id, package_name, path_ref, method_version, pair_version)
);
CREATE TABLE core.candidate (
    candidate_id uuid PRIMARY KEY,
    candidate_fingerprint char(64) NOT NULL UNIQUE
        CHECK (candidate_fingerprint ~ '^[0-9a-f]{64}$'),
    case_version_id uuid NOT NULL,
    repository_id uuid NOT NULL,
    artifact_id uuid NOT NULL REFERENCES core.evidence_artifact(artifact_id),
    baseline_version text NOT NULL,
    candidate_rule_id text NOT NULL,
    candidate_rule_version text NOT NULL,
    lifecycle_category text NOT NULL,
    source_origin text NOT NULL
        CHECK (source_origin IN ('LOCAL_DOWNSTREAM','COPIED_UPSTREAM','UNRESOLVED')),
    emitted_at timestamptz,
    candidate_status text NOT NULL CHECK (candidate_status IN ('EMITTED','WITHDRAWN')),
    candidate_reason text NOT NULL,
    span_ref text NOT NULL,
    candidate_payload_ref text,
    FOREIGN KEY (case_version_id, repository_id)
        REFERENCES core.cohort_membership(case_version_id, repository_id),
    FOREIGN KEY (artifact_id, repository_id)
        REFERENCES core.evidence_artifact(artifact_id, repository_id)
);
CREATE TABLE core.analyst_review (
    review_id uuid PRIMARY KEY,
    candidate_id uuid NOT NULL REFERENCES core.candidate(candidate_id),
    review_cycle integer NOT NULL CHECK (review_cycle >= 1),
    review_sequence integer NOT NULL CHECK (review_sequence >= 1),
    reviewer_identity text,
    decision text NOT NULL CHECK (decision IN ('ACCEPT','REJECT','NEEDS_EVIDENCE')),
    reason_code text NOT NULL,
    review_note text,
    reviewed_at timestamptz NOT NULL,
    UNIQUE (candidate_id, review_cycle, review_sequence)
);
CREATE UNIQUE INDEX analyst_review_terminal_uq
    ON core.analyst_review(candidate_id, review_cycle)
    WHERE decision IN ('ACCEPT','REJECT');

CREATE TABLE core.sufficiency_assessment (
    assessment_id uuid PRIMARY KEY,
    case_version_id uuid NOT NULL,
    repository_id uuid NOT NULL,
    lifecycle_category text NOT NULL,
    question_id text NOT NULL,
    assessment_version integer NOT NULL CHECK (assessment_version >= 1),
    sufficiency_status text NOT NULL CHECK (
        sufficiency_status IN ('SUFFICIENT','INSUFFICIENT','SOURCE_UNAVAILABLE','CONFLICTING')
    ),
    reason_code text NOT NULL,
    required_source_set_version text NOT NULL,
    rule_version text NOT NULL,
    assessed_at timestamptz NOT NULL,
    FOREIGN KEY (case_version_id, repository_id)
        REFERENCES core.cohort_membership(case_version_id, repository_id),
    UNIQUE (case_version_id, repository_id, lifecycle_category, question_id, assessment_version),
    UNIQUE (assessment_id, case_version_id, repository_id, lifecycle_category, question_id)
);
CREATE TABLE core.assessment_source_reason (
    assessment_id uuid NOT NULL REFERENCES core.sufficiency_assessment(assessment_id),
    source_id uuid NOT NULL REFERENCES ingestion.source_registry(source_id),
    reason_code text NOT NULL,
    required_flag boolean NOT NULL,
    PRIMARY KEY (assessment_id, source_id, reason_code)
);
CREATE TABLE core.lifecycle_finding (
    finding_id uuid PRIMARY KEY,
    case_version_id uuid NOT NULL,
    repository_id uuid NOT NULL,
    lifecycle_category text NOT NULL,
    question_id text NOT NULL,
    finding_version integer NOT NULL CHECK (finding_version >= 1),
    finding_status text NOT NULL CHECK (
        finding_status IN ('QUALIFYING_EVIDENCE','NO_QUALIFYING_EVIDENCE_FOUND','UNKNOWN')
    ),
    sufficiency_assessment_id uuid NOT NULL,
    rule_version text NOT NULL,
    reason_code text NOT NULL,
    confidence_level text,
    created_at timestamptz NOT NULL,
    FOREIGN KEY (case_version_id, repository_id)
        REFERENCES core.cohort_membership(case_version_id, repository_id),
    FOREIGN KEY (sufficiency_assessment_id, case_version_id, repository_id,
                 lifecycle_category, question_id)
        REFERENCES core.sufficiency_assessment(assessment_id, case_version_id, repository_id,
                                               lifecycle_category, question_id),
    UNIQUE (case_version_id, repository_id, lifecycle_category, question_id, finding_version)
);
CREATE TABLE core.finding_artifact_support (
    finding_id uuid NOT NULL REFERENCES core.lifecycle_finding(finding_id),
    artifact_id uuid NOT NULL REFERENCES core.evidence_artifact(artifact_id),
    support_role text NOT NULL,
    PRIMARY KEY (finding_id, artifact_id, support_role)
);
CREATE TABLE core.finding_observation_support (
    finding_id uuid NOT NULL REFERENCES core.lifecycle_finding(finding_id),
    observation_id uuid NOT NULL REFERENCES core.dependency_observation(observation_id),
    support_role text NOT NULL,
    PRIMARY KEY (finding_id, observation_id, support_role)
);
CREATE TABLE core.finding_review_support (
    finding_id uuid NOT NULL REFERENCES core.lifecycle_finding(finding_id),
    review_id uuid NOT NULL REFERENCES core.analyst_review(review_id),
    support_role text NOT NULL,
    PRIMARY KEY (finding_id, review_id, support_role)
);

CREATE TABLE core.analysis_snapshot (
    analysis_snapshot_id uuid PRIMARY KEY,
    case_version_id uuid NOT NULL REFERENCES core.investigation_case(case_version_id),
    source_plan_version text NOT NULL,
    rule_version text NOT NULL,
    metric_definition_version text NOT NULL,
    model_version text NOT NULL,
    loader_version text NOT NULL,
    generated_at timestamptz NOT NULL,
    state text NOT NULL CHECK (state IN ('DRAFT','VALIDATED','PUBLISHED','REVOKED')),
    manifest_sha256 char(64) NOT NULL UNIQUE CHECK (manifest_sha256 ~ '^[0-9a-f]{64}$'),
    supersedes_snapshot_id uuid REFERENCES core.analysis_snapshot(analysis_snapshot_id)
);
CREATE TABLE core.snapshot_run (
    analysis_snapshot_id uuid NOT NULL REFERENCES core.analysis_snapshot(analysis_snapshot_id),
    collection_run_id uuid NOT NULL REFERENCES ingestion.collection_run(collection_run_id),
    PRIMARY KEY (analysis_snapshot_id, collection_run_id)
);
CREATE TABLE core.snapshot_artifact (
    analysis_snapshot_id uuid NOT NULL REFERENCES core.analysis_snapshot(analysis_snapshot_id),
    artifact_id uuid NOT NULL REFERENCES core.evidence_artifact(artifact_id),
    expected_sha256 char(64) NOT NULL CHECK (expected_sha256 ~ '^[0-9a-f]{64}$'),
    sort_ordinal integer NOT NULL CHECK (sort_ordinal >= 0),
    PRIMARY KEY (analysis_snapshot_id, artifact_id),
    UNIQUE (analysis_snapshot_id, sort_ordinal)
);
CREATE TABLE core.snapshot_candidate (
    analysis_snapshot_id uuid NOT NULL REFERENCES core.analysis_snapshot(analysis_snapshot_id),
    candidate_id uuid NOT NULL REFERENCES core.candidate(candidate_id),
    PRIMARY KEY (analysis_snapshot_id, candidate_id)
);
CREATE TABLE core.snapshot_review (
    analysis_snapshot_id uuid NOT NULL REFERENCES core.analysis_snapshot(analysis_snapshot_id),
    review_id uuid NOT NULL REFERENCES core.analyst_review(review_id),
    PRIMARY KEY (analysis_snapshot_id, review_id)
);
CREATE TABLE core.snapshot_assessment (
    analysis_snapshot_id uuid NOT NULL REFERENCES core.analysis_snapshot(analysis_snapshot_id),
    assessment_id uuid NOT NULL REFERENCES core.sufficiency_assessment(assessment_id),
    PRIMARY KEY (analysis_snapshot_id, assessment_id)
);
CREATE TABLE core.snapshot_finding (
    analysis_snapshot_id uuid NOT NULL REFERENCES core.analysis_snapshot(analysis_snapshot_id),
    finding_id uuid NOT NULL REFERENCES core.lifecycle_finding(finding_id),
    PRIMARY KEY (analysis_snapshot_id, finding_id)
);

-- Only FK-supporting, foreseeable lookup indexes beyond PK/unique indexes.
CREATE INDEX collection_task_run_repo_idx
    ON ingestion.collection_task(collection_run_id, repository_id);
CREATE INDEX artifact_digest_idx ON core.evidence_artifact(content_sha256);
CREATE INDEX artifact_task_idx ON core.evidence_artifact(collection_task_id)
    WHERE collection_task_id IS NOT NULL;
CREATE INDEX observation_case_repo_package_idx
    ON core.dependency_observation(case_version_id, repository_id, package_name);
CREATE INDEX candidate_case_repo_idx ON core.candidate(case_version_id, repository_id);
CREATE INDEX candidate_artifact_idx ON core.candidate(artifact_id);
CREATE INDEX review_candidate_idx ON core.analyst_review(candidate_id, review_cycle, review_sequence DESC);
CREATE INDEX finding_case_repo_category_idx
    ON core.lifecycle_finding(case_version_id, repository_id, lifecycle_category);

INSERT INTO public.schema_migrations(version, description)
VALUES (1, 'base relational foundation');
COMMIT;
