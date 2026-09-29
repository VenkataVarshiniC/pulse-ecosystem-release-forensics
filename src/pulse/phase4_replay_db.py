"""Load the pinned M4.1 replay as two case-scoped analytical snapshots."""

from __future__ import annotations

import hashlib
import json
from typing import Any
from uuid import UUID

import psycopg

from pulse.detector_evaluation import load_verified_baseline
from pulse.phase2_postgres.loader import connect, identity
from pulse.phase2_postgres.manifest import ROOT, canonical_digest, sha256, verify_inputs
from pulse.phase4_replay import read_rule_manifest

REPLAY = ROOT / "data/processed/m4-1/replay.json"
REPLAY_SHA = "b3be08da423c5c988be9151178b0da137a6d5bd1aedd300afbfc2c825cc48f13"
RULE_SHA = "b9f09c03b5e72aa44cbb334e71261b4c72c966e899c0e9b962ddb97d1d858896"
RULE_RELEASE = "rule-replay-b2b638bb97c8-e10fb03f467e267f"
INPUT_SHA = "09d66f72862cfaa1a664cb1fc5c42a5b8fe28dbaeb35bd7f42364bdbff50a743"
METRIC_VERSION = "m2-5-metric-registry-v1"
LOADER_VERSION = "m4-1b-governed-replay-v1"
CASES = ("pytest-8.0.0", "urllib3-2.0.0")


def model_digest() -> str:
    """Pin the dbt project, models and macros independently of checkout EOLs."""
    root = ROOT / "analytics/dbt"
    files = sorted([
        *root.glob("models/**/*.sql"), *root.glob("models/**/*.yml"),
        *root.glob("macros/**/*.sql"), root / "dbt_project.yml",
    ])
    digest = hashlib.sha256()
    for path in files:
        digest.update(path.relative_to(root).as_posix().encode())
        digest.update(b"\0")
        digest.update(path.read_bytes().replace(b"\r\n", b"\n"))
        digest.update(b"\0")
    return digest.hexdigest()


def verified_replay() -> tuple[dict[str, Any], Any, dict[str, Any]]:
    if sha256(REPLAY) != REPLAY_SHA:
        raise ValueError("Committed replay artifact SHA-256 changed")
    inputs = verify_inputs()
    if len(inputs.files) != 142 or inputs.manifest["manifest_sha256"] != INPUT_SHA:
        raise ValueError("Frozen 142-file input manifest changed")
    rule = read_rule_manifest()
    if rule["manifest_sha256"] != RULE_SHA or rule["rule_release_id"] != RULE_RELEASE:
        raise ValueError("Replay rule manifest/version changed")
    replay = json.loads(REPLAY.read_text(encoding="utf-8"))
    if (replay["input_manifest_sha256"], replay["rule_manifest_sha256"],
            replay["rule_release_id"]) != (INPUT_SHA, RULE_SHA, RULE_RELEASE):
        raise ValueError("Replay artifact lineage changed")
    if set(replay["cases"]) != set(CASES):
        raise ValueError("Replay case population changed")
    for case, result in replay["cases"].items():
        if result["report"] is None or result["missing_legacy_candidate_ids"]:
            raise ValueError(f"Replay case {case} lacks complete qualified findings")
        if len(result["candidates"]) != len(result["review_provenance"]):
            raise ValueError("Replay candidate/review equivalence is incomplete")
        if any(c["equivalence"] != "EXACT_EQUIVALENT" for c in result["candidates"]):
            raise ValueError("Replay contains a candidate requiring fresh review")
    return replay, inputs, rule


def release_identity(model_sha: str, metric_sha: str, source_commit: str) -> str:
    return "m4-1b-" + canonical_digest({
        "replay_sha256": REPLAY_SHA, "rule_manifest_sha256": RULE_SHA,
        "model_sha256": model_sha, "metric_registry_sha256": metric_sha,
        "source_commit": source_commit,
    })[:20]


def snapshot_manifest(
    case: str, original_snapshot_id: UUID, release_id: str,
    model_sha: str, metric_sha: str, source_commit: str,
) -> dict[str, Any]:
    body = {
        "case_id": case,
        "release_id": release_id,
        "original_snapshot_id": str(original_snapshot_id),
        "input_manifest_sha256": INPUT_SHA,
        "replay_artifact_sha256": REPLAY_SHA,
        "rule_manifest_sha256": RULE_SHA,
        "rule_release_id": RULE_RELEASE,
        "metric_contract_version": METRIC_VERSION,
        "metric_registry_sha256": metric_sha,
        "mart_model_version": f"m4-1b-{model_sha[:16]}",
        "mart_model_sha256": model_sha,
        "source_git_commit": source_commit,
    }
    return {**body, "manifest_sha256": canonical_digest(body)}


