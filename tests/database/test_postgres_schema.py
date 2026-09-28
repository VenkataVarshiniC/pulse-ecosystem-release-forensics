"""Transactional, test-only PostgreSQL integrity probes.

All inserted rows use capture_method=fixture and are rolled back. They are never
loaded into PULSE's frozen evidence or analytical metrics.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

import pytest
from dotenv import dotenv_values

ROOT = Path(__file__).resolve().parents[2]


def uid(number: int) -> str:
    return f"00000000-0000-0000-0000-{number:012d}"


SOURCE = uid(1)
RELEASE = uid(2)
REPOSITORY = uid(3)
CASE_VERSION = uid(4)
CASE = uid(5)
ARTIFACT = uid(6)
ASSESSMENT = uid(7)
FINDING = uid(8)
CANDIDATE = uid(9)
REVIEW = uid(10)
SNAPSHOT = uid(11)
OBSERVATION = uid(12)

BASE = f"""
INSERT INTO ingestion.source_registry
  (source_id, provider, source_type, source_version, access_class)
VALUES ('{SOURCE}', 'fixture', 'unit_test', 'v1', 'public');
INSERT INTO core.dependency_release
  (release_id, package_ecosystem, package_name_normalized, version,
   release_time, release_source_id)
VALUES ('{RELEASE}', 'pypi', 'fixture-package', '1.0',
        '2026-01-01T00:00:00Z', '{SOURCE}');
INSERT INTO core.repository
  (repository_id, provider, provider_repository_id, canonical_full_name, identity_status)
VALUES ('{REPOSITORY}', 'fixture', 'repo-1', 'example/repo', 'verified');
INSERT INTO core.investigation_case
  (case_version_id, case_id, case_version, case_name, target_release_id,
   window_start, window_end, source_plan_version, rule_version, status)
VALUES ('{CASE_VERSION}', '{CASE}', 1, 'fixture case', '{RELEASE}',
        '2025-12-01T00:00:00Z', '2026-02-01T00:00:00Z', 'plan-1', 'rule-1', 'DRAFT');
INSERT INTO core.cohort_membership
  (case_version_id, repository_id, selection_method, eligibility_status, included_at)
VALUES ('{CASE_VERSION}', '{REPOSITORY}', 'fixture', 'included', '2025-12-01T00:00:00Z');
INSERT INTO core.evidence_artifact
  (artifact_id, capture_fingerprint, source_id, repository_id, artifact_type,
   source_locator, retrieved_at, capture_method, content_sha256,
   raw_snapshot_uri, media_type)
VALUES ('{ARTIFACT}', repeat('a', 64), '{SOURCE}', '{REPOSITORY}', 'fixture',
        'fixture://source/one', '2026-01-02T00:00:00Z', 'fixture', repeat('b', 64),
        'fixture://raw/one', 'application/json');
"""

CANDIDATE_SQL = f"""
INSERT INTO core.candidate
  (candidate_id, candidate_fingerprint, case_version_id, repository_id,
   artifact_id, baseline_version, candidate_rule_id, candidate_rule_version,
   lifecycle_category, source_origin, candidate_status, candidate_reason, span_ref)
VALUES ('{CANDIDATE}', repeat('c', 64), '{CASE_VERSION}', '{REPOSITORY}',
        '{ARTIFACT}', 'baseline-1', 'rule-1', 'v1', 'friction',
        'LOCAL_DOWNSTREAM', 'EMITTED', 'fixture only', 'span:1');
"""

ASSESSMENT_SQL = f"""
INSERT INTO core.sufficiency_assessment
  (assessment_id, case_version_id, repository_id, lifecycle_category, question_id,
   assessment_version, sufficiency_status, reason_code, required_source_set_version,
   rule_version, assessed_at)
VALUES ('{ASSESSMENT}', '{CASE_VERSION}', '{REPOSITORY}', 'friction', 'q1',
        1, 'SUFFICIENT', 'qualified_fixture', 'source-set-1', 'rule-1',
        '2026-01-03T00:00:00Z');