def _legacy_snapshot(conn: psycopg.Connection[Any], case: str) -> tuple[UUID, UUID, str]:
    case_id = identity("case-version", case, 1)
    rows = conn.execute(
        """SELECT analysis_snapshot_id,case_version_id,source_plan_version
           FROM core.analysis_snapshot WHERE case_version_id=%s
             AND rule_version='unrecorded_in_frozen_report' AND state='DRAFT'""",
        (case_id,),
    ).fetchall()
    if len(rows) != 1:
        raise ValueError("Expected one unchanged historical DRAFT snapshot for case")
    return rows[0]


def _member_ids(conn: psycopg.Connection[Any], case_id: UUID) -> dict[str, UUID]:
    rows = conn.execute(
        """SELECT r.canonical_full_name,r.repository_id
           FROM core.cohort_membership m JOIN core.repository r USING(repository_id)
           WHERE m.case_version_id=%s""",
        (case_id,),
    )
    return dict(rows)


def _load_candidate(
    conn: psycopg.Connection[Any], case: str, snapshot_id: UUID,
    case_id: UUID, repositories: dict[str, UUID], candidate: dict[str, Any],
    provenance: dict[str, Any], baseline_by_id: dict[str, Any],
) -> None:
    source_id = candidate["candidate_id"]
    old_source_id = candidate["legacy_candidate_id"]
    if provenance["replay_candidate_id"] != source_id or (
        provenance["original_candidate_id"] != old_source_id
        or provenance["original_review_decision"] != "rejected"
        or provenance["reuse_policy"] != "exact-candidate-v1"
    ):
        raise ValueError("Inherited review provenance mismatch")
    original = baseline_by_id[old_source_id]
    if (original.evidence[0].content_sha256 != candidate["artifact_digest"]
            or original.classification_rule != candidate["rule_id"]
            or original.lifecycle_stage.value != candidate["lifecycle_category"]
            or str(original.evidence[0].url) != candidate["artifact"]):
        raise ValueError("Replay candidate differs from verified frozen baseline")
    repository = candidate["repository"].removeprefix("https://github.com/")
    if repository not in repositories:
        raise ValueError("Replay candidate repository outside frozen cohort")
    old_id = identity("candidate", case, old_source_id)
    old_review_id = UUID(provenance["original_review_id"])
    old = conn.execute(
        """SELECT c.artifact_id,c.repository_id,c.case_version_id,c.candidate_rule_id,
                  c.lifecycle_category,c.source_origin,c.candidate_payload_ref,
                  r.review_id,r.decision,r.reason_code,r.review_note,r.reviewed_at
           FROM core.candidate c JOIN core.analyst_review r ON c.candidate_id=r.candidate_id
           WHERE c.candidate_id=%s AND r.review_id=%s""",
        (old_id, old_review_id),
    ).fetchone()
    if old is None or (
        old[1] != repositories[repository] or old[2] != case_id
        or old[3] != candidate["rule_id"] or old[4] != candidate["lifecycle_category"]
        or old[5] != candidate["source_origin"] or old[6] != candidate["artifact"]
        or old[8] != "REJECT"
    ):
        raise ValueError("Historical candidate/review database lineage differs")
    new_id = identity("m4-1b-candidate", source_id)
    new_review_id = identity("m4-1b-inherited-review", source_id)
    conn.execute(
        """INSERT INTO core.candidate
           (candidate_id,candidate_fingerprint,case_version_id,repository_id,artifact_id,
            baseline_version,candidate_rule_id,candidate_rule_version,lifecycle_category,
            source_origin,emitted_at,candidate_status,candidate_reason,span_ref,
            candidate_payload_ref)
           VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NULL,'EMITTED',%s,%s,%s)""",
        (new_id, candidate["normalized_candidate_fingerprint"], case_id,
         repositories[repository], old[0], REPLAY_SHA, candidate["rule_id"],
         RULE_RELEASE, candidate["lifecycle_category"], candidate["source_origin"],
         candidate["emitted_reason"], "evidence[0]", source_id),
    )
    conn.execute(
        """INSERT INTO core.analyst_review
           (review_id,candidate_id,review_cycle,review_sequence,reviewer_identity,
            decision,reason_code,review_note,reviewed_at,review_origin,
            inherited_from_review_id)
           VALUES (%s,%s,1,1,NULL,'REJECT',%s,%s,%s,'INHERITED',%s)""",
        (new_review_id, new_id, old[9], old[10], old[11], old_review_id),
    )
    conn.execute(
        """INSERT INTO core.replay_candidate_lineage
           (candidate_id,analysis_snapshot_id,replay_candidate_source_id,
            original_candidate_id,original_review_id,replay_review_id,
            normalized_fingerprint,evidence_content_sha256,equivalence,
            equivalence_basis,reuse_policy)
           VALUES (%s,%s,%s,%s,%s,%s,%s,%s,'EXACT_EQUIVALENT',%s,%s)""",
        (new_id, snapshot_id, source_id, old_id, old_review_id, new_review_id,
         candidate["normalized_candidate_fingerprint"], candidate["artifact_digest"],
         provenance["equivalence_basis"], provenance["reuse_policy"]),
    )
    conn.execute("INSERT INTO core.snapshot_candidate VALUES (%s,%s)", (snapshot_id, new_id))
    conn.execute("INSERT INTO core.snapshot_review VALUES (%s,%s)", (snapshot_id, new_review_id))


def _load_findings(
    conn: psycopg.Connection[Any], case: str, snapshot_id: UUID,
    case_id: UUID, repositories: dict[str, UUID], report: dict[str, Any],
) -> None:
    states = {
        "unknown_insufficient_data": "UNKNOWN",
        "no_qualifying_evidence_found": "NO_QUALIFYING_EVIDENCE_FOUND",
        "yes": "QUALIFYING_EVIDENCE",
    }
    if set(r["repository"] for r in report["repositories"]) != set(repositories):
        raise ValueError("Replay report member population changed")
    for member in report["repositories"]:
        repository = member["repository"]
        for stage, sufficient in member["stage_sufficiency"].items():
            finding = member["stage_findings"][stage]
            status = states[finding["state"]]
            if status == "NO_QUALIFYING_EVIDENCE_FOUND" and not sufficient:
                raise ValueError("Replay bounded NO lacks sufficiency")
            if status == "QUALIFYING_EVIDENCE":
                raise ValueError("Unexpected positive replay finding needs explicit support load")
            assessment_id = identity("m4-1b-assessment", case, repository, stage)
            finding_id = identity("m4-1b-finding", case, repository, stage)
            conn.execute(
                """INSERT INTO core.sufficiency_assessment
                   (assessment_id,case_version_id,repository_id,lifecycle_category,
                    question_id,assessment_version,sufficiency_status,reason_code,
                    required_source_set_version,rule_version,assessed_at)
                   VALUES (%s,%s,%s,%s,%s,2,%s,%s,%s,%s,NULL)""",
                (assessment_id, case_id, repositories[repository], stage, stage,
                 "SUFFICIENT" if sufficient else "INSUFFICIENT",
                 "replay_stage_sufficient" if sufficient else "replay_stage_insufficient",
                 RULE_RELEASE, RULE_RELEASE),
            )
            conn.execute(
                """INSERT INTO core.lifecycle_finding
                   (finding_id,case_version_id,repository_id,lifecycle_category,
                    question_id,finding_version,finding_status,sufficiency_assessment_id,
                    rule_version,reason_code,confidence_level,created_at)
                   VALUES (%s,%s,%s,%s,%s,2,%s,%s,%s,%s,%s,NULL)""",
                (finding_id, case_id, repositories[repository], stage, stage,
                 status, assessment_id, RULE_RELEASE, finding["state"], member["confidence"]),
            )
            conn.execute("INSERT INTO core.snapshot_assessment VALUES (%s,%s)",
                         (snapshot_id, assessment_id))
            conn.execute("INSERT INTO core.snapshot_finding VALUES (%s,%s)",
                         (snapshot_id, finding_id))


def _existing_snapshot_valid(
    conn: psycopg.Connection[Any], snapshot_id: UUID,
    manifest: dict[str, Any], result: dict[str, Any],
) -> bool:
    row = conn.execute(
        """SELECT s.manifest_sha256,s.rule_version,s.metric_definition_version,
                  s.model_version,l.replay_artifact_sha256,l.rule_manifest_sha256,
                  (SELECT count(*) FROM core.snapshot_candidate x
                   WHERE x.analysis_snapshot_id=s.analysis_snapshot_id),
                  (SELECT count(*) FROM core.snapshot_review x
                   WHERE x.analysis_snapshot_id=s.analysis_snapshot_id),
                  (SELECT count(*) FROM core.snapshot_assessment x
                   WHERE x.analysis_snapshot_id=s.analysis_snapshot_id),
                  (SELECT count(*) FROM core.snapshot_finding x
                   WHERE x.analysis_snapshot_id=s.analysis_snapshot_id)
           FROM core.analysis_snapshot s JOIN core.replay_snapshot_lineage l
             USING(analysis_snapshot_id) WHERE s.analysis_snapshot_id=%s""",
        (snapshot_id,),
    ).fetchone()
    if row is None:
        return False
    expected = (
        manifest["manifest_sha256"], RULE_RELEASE, METRIC_VERSION,
        manifest["mart_model_version"], REPLAY_SHA, RULE_SHA,
        result["replay_candidate_count"], len(result["review_provenance"]),
        len(result["report"]["repositories"]) * 5,
        len(result["report"]["repositories"]) * 5,
    )
    if tuple(str(x).strip() if isinstance(x, str) else x for x in row) != expected:
        raise ValueError("Existing replay snapshot differs from declared manifest/rows")
    return True