"""


@pytest.fixture(scope="module")
def pg() -> tuple[str, dict[str, str]]:
    config = dotenv_values(ROOT / ".env")
    default_psql = Path("C:/Program Files/PostgreSQL/16/bin/psql.exe")
    executable = os.environ.get("PULSE_PSQL") or shutil.which("psql") or str(default_psql)
    reason = "PostgreSQL test environment is not configured"
    if not config.get("PGPASSWORD") or not Path(executable).exists():
        if os.environ.get("PULSE_REQUIRE_DB_TESTS") == "1":
            pytest.fail(reason)
        pytest.skip(reason)
    env = os.environ.copy()
    env.update({key: str(value) for key, value in config.items() if value is not None})
    env["PGDATABASE"] = "pulse_test"
    probe = subprocess.run(
        [executable, "-X", "-w", "-At", "-c", "SELECT current_database()"],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    if probe.returncode != 0 or probe.stdout.strip() != "pulse_test":
        if os.environ.get("PULSE_REQUIRE_DB_TESTS") == "1":
            pytest.fail("pulse_test is unavailable; run db.ps1 start and reset")
        pytest.skip("pulse_test unavailable; run db.ps1 start and reset")
    return executable, env


def execute(pg: tuple[str, dict[str, str]], sql: str, *, valid: bool = True) -> str:
    executable, env = pg
    result = subprocess.run(
        [executable, "-X", "-w", "-qAt", "-v", "ON_ERROR_STOP=1", "-c", sql],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    if valid:
        assert result.returncode == 0, result.stderr
    else:
        assert result.returncode != 0, "Expected constraint rejection"
    return result.stdout if valid else result.stderr


def in_transaction(pg: tuple[str, dict[str, str]], sql: str, *, valid: bool = True) -> str:
    return execute(pg, f"BEGIN; {BASE} {sql} ROLLBACK;", valid=valid)


def test_revision_and_schemas(pg: tuple[str, dict[str, str]]) -> None:
    output = execute(
        pg,
        "SELECT version FROM public.schema_migrations; "
        "SELECT schema_name FROM information_schema.schemata "
        "WHERE schema_name IN ('ingestion','core') ORDER BY schema_name;",
    )
    assert output.splitlines() == ["1", "2", "3", "4", "core", "ingestion"]


def test_local_authentication_settings(pg: tuple[str, dict[str, str]]) -> None:
    output = execute(pg, "SHOW listen_addresses; SHOW password_encryption;")
    assert output.splitlines() == ["127.0.0.1", "scram-sha-256"]


def test_duplicate_case_version_rejected(pg: tuple[str, dict[str, str]]) -> None:
    in_transaction(
        pg,
        f"INSERT INTO core.investigation_case "
        f"(case_version_id,case_id,case_version,case_name,target_release_id,"
        f"window_start,window_end,source_plan_version,rule_version,status) VALUES "
        f"('{uid(100)}','{CASE}',1,'duplicate','{RELEASE}',now(),now(),'p','r','DRAFT');",
        valid=False,
    )


def test_duplicate_membership_rejected(pg: tuple[str, dict[str, str]]) -> None:
    in_transaction(
        pg,
        f"INSERT INTO core.cohort_membership "
        f"(case_version_id,repository_id,selection_method,eligibility_status,included_at) "
        f"VALUES ('{CASE_VERSION}','{REPOSITORY}','fixture','included',now());",
        valid=False,
    )


def test_frozen_case_cannot_mutate(pg: tuple[str, dict[str, str]]) -> None:
    in_transaction(
        pg,
        f"UPDATE core.investigation_case SET status='FROZEN' "
        f"WHERE case_version_id='{CASE_VERSION}'; "
        f"UPDATE core.investigation_case SET case_name='changed' "
        f"WHERE case_version_id='{CASE_VERSION}';",
        valid=False,
    )


def test_frozen_membership_cannot_disappear(pg: tuple[str, dict[str, str]]) -> None:
    in_transaction(
        pg,
        f"UPDATE core.investigation_case SET status='FROZEN' "
        f"WHERE case_version_id='{CASE_VERSION}'; "
        f"DELETE FROM core.cohort_membership WHERE case_version_id='{CASE_VERSION}';",
        valid=False,
    )


def test_membership_cannot_move_into_frozen_case(pg: tuple[str, dict[str, str]]) -> None:
    error = in_transaction(
        pg,
        f"INSERT INTO core.repository "
        f"(repository_id,provider,provider_repository_id,canonical_full_name,identity_status) "
        f"VALUES ('{uid(109)}','fixture','repo-2','example/repo-2','verified'); "
        f"INSERT INTO core.investigation_case "
        f"(case_version_id,case_id,case_version,case_name,target_release_id,"
        f"window_start,window_end,source_plan_version,rule_version,status) VALUES "
        f"('{uid(110)}','{uid(111)}',1,'other','{RELEASE}',now(),now(),'p','r','DRAFT'); "
        f"INSERT INTO core.cohort_membership "
        f"(case_version_id,repository_id,selection_method,eligibility_status,included_at) "
        f"VALUES ('{uid(110)}','{uid(109)}','fixture','included',now()); "
        f"UPDATE core.investigation_case SET status='FROZEN' "
        f"WHERE case_version_id='{CASE_VERSION}'; "
        f"UPDATE core.cohort_membership SET case_version_id='{CASE_VERSION}' "
        f"WHERE repository_id='{uid(109)}';",
        valid=False,
    )
    assert "cannot move membership into frozen case" in error


def test_identical_hash_distinct_capture_allowed(pg: tuple[str, dict[str, str]]) -> None:
    output = in_transaction(
        pg,
        f"INSERT INTO core.evidence_artifact "
        f"(artifact_id,capture_fingerprint,source_id,repository_id,artifact_type,"
        f"source_locator,retrieved_at,capture_method,content_sha256,raw_snapshot_uri,media_type) "
        f"VALUES ('{uid(101)}',repeat('d',64),'{SOURCE}','{REPOSITORY}','fixture',"
        f"'fixture://source/two',now(),'fixture',repeat('b',64),'fixture://raw/two',"
        f"'application/json'); "
        f"SELECT count(*) FROM core.evidence_artifact WHERE content_sha256=repeat('b',64);",
    )
    assert "2" in output.splitlines()


def test_invalid_hash_rejected(pg: tuple[str, dict[str, str]]) -> None:
    in_transaction(
        pg,
        f"INSERT INTO core.evidence_artifact "
        f"(artifact_id,capture_fingerprint,source_id,artifact_type,source_locator,"
        f"retrieved_at,capture_method,content_sha256,raw_snapshot_uri,media_type) "
        f"VALUES ('{uid(102)}',repeat('d',64),'{SOURCE}','fixture','fixture://x',"
        f"now(),'fixture','bad','fixture://raw/x','text/plain');",
        valid=False,
    )


def test_collector_capture_requires_task(pg: tuple[str, dict[str, str]]) -> None:
    in_transaction(
        pg,
        f"INSERT INTO core.evidence_artifact "
        f"(artifact_id,capture_fingerprint,source_id,artifact_type,source_locator,"
        f"retrieved_at,capture_method,content_sha256,raw_snapshot_uri,media_type) "
        f"VALUES ('{uid(103)}',repeat('d',64),'{SOURCE}','fixture','fixture://x',"
        f"now(),'collector',repeat('e',64),'fixture://raw/x','text/plain');",
        valid=False,
    )


def test_two_candidates_one_artifact(pg: tuple[str, dict[str, str]]) -> None:
    output = in_transaction(
        pg,
        CANDIDATE_SQL
        + f"INSERT INTO core.candidate "
        f"(candidate_id,candidate_fingerprint,case_version_id,repository_id,"
        f"artifact_id,baseline_version,candidate_rule_id,candidate_rule_version,"
        f"lifecycle_category,source_origin,candidate_status,candidate_reason,span_ref) "
        f"VALUES ('{uid(104)}',repeat('d',64),'{CASE_VERSION}','{REPOSITORY}',"
        f"'{ARTIFACT}','baseline-1','rule-2','v1','friction',"
        f"'COPIED_UPSTREAM','EMITTED','fixture only','span:2'); "
        f"SELECT count(*),count(DISTINCT artifact_id) FROM core.candidate;",
    )
    assert "2|1" in output


def test_dangling_candidate_artifact_rejected(pg: tuple[str, dict[str, str]]) -> None:
    in_transaction(
        pg,
        CANDIDATE_SQL.replace(f"'{ARTIFACT}'", f"'{uid(999)}'"),
        valid=False,
    )


def test_candidate_cannot_cite_other_repository_artifact(pg: tuple[str, dict[str, str]]) -> None:
    in_transaction(
        pg,
        f"INSERT INTO core.repository "
        f"(repository_id,provider,provider_repository_id,canonical_full_name,identity_status) "
        f"VALUES ('{uid(109)}','fixture','repo-2','example/repo-2','verified'); "
        f"INSERT INTO core.cohort_membership "
        f"(case_version_id,repository_id,selection_method,eligibility_status,included_at) "
        f"VALUES ('{CASE_VERSION}','{uid(109)}','fixture','included',now()); "
        + CANDIDATE_SQL.replace(f"'{REPOSITORY}'", f"'{uid(109)}'"),
        valid=False,
    )


def test_needs_evidence_is_not_reject(pg: tuple[str, dict[str, str]]) -> None:
    output = in_transaction(
        pg,
        CANDIDATE_SQL
        + f"INSERT INTO core.analyst_review "
        f"(review_id,candidate_id,review_cycle,review_sequence,decision,reason_code,reviewed_at) "
        f"VALUES ('{REVIEW}','{CANDIDATE}',1,1,'NEEDS_EVIDENCE','fixture',now()); "
        f"SELECT decision FROM core.analyst_review WHERE review_id='{REVIEW}';",
    )
    assert "NEEDS_EVIDENCE" in output.splitlines()


def test_duplicate_terminal_review_rejected(pg: tuple[str, dict[str, str]]) -> None:
    in_transaction(
        pg,
        CANDIDATE_SQL
        + f"INSERT INTO core.analyst_review "
        f"(review_id,candidate_id,review_cycle,review_sequence,decision,reason_code,reviewed_at) "
        f"VALUES ('{REVIEW}','{CANDIDATE}',1,1,'ACCEPT','fixture',now()); "
        f"INSERT INTO core.analyst_review "
        f"(review_id,candidate_id,review_cycle,review_sequence,decision,reason_code,reviewed_at) "
        f"VALUES ('{uid(105)}','{CANDIDATE}',1,2,'REJECT','fixture',now());",
        valid=False,
    )


def test_unknown_distinct_from_bounded_no(pg: tuple[str, dict[str, str]]) -> None:
    output = in_transaction(
        pg,
        ASSESSMENT_SQL
        + f"INSERT INTO core.lifecycle_finding "
        f"(finding_id,case_version_id,repository_id,lifecycle_category,question_id,"
        f"finding_version,finding_status,sufficiency_assessment_id,rule_version,"
        f"reason_code,created_at) VALUES "
        f"('{FINDING}','{CASE_VERSION}','{REPOSITORY}','friction','q1',1,'UNKNOWN',"
        f"'{ASSESSMENT}','rule-1','fixture',now()),"
        f"('{uid(106)}','{CASE_VERSION}','{REPOSITORY}','friction','q1',2,"
        f"'NO_QUALIFYING_EVIDENCE_FOUND','{ASSESSMENT}','rule-1','fixture',now()); "
        f"SELECT count(DISTINCT finding_status) FROM core.lifecycle_finding;",
    )
    assert "2" in output.splitlines()


def test_finding_assessment_question_must_match(pg: tuple[str, dict[str, str]]) -> None:
    in_transaction(
        pg,
        ASSESSMENT_SQL
        + f"INSERT INTO core.lifecycle_finding "
        f"(finding_id,case_version_id,repository_id,lifecycle_category,question_id,"
        f"finding_version,finding_status,sufficiency_assessment_id,rule_version,"
        f"reason_code,created_at) VALUES "
        f"('{FINDING}','{CASE_VERSION}','{REPOSITORY}','friction','different-question',"
        f"1,'UNKNOWN','{ASSESSMENT}','rule-1','fixture',now());",
        valid=False,
    )


def test_after_only_pair_is_not_paired(pg: tuple[str, dict[str, str]]) -> None:
    observation = f"""
    INSERT INTO core.dependency_observation
      (observation_id,observation_fingerprint,case_version_id,repository_id,artifact_id,observation_type,
       package_name,declared_constraint,repository_ref,path_ref,
       historical_position,parser_version,quality_status)
    VALUES ('{OBSERVATION}',repeat('1',64),'{CASE_VERSION}','{REPOSITORY}','{ARTIFACT}',
            'HISTORICAL_DECLARATION','fixture-package','>=1','ref-after',
            'requirements.txt','AFTER_RELEASE','parser-1','verified');
    """
    output = in_transaction(
        pg,
        observation
        + f"INSERT INTO core.historical_pair "
        f"(historical_pair_id,case_version_id,repository_id,package_name,path_ref,"
        f"after_observation_id,pair_status,pair_version,method_version,reason) "
        f"VALUES ('{uid(107)}','{CASE_VERSION}','{REPOSITORY}','fixture-package',"
        f"'requirements.txt','{OBSERVATION}','AFTER_ONLY',1,'method-1','no before'); "
        f"SELECT pair_status FROM core.historical_pair;",
    )
    assert "AFTER_ONLY" in output.splitlines()


def test_declaration_resolution_types_not_collapsed(pg: tuple[str, dict[str, str]]) -> None:
    in_transaction(
        pg,
        f"INSERT INTO core.dependency_observation "
        f"(observation_id,observation_fingerprint,case_version_id,repository_id,artifact_id,observation_type,"
        f"package_name,declared_constraint,resolved_version,parser_version,quality_status) "
        f"VALUES ('{OBSERVATION}',repeat('1',64),'{CASE_VERSION}','{REPOSITORY}','{ARTIFACT}',"
        f"'CURRENT_DECLARATION','fixture-package','>=1','1.0','parser-1','verified');",
        valid=False,
    )


def test_snapshot_fingerprint_unique(pg: tuple[str, dict[str, str]]) -> None:
    in_transaction(
        pg,
        f"INSERT INTO core.analysis_snapshot "
        f"(analysis_snapshot_id,case_version_id,source_plan_version,rule_version,"
        f"metric_definition_version,model_version,loader_version,generated_at,"
        f"state,manifest_sha256) VALUES "
        f"('{SNAPSHOT}','{CASE_VERSION}','p1','r1','m1','d1','l1',now(),'DRAFT',repeat('f',64)),"
        f"('{uid(108)}','{CASE_VERSION}','p1','r1','m1','d1','l1',now(),'DRAFT',repeat('f',64));",
        valid=False,
    )


def test_positive_finding_support_chain_fixture(pg: tuple[str, dict[str, str]]) -> None:
    output = in_transaction(
        pg,
        CANDIDATE_SQL
        + f"INSERT INTO core.analyst_review "
        f"(review_id,candidate_id,review_cycle,review_sequence,decision,reason_code,reviewed_at) "
        f"VALUES ('{REVIEW}','{CANDIDATE}',1,1,'ACCEPT','qualified_fixture',now()); "
        + ASSESSMENT_SQL
        + f"INSERT INTO core.lifecycle_finding "
        f"(finding_id,case_version_id,repository_id,lifecycle_category,question_id,"
        f"finding_version,finding_status,sufficiency_assessment_id,rule_version,"
        f"reason_code,created_at) VALUES "
        f"('{FINDING}','{CASE_VERSION}','{REPOSITORY}','friction','q1',1,"
        f"'QUALIFYING_EVIDENCE','{ASSESSMENT}','rule-1','qualified_fixture',now()); "
        f"INSERT INTO core.finding_artifact_support VALUES "
        f"('{FINDING}','{ARTIFACT}','original_source'); "
        f"INSERT INTO core.finding_review_support VALUES "
        f"('{FINDING}','{REVIEW}','accepted_candidate'); "
        f"SELECT f.finding_status,r.decision,a.capture_method "
        f"FROM core.lifecycle_finding f "
        f"JOIN core.finding_review_support fr USING (finding_id) "
        f"JOIN core.analyst_review r USING (review_id) "
        f"JOIN core.finding_artifact_support fa USING (finding_id) "
        f"JOIN core.evidence_artifact a USING (artifact_id) "
        f"WHERE f.finding_id='{FINDING}';",
    )
    assert "QUALIFYING_EVIDENCE|ACCEPT|fixture" in output


def test_fixture_rows_rolled_back(pg: tuple[str, dict[str, str]]) -> None:
    output = execute(
        pg,
        "SELECT (SELECT count(*) FROM core.evidence_artifact),"
        "(SELECT count(*) FROM core.candidate),"
        "(SELECT count(*) FROM core.lifecycle_finding);",
    )
    assert output.strip() == "0|0|0"