def load_replay_into(
    conn: psycopg.Connection[Any], replay: dict[str, Any], inputs: Any,
    source_commit: str, model_sha: str, metric_sha: str,
) -> dict[str, str]:
    release_id = release_identity(model_sha, metric_sha, source_commit)
    result_ids = {}
    with conn.transaction():
        for case in CASES:
            result = replay["cases"][case]
            original_snapshot, case_id, plan_version = _legacy_snapshot(conn, case)
            manifest = snapshot_manifest(
                case, original_snapshot, release_id, model_sha, metric_sha, source_commit
            )
            snapshot_id = identity("m4-1b-snapshot", case, manifest["manifest_sha256"])
            result_ids[case] = str(snapshot_id)
            if _existing_snapshot_valid(conn, snapshot_id, manifest, result):
                continue
            if conn.execute(
                "SELECT 1 FROM core.analysis_snapshot WHERE manifest_sha256=%s",
                (manifest["manifest_sha256"],),
            ).fetchone():
                raise ValueError("Replay manifest identity collides with another snapshot")
            repositories = _member_ids(conn, case_id)
            if set(repositories) != set(result["report"]["frozen_cohort"]):
                raise ValueError("Replay cohort differs from governed case membership")
            conn.execute(
                """INSERT INTO core.analysis_snapshot
                   (analysis_snapshot_id,case_version_id,source_plan_version,rule_version,
                    metric_definition_version,model_version,loader_version,generated_at,
                    state,manifest_sha256)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,now(),'DRAFT',%s)""",
                (snapshot_id, case_id, plan_version, RULE_RELEASE, METRIC_VERSION,
                 manifest["mart_model_version"], LOADER_VERSION, manifest["manifest_sha256"]),
            )
            conn.execute(
                """INSERT INTO core.replay_snapshot_lineage
                   (analysis_snapshot_id,replay_artifact_sha256,input_manifest_sha256,
                    rule_manifest_sha256,rule_release_id,source_git_commit,
                    metric_contract_version,metric_registry_sha256,mart_model_version,
                    mart_model_sha256,release_id,case_id)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (snapshot_id, REPLAY_SHA, INPUT_SHA, RULE_SHA, RULE_RELEASE, source_commit,
                 METRIC_VERSION, metric_sha, manifest["mart_model_version"], model_sha,
                 release_id, case),
            )
            for table, columns in (
                ("snapshot_run", "collection_run_id"),
                ("snapshot_artifact", "artifact_id,expected_sha256,sort_ordinal"),
            ):
                conn.execute(
                    f"INSERT INTO core.{table} (analysis_snapshot_id,{columns}) "
                    f"SELECT %s,{columns} FROM core.{table} WHERE analysis_snapshot_id=%s",
                    (snapshot_id, original_snapshot),
                )
            baseline = load_verified_baseline(
                inputs.one(case, "candidate_baseline")[1],
                inputs.one(case, "candidate_baseline_manifest")[1],
            )
            baseline_by_id = {row.candidate_id: row for row in baseline}
            provenance = {r["replay_candidate_id"]: r for r in result["review_provenance"]}
            for candidate in result["candidates"]:
                _load_candidate(conn, case, snapshot_id, case_id, repositories,
                                candidate, provenance[candidate["candidate_id"]], baseline_by_id)
            _load_findings(conn, case, snapshot_id, case_id, repositories, result["report"])
            conn.execute(
                """INSERT INTO ingestion.load_audit
                   (load_id,idempotency_key,input_digest,target_relation,loader_version,
                    loaded_count,rejected_count,result)
                   VALUES (%s,%s,%s,'m4_1b_replay_snapshot',%s,%s,0,'succeeded')""",
                (identity("m4-1b-load", case, manifest["manifest_sha256"]),
                 f"m4-1b:{case}:{release_id}", manifest["manifest_sha256"],
                 LOADER_VERSION, len(result["candidates"]) * 2
                 + len(result["report"]["repositories"]) * 10 + 1),
            )
    return result_ids


def load_replay(database: str = "pulse_dev", *, source_commit: str) -> dict[str, str]:
    replay, inputs, _ = verified_replay()
    metric_sha = sha256(ROOT / "analytics/metrics/metric_registry.yml")
    model_sha = model_digest()
    with connect(database) as conn:
        return load_replay_into(conn, replay, inputs, source_commit, model_sha, metric_sha)
