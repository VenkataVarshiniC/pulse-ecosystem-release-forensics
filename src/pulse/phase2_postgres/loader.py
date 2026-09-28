"""Transactional, source-faithful loading of the two frozen Phase 2 cases."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any
from uuid import NAMESPACE_URL, UUID, uuid4, uuid5

import psycopg
import yaml
from dotenv import dotenv_values

from pulse.phase2_postgres.manifest import ROOT, VerifiedInputs, canonical_digest

LOADER_VERSION = "phase2-postgres-loader-v1"
RULE_VERSION = "unrecorded_in_frozen_report"
HISTORY_PARSER_VERSION = "unrecorded_in_frozen_history"


def identity(kind: str, *parts: object) -> UUID:
    value = "pulse:phase2-postgres:v1:" + kind + ":" + "|".join(map(str, parts))
    return uuid5(NAMESPACE_URL, value)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def connect(database: str = "pulse_dev") -> psycopg.Connection[Any]:
    if database not in {"pulse_dev", "pulse_test"}:
        raise ValueError("Only the isolated PULSE development and test databases are supported")
    values = dotenv_values(ROOT / ".env")

    def setting(name: str) -> str:
        value = os.environ.get(name) or values.get(name)
        if not value:
            raise ValueError(f"Missing database setting: {name}")
        return value

    host, port, user = setting("PGHOST"), setting("PGPORT"), setting("PGUSER")
    if (host, port, user) != ("127.0.0.1", "55432", "pulse_local"):
        raise ValueError("M2.2 loader may connect only to the isolated local cluster")
    return psycopg.connect(
        host=host, port=port, dbname=database, user=user,
        password=setting("PGPASSWORD"), autocommit=True,
    )


def _source(
    conn: psycopg.Connection[Any], provider: str, source_type: str,
) -> UUID:
    version = "phase2-frozen-source-v1"
    source_id = identity("source", provider, source_type, version)
    conn.execute(
        """INSERT INTO ingestion.source_registry
           (source_id,provider,source_type,source_version,access_class)
           VALUES (%s,%s,%s,%s,'public') ON CONFLICT (source_id) DO NOTHING""",
        (source_id, provider, source_type, version),
    )
    row = conn.execute(
        """SELECT provider,source_type,source_version
           FROM ingestion.source_registry WHERE source_id=%s""",
        (source_id,),
    ).fetchone()
    if row != (provider, source_type, version):
        raise ValueError("Source registry identity conflict")
    return source_id


def _case_inputs(inputs: VerifiedInputs, case: str) -> dict[str, Any]:
    case_entry, case_file = inputs.one(case, "case_definition")
    definition = yaml.safe_load(case_file.read_text(encoding="utf-8"))
    report = read_json(inputs.one(case, "forensics_report")[1])
    run = read_json(inputs.one(case, "collection_manifest")[1])
    history = read_json(inputs.one(case, "history_manifest")[1])
    baseline = read_jsonl(inputs.one(case, "candidate_baseline")[1])
    baseline_manifest = read_json(inputs.one(case, "candidate_baseline_manifest")[1])
    reviews = [
        item for item in read_jsonl(inputs.one(case, "review_ledger")[1])
        if item["candidate"]["case_id"] == case
    ]
    accepted = read_jsonl(inputs.one(case, "accepted_ledger")[1])
    replay = read_json(inputs.one(case, "replay_audit")[1])
    attempts = []
    for item, path in inputs.entries(case, "collector_task_attempt"):
        attempt = read_json(path)
        if item["repository"] != attempt["task"]["repository"]:
            raise ValueError("Task journal repository differs from frozen manifest")
        attempts.append(attempt)
    if definition["case"]["case_id"] != case or report["case_id"] != case:
        raise ValueError("Frozen case/report identity mismatch")
    if run["case_id"] != case or history["case_id"] != case:
        raise ValueError("Frozen collection/history run case mismatch")
    if set(report["frozen_cohort"]) != {
        item["repository"] for item in definition["cohort"]["repositories"]
    }:
        raise ValueError("Frozen case/report cohort mismatch")
    if {a["task"]["task_id"] for a in attempts} != {
        outcome["task_id"] for outcome in run["outcomes"]
    }:
        raise ValueError("Frozen planned task/outcome/attempt mismatch")
    if len(attempts) != report["collection_task_counts"]["planned"]:
        raise ValueError("Frozen report task count mismatch")
    if {item["candidate_id"] for item in baseline} != {
        item["candidate"]["candidate_id"] for item in reviews
    }:
        raise ValueError("Frozen candidate/review identity mismatch")
    if accepted:
        raise ValueError("Accepted ledger unexpectedly nonempty in frozen cases")
    return {
        "definition": definition, "report": report, "run": run, "history": history,
        "baseline": baseline, "baseline_manifest": baseline_manifest,
        "reviews": reviews, "replay": replay, "attempts": attempts,
        "case_sha": case_entry["sha256"],
    }


def _audit_reuse(
    conn: psycopg.Connection[Any], case: str, digest: str,
) -> bool:
    key = f"phase2-frozen-case-v1:{case}"
    row = conn.execute(
        """SELECT input_digest,result FROM ingestion.load_audit
           WHERE idempotency_key=%s AND target_relation='phase2_frozen_case'
             AND result='succeeded'""",
        (key,),
    ).fetchone()
    if row is None:
        return False
    if row[0].strip() != digest:
        raise ValueError(f"Idempotency conflict for {case}: trusted source digest differs")
    if row[1] != "succeeded":
        raise ValueError("Unexpected load audit state")
    return True


def _release_case_members(
    conn: psycopg.Connection[Any], case: str, data: dict[str, Any],
    inputs: VerifiedInputs,
) -> tuple[UUID, dict[str, UUID], str, int]:
    definition = data["definition"]
    report = data["report"]
    case_info = definition["case"]
    plan_version = f"case-sha256:{data['case_sha']}"
    pypi_source = _source(conn, "pypi", "pypi_version")
    release_id = identity("release", case_info["ecosystem"], case_info["target_package"],
                          case_info["target_version"])
    conn.execute(
        """INSERT INTO core.dependency_release
           (release_id,package_ecosystem,package_name_normalized,version,
            release_time,release_source_id)
           VALUES (%s,%s,%s,%s,%s,%s)""",
        (release_id, case_info["ecosystem"], case_info["target_package"],
         case_info["target_version"], case_info["release_timestamp"], pypi_source),
    )
    case_version_id = identity("case-version", case, 1)
    conn.execute(
        """INSERT INTO core.investigation_case
           (case_version_id,case_id,case_version,case_name,target_release_id,
            window_start,window_end,source_plan_version,rule_version,status,created_at)
           VALUES (%s,%s,1,%s,%s,%s,%s,%s,%s,'DRAFT',%s)""",
        (case_version_id, identity("case", case), case, release_id,
         case_info["observation_window_start"], case_info["observation_window_end"],
         plan_version, RULE_VERSION, case_info["created_at"]),
    )
    repo_metadata: dict[str, tuple[str, UUID]] = {}
    for item, path in inputs.entries(case, "raw_capture"):
        raw = read_json(path)
        if raw["query"]["kind"] != "github_repository":
            continue
        payload = raw["payload"]
        name = payload["full_name"]
        if name in report["frozen_cohort"]:
            repo_metadata[name] = (str(payload["id"]),
                                   identity("artifact", item["root"], item["path"]))
    repositories: dict[str, UUID] = {}
    for member in definition["cohort"]["repositories"]:
        name = member["repository"]
        if name not in repo_metadata:
            raise ValueError(f"Missing verified repository metadata for {name}")
        provider_id, artifact_id = repo_metadata[name]
        repository_id = identity("repository", "github", provider_id)
        repositories[name] = repository_id
        conn.execute(
            """INSERT INTO core.repository
               (repository_id,provider,provider_repository_id,canonical_full_name,identity_status)
               VALUES (%s,'github',%s,%s,'verified')""",
            (repository_id, provider_id, name),
        )
        conn.execute(
            """INSERT INTO core.cohort_membership
               (case_version_id,repository_id,selection_method,eligibility_status,
                selection_rationale,included_at)
               VALUES (%s,%s,%s,'included',%s,%s)""",
            (case_version_id, repository_id, definition["cohort"]["selection_method"],
             member["inclusion_reason"], definition["cohort"]["created_at"]),
        )
        # Alias source link is inserted after artifacts to satisfy its FK.
        repo_metadata[name] = (provider_id, artifact_id)
    conn.execute(
        "UPDATE core.investigation_case SET status='FROZEN' WHERE case_version_id=%s",
        (case_version_id,),
    )
    if report["release_timestamp"] != case_info["release_timestamp"].replace("+00:00", "Z"):
        raise ValueError("Release timestamp differs between frozen case and report")
    return case_version_id, repositories, plan_version, 2 + 2 * len(repositories)


def _runs_tasks(
    conn: psycopg.Connection[Any], case: str, data: dict[str, Any],
    case_version_id: UUID, repositories: dict[str, UUID], plan_version: str,
) -> tuple[UUID, UUID, dict[str, UUID], int]:
    run, history = data["run"], data["history"]
    base_id = identity("run", case, run["run_id"])
    history_id = identity("run", case, history["run_id"])
    for source, run_id, kind in (
        (run, base_id, "release_collection"),
        (history, history_id, "historical_reconstruction"),
    ):
        conn.execute(
            """INSERT INTO ingestion.collection_run
               (collection_run_id,case_version_id,collector_version,started_at,
                completed_at,run_status,source_plan_version,run_kind)
               VALUES (%s,%s,%s,%s,%s,'complete',%s,%s)""",
            (run_id, case_version_id, "unrecorded_in_frozen_manifest",
             source["started_at"], source["completed_at"], plan_version, kind),
        )
    task_ids: dict[str, UUID] = {}
    for attempt in data["attempts"]:
        task, outcome = attempt["task"], attempt["outcome"]
        if attempt["run_id"] != run["run_id"] or task["case_id"] != case:
            raise ValueError("Task journal run/case mismatch")
        if attempt["capture_method"] != "collector":
            raise ValueError("Release-case task was not captured by collector")
        kind, provider = task["kind"], task["source"]
        source_id = _source(conn, provider, kind)
        task_id = identity("task", case, run["run_id"], task["task_id"])
        task_ids[task["task_id"]] = task_id
        repository = task["repository"]
        repository_id = repositories.get(repository)
        if (repository is not None and repository_id is None
                and kind not in {"github_repository", "github_releases"}):
            raise ValueError("Nonmember downstream task would change the frozen cohort")
        request = json.dumps(
            {"repository": repository, "parameters": task["parameters"]},
            sort_keys=True, separators=(",", ":"),
        )
        retry_count = attempt["stats"]["retry_count"]
        if retry_count != 0:
            raise ValueError("Frozen release-case retry count changed")
        conn.execute(
            """INSERT INTO ingestion.collection_task
               (collection_task_id,collection_run_id,case_version_id,repository_id,
                source_id,plan_task_key,task_type,required_flag,request_locator,
                attempt_count,terminal_status,started_at,completed_at,error_class)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,1,%s,%s,%s,%s)""",
            (task_id, base_id, case_version_id, repository_id, source_id,
             task["task_id"], kind, task["requirement"] == "required", request,
             outcome["status"], outcome["started_at"], outcome["completed_at"],
             attempt["failure_kind"]),
        )
        conn.execute(
            """INSERT INTO ingestion.task_attempt
               (collection_task_id,attempt_number,outcome,attempted_at,
                source_status,artifact_digest)
               VALUES (%s,1,%s,%s,%s,%s)""",
            (task_id, outcome["status"], outcome["started_at"],
             attempt["stats"]["termination"], attempt["snapshot_sha256"]),
        )
    if len(task_ids) != len(data["attempts"]):
        raise ValueError("Duplicate source task ID in frozen run")
    return base_id, history_id, task_ids, 2 + 2 * len(task_ids)


def _artifacts(
    conn: psycopg.Connection[Any], inputs: VerifiedInputs, case: str,
    repositories: dict[str, UUID], base_run_id: UUID, history_run_id: UUID,
    task_ids: dict[str, UUID], history: dict[str, Any],
) -> tuple[dict[tuple[str, str], UUID], dict[str, UUID], int]:
    del base_run_id  # Base captures attach to verified task identities.
    artifacts: dict[tuple[str, str], UUID] = {}
    pr_by_repo: dict[str, UUID] = {}
    history_events: dict[str, tuple[str | None, str | None]] = {}
    for result in history["results"]:
        for position in ("before_state", "after_state"):
            state = result.get(position)
            if state and state.get("raw_snapshot_path"):
                history_events[state["raw_snapshot_path"]] = (
                    state.get("commit_sha"), state.get("commit_timestamp")
                )
    count = 0
    roles = ("raw_capture", "historical_query_capture", "historical_file_capture")
    for role in roles:
        for item, path in inputs.entries(case, role):
            raw = read_json(path)
            if raw.get("capture_method") != "collector":
                raise ValueError("Frozen raw capture method is not collector")
            raw_key = (item["root"], item["path"])
            artifact_id = identity("artifact", *raw_key)
            artifacts[raw_key] = artifact_id
            provider = raw["source"]
            source_type = raw["query"]["kind"] if role == "raw_capture" else role
            source_id = _source(conn, provider, source_type)
            repository = item.get("repository") or raw.get("source_identifier")
            repository_id = repositories.get(repository)
            if role != "raw_capture" and repository_id is None:
                raise ValueError("Historical capture lacks declared repository identity")
            source_task = raw.get("task_id")
            collection_task_id = task_ids.get(source_task) if role == "raw_capture" else None
            if role == "raw_capture" and collection_task_id is None:
                raise ValueError("Base collector capture lacks planned task")
            history_ref, event_time = history_events.get(str(path), (None, None))
            source_locator = str(raw.get("source_identifier") or f"{item['root']}/{item['path']}")
            conn.execute(
                """INSERT INTO core.evidence_artifact
                   (artifact_id,capture_fingerprint,source_id,repository_id,
                    collection_task_id,history_run_id,artifact_type,source_locator,
                    repository_ref,source_event_time,retrieved_at,capture_method,
                    content_sha256,raw_snapshot_uri,media_type,source_task_key,
                    source_attempt_key)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'collector',%s,%s,
                           'application/json',%s,%s)""",
                (artifact_id, canonical_digest({"root": item["root"], "path": item["path"]}),
                 source_id, repository_id, collection_task_id,
                 history_run_id if role != "raw_capture" else None,
                 role, source_locator, history_ref or raw["query"].get("ref"),
                 event_time, raw["retrieved_at"], item["sha256"],
                 f"{item['root']}/{item['path']}", source_task, raw.get("attempt_id")),
            )
            count += 1
            if role == "raw_capture" and raw["query"]["kind"] == "pypi_version":
                release_id = identity(
                    "release", "pypi", raw["query"]["package"], raw["query"]["version"]
                )
                updated = conn.execute(
                    "UPDATE core.dependency_release SET release_artifact_id=%s WHERE release_id=%s",
                    (artifact_id, release_id),
                ).rowcount
                if updated != 1:
                    raise ValueError("Frozen release capture has no matching target release")
            if role == "raw_capture" and raw["query"]["kind"] == "github_repository":
                name = raw["payload"]["full_name"]
                if name in repositories:
                    conn.execute(
                        """INSERT INTO core.repository_alias
                           (alias_id,repository_id,full_name,observed_from,
                            supporting_artifact_id)
                           VALUES (%s,%s,%s,%s,%s)""",
                        (identity("repository-alias", case, name, artifact_id),
                         repositories[name], name, raw["retrieved_at"], artifact_id),
                    )
            if (role == "raw_capture" and raw["query"]["kind"] == "github_pull_requests"
                    and repository in repositories):
                for pr in raw["payload"]:
                    if pr.get("number") == 226 and repository == "jamesturk/scrapelib":
                        pr_by_repo[repository] = artifact_id
                        conn.execute(
                                """INSERT INTO core.external_evidence_reference
                                   (external_ref_id,artifact_id,provider,source_object_type,
                                    provider_object_id,object_locator,observed_at)
                                   VALUES (%s,%s,'github','pull_request',%s,%s,%s)""",
                                (identity("external-ref", case, "github-pr", pr["id"]),
                                 artifact_id, str(pr["id"]), pr["html_url"], pr["created_at"]),
                        )
    return artifacts, pr_by_repo, count


def _history_observations(
    conn: psycopg.Connection[Any], inputs: VerifiedInputs, case: str,
    case_version_id: UUID, repositories: dict[str, UUID],
    artifacts: dict[tuple[str, str], UUID], history: dict[str, Any],
    target_package: str,
) -> tuple[list[UUID], list[UUID]]:
    observations: list[UUID] = []
    pairs: list[UUID] = []
    status_map = {
        "paired": "PAIRED",
        "missing_before": "AFTER_ONLY",
        "insufficient_history": "UNRESOLVED",
        "cross_file_ambiguity": "CROSS_FILE_AMBIGUITY",
    }
    for result in history["results"]:
        pair = result["pair"]
        repository = pair["repository"]
        repository_id = repositories[repository]
        state_ids: dict[str, UUID | None] = {}
        for position in ("before", "after"):
            state = result.get(f"{position}_state")
            if state is None:
                state_ids[position] = None
                continue
            raw_path = state.get("raw_snapshot_path")
            if not raw_path:
                raise ValueError("Historical state lacks raw snapshot provenance")
            entry, _ = inputs.by_absolute_path(raw_path)
            artifact_id = artifacts[entry["root"], entry["path"]]
            state_id = identity("observation", case, repository, pair["manifest_path"],
                                position, state["commit_sha"], "path-state")
            state_ids[position] = state_id
            observations.append(state_id)
            conn.execute(
                """INSERT INTO core.dependency_observation
                   (observation_id,observation_fingerprint,case_version_id,
                    repository_id,artifact_id,observation_type,package_name,
                    repository_ref,path_ref,observation_time,historical_position,
                    parser_version,quality_status)
                   VALUES (%s,%s,%s,%s,%s,'PATH_STATE',%s,%s,%s,%s,%s,%s,%s)""",
                (state_id, canonical_digest({"observation": str(state_id)}),
                 case_version_id, repository_id, artifact_id, target_package,
                 state["commit_sha"], state["path"], state["commit_timestamp"],
                 "BEFORE_RELEASE" if position == "before" else "AFTER_RELEASE",
                 HISTORY_PARSER_VERSION, state["status"]),
            )
            for ordinal, target in enumerate(state["target_observations"]):
                if target["package"].lower() != target_package.lower():
                    raise ValueError("Non-target historical declaration in frozen result")
                declaration_id = identity("observation", case, repository,
                                          pair["manifest_path"], position,
                                          state["commit_sha"], "target", ordinal)
                observations.append(declaration_id)
                constraint = target.get("constraint")
                if constraint is None:
                    constraint = ""  # Explicit bare-package declaration, not absence.
                conn.execute(
                    """INSERT INTO core.dependency_observation
                       (observation_id,observation_fingerprint,case_version_id,
                        repository_id,artifact_id,observation_type,package_name,
                        declared_constraint,repository_ref,path_ref,observation_time,
                        historical_position,parser_version,quality_status)
                       VALUES (%s,%s,%s,%s,%s,'HISTORICAL_DECLARATION',%s,%s,
                               %s,%s,%s,%s,%s,'parsed')""",
                    (declaration_id, canonical_digest({"observation": str(declaration_id)}),
                     case_version_id, repository_id, artifact_id, target_package,
                     constraint, target["commit_reference"], target["file_path"],
                     target["observed_at"],
                     "BEFORE_RELEASE" if position == "before" else "AFTER_RELEASE",
                     HISTORY_PARSER_VERSION),
                )
        source_status = pair["status"]
        if source_status not in status_map:
            raise ValueError(f"Unsupported historical pair source status: {source_status}")
        if source_status == "missing_before" and state_ids["after"] is None:
            raise ValueError("After-only pair lacks observed after state")
        pair_id = identity("historical-pair", case, repository, pair["manifest_path"], 1)
        pairs.append(pair_id)
        conn.execute(
            """INSERT INTO core.historical_pair
               (historical_pair_id,case_version_id,repository_id,package_name,
                path_ref,before_observation_id,after_observation_id,pair_status,
                pair_version,method_version,reason)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,1,%s,%s)""",
            (pair_id, case_version_id, repository_id, target_package,
             pair["manifest_path"], state_ids["before"], state_ids["after"],
             status_map[source_status], pair["pairing_strategy"],
             f"source_status={source_status}; {pair['reason']}"),
        )
    return observations, pairs


def _candidates_reviews(
    conn: psycopg.Connection[Any], case: str, data: dict[str, Any],
    case_version_id: UUID, repositories: dict[str, UUID],
    pr_by_repo: dict[str, UUID],
) -> tuple[list[UUID], list[UUID]]:
    candidates: list[UUID] = []
    reviews: list[UUID] = []
    review_by_id = {
        row["candidate"]["candidate_id"]: row for row in data["reviews"]
    }
    for row in data["baseline"]:
        source_id = row["candidate_id"]
        repository = row["repository"].removeprefix("https://github.com/")
        if repository not in repositories:
            raise ValueError("Candidate repository outside frozen cohort")
        artifact_id = pr_by_repo.get(repository)
        if artifact_id is None:
            raise ValueError("Candidate PR lacks collector-captured artifact")
        evidence = row["evidence"][0]
        if evidence["url"] != "https://github.com/jamesturk/scrapelib/pull/226":
            raise ValueError("Unexpected frozen candidate provider reference")
        review = review_by_id[source_id]
        if review["candidate"]["status"] != "rejected":
            raise ValueError("Frozen review status changed")
        if "copied upstream" not in review["candidate"]["reviewer_note"].lower():
            raise ValueError("Copied-upstream origin not supported by review")
        candidate_id = identity("candidate", case, source_id)
        candidates.append(candidate_id)
        conn.execute(
            """INSERT INTO core.candidate
               (candidate_id,candidate_fingerprint,case_version_id,repository_id,
                artifact_id,baseline_version,candidate_rule_id,candidate_rule_version,
                lifecycle_category,source_origin,emitted_at,candidate_status,
                candidate_reason,span_ref,candidate_payload_ref)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,'COPIED_UPSTREAM',NULL,'EMITTED',
                       %s,%s,%s)""",
            (candidate_id, canonical_digest({"case": case, "candidate": source_id}),
             case_version_id, repositories[repository], artifact_id,
             data["baseline_manifest"].get("baseline_fingerprint", "unrecorded"),
             row["classification_rule"], "unrecorded_in_frozen_baseline",
             row["lifecycle_stage"], row["classification_reason"],
             "evidence[0]", evidence["url"]),
        )
        review_id = identity("review", case, source_id, 1, 1)
        reviews.append(review_id)
        conn.execute(
            """INSERT INTO core.analyst_review
               (review_id,candidate_id,review_cycle,review_sequence,
                reviewer_identity,decision,reason_code,review_note,reviewed_at)
               VALUES (%s,%s,1,1,NULL,'REJECT',%s,%s,%s)""",
            (review_id, candidate_id, review["reason_code"],
             review["candidate"]["reviewer_note"], review["candidate"]["reviewed_at"]),
        )
    return candidates, reviews


def _assessments_findings(
    conn: psycopg.Connection[Any], case: str, report: dict[str, Any],
    case_version_id: UUID, repositories: dict[str, UUID],
) -> tuple[list[UUID], list[UUID]]:
    assessments: list[UUID] = []
    findings: list[UUID] = []
    mapping = {
        "unknown_insufficient_data": "UNKNOWN",
        "no_qualifying_evidence_found": "NO_QUALIFYING_EVIDENCE_FOUND",
        "yes": "QUALIFYING_EVIDENCE",
    }
    for repo_report in report["repositories"]:
        repository = repo_report["repository"]
        repository_id = repositories[repository]
        for category, finding in repo_report["stage_findings"].items():
            source_sufficient = repo_report["stage_sufficiency"][category]
            status = "SUFFICIENT" if source_sufficient else "LEGACY_UNCLASSIFIED"
            finding_status = mapping.get(finding["state"])
            if finding_status is None:
                raise ValueError("Unknown frozen finding state")
            if finding_status == "NO_QUALIFYING_EVIDENCE_FOUND" and not source_sufficient:
                raise ValueError("Frozen bounded NO lacks source sufficiency")
            if finding_status == "QUALIFYING_EVIDENCE":
                raise ValueError("Frozen cases unexpectedly contain a positive event")
            assessment_id = identity("assessment", case, repository, category, 1)
            finding_id = identity("finding", case, repository, category, 1)
            assessments.append(assessment_id)
            findings.append(finding_id)
            conn.execute(
                """INSERT INTO core.sufficiency_assessment
                   (assessment_id,case_version_id,repository_id,lifecycle_category,
                    question_id,assessment_version,sufficiency_status,reason_code,
                    required_source_set_version,rule_version,assessed_at)
                   VALUES (%s,%s,%s,%s,%s,1,%s,%s,%s,%s,NULL)""",
                (assessment_id, case_version_id, repository_id, category, category,
                 status, f"legacy_boolean_{str(source_sufficient).lower()}",
                 "unrecorded_in_frozen_report", RULE_VERSION),
            )
            conn.execute(
                """INSERT INTO core.lifecycle_finding
                   (finding_id,case_version_id,repository_id,lifecycle_category,
                    question_id,finding_version,finding_status,
                    sufficiency_assessment_id,rule_version,reason_code,
                    confidence_level,created_at)
                   VALUES (%s,%s,%s,%s,%s,1,%s,%s,%s,%s,%s,NULL)""",
                (finding_id, case_version_id, repository_id, category, category,
                 finding_status, assessment_id, RULE_VERSION, finding["state"],
                 repo_report.get("confidence")),
            )
    if len(findings) != len(repositories) * 5:
        raise ValueError("Frozen finding category count differs from source report")
    return assessments, findings


def _replay_snapshot_audit(
    conn: psycopg.Connection[Any], inputs: VerifiedInputs, case: str,
    data: dict[str, Any], case_version_id: UUID, plan_version: str,
    runs: tuple[UUID, UUID], artifacts: dict[tuple[str, str], UUID],
    candidates: list[UUID], reviews: list[UUID], assessments: list[UUID],
    findings: list[UUID], loaded_count: int,
) -> None:
    report_item, _ = inputs.one(case, "forensics_report")
    replay_item, _ = inputs.one(case, "replay_audit")
    report_path = f"{report_item['root']}/{report_item['path']}"
    if data["replay"]["output_sha256"].get(report_item["path"]) != report_item["sha256"]:
        raise ValueError("Replay audit does not match frozen report digest")
    for attempt in data["replay"]["attempts"]:
        if attempt["matched_frozen_outputs"] is not True:
            raise ValueError("Frozen replay audit contains an unmatched attempt")
        conn.execute(
            """INSERT INTO ingestion.replay_attempt
               (case_version_id,attempt_number,matched_frozen_outputs,
                output_sha256,source_manifest_sha256)
               VALUES (%s,%s,%s,%s,%s)""",
            (case_version_id, attempt["attempt"], True,
             report_item["sha256"], replay_item["sha256"]),
        )
    snapshot_digest = canonical_digest({
        "case": case, "input_manifest_sha256": inputs.manifest["manifest_sha256"],
        "report": report_path,
    })
    snapshot_id = identity("input-snapshot", case, snapshot_digest)
    conn.execute(
        """INSERT INTO core.analysis_snapshot
           (analysis_snapshot_id,case_version_id,source_plan_version,rule_version,
            metric_definition_version,model_version,loader_version,generated_at,
            state,manifest_sha256)
           VALUES (%s,%s,%s,%s,'not_yet_modeled','postgres-core-v4',%s,now(),
                   'DRAFT',%s)""",
        (snapshot_id, case_version_id, plan_version, RULE_VERSION, LOADER_VERSION,
         snapshot_digest),
    )
    for run_id in runs:
        conn.execute(
            "INSERT INTO core.snapshot_run VALUES (%s,%s)", (snapshot_id, run_id)
        )
    for ordinal, key in enumerate(sorted(artifacts)):
        item = next(
            item for item in inputs.manifest["inputs"]
            if (item["root"], item["path"]) == key
        )
        conn.execute(
            "INSERT INTO core.snapshot_artifact VALUES (%s,%s,%s,%s)",
            (snapshot_id, artifacts[key], item["sha256"], ordinal),
        )
    for table, column, identities in (
        ("snapshot_candidate", "candidate_id", candidates),
        ("snapshot_review", "review_id", reviews),
        ("snapshot_assessment", "assessment_id", assessments),
        ("snapshot_finding", "finding_id", findings),
    ):
        for record_id in identities:
            conn.execute(
                f"INSERT INTO core.{table} (analysis_snapshot_id,{column}) VALUES (%s,%s)",
                (snapshot_id, record_id),
            )
    conn.execute(
        """INSERT INTO ingestion.load_audit
           (load_id,idempotency_key,input_digest,target_relation,loader_version,
            loaded_count,rejected_count,result)
           VALUES (%s,%s,%s,'phase2_frozen_case',%s,%s,0,'succeeded')""",
        (identity("load", case, inputs.manifest["manifest_sha256"]),
         f"phase2-frozen-case-v1:{case}", inputs.manifest["manifest_sha256"],
         LOADER_VERSION, loaded_count),
    )


def _load_case_transaction(
    conn: psycopg.Connection[Any], inputs: VerifiedInputs, case: str,
) -> str:
    """Insert one verified case atomically; reuse identical input, reject changed digest."""
    if case not in inputs.manifest["cases"]:
        raise ValueError("Case is outside the committed frozen input manifest")
    digest = inputs.manifest["manifest_sha256"]
    with conn.transaction():
        if _audit_reuse(conn, case, digest):
            # An audit row alone cannot certify that its linked rows still exist.
            from pulse.phase2_postgres.reconcile import EXPECTED, actual_case

            actual = actual_case(conn, case)
            if actual != EXPECTED[case]:
                raise ValueError("Trusted load audit exists but case rows fail reconciliation")
            return "reused"
        data = _case_inputs(inputs, case)
        case_id, repositories, plan_version, count = _release_case_members(
            conn, case, data, inputs
        )
        base_run, history_run, tasks, increment = _runs_tasks(
            conn, case, data, case_id, repositories, plan_version
        )
        count += increment
        artifacts, pr_by_repo, increment = _artifacts(
            conn, inputs, case, repositories, base_run, history_run, tasks,
            data["history"],
        )
        count += increment
        observations, pairs = _history_observations(
            conn, inputs, case, case_id, repositories, artifacts, data["history"],
            data["definition"]["case"]["target_package"],
        )
        count += len(observations) + len(pairs)
        candidates, reviews = _candidates_reviews(
            conn, case, data, case_id, repositories, pr_by_repo
        )
        count += len(candidates) + len(reviews)
        assessments, findings = _assessments_findings(
            conn, case, data["report"], case_id, repositories
        )
        count += len(assessments) + len(findings)
        _replay_snapshot_audit(
            conn, inputs, case, data, case_id, plan_version,
            (base_run, history_run), artifacts, candidates, reviews,
            assessments, findings, count,
        )
    return "loaded"


def load_case_into(
    conn: psycopg.Connection[Any], inputs: VerifiedInputs, case: str,
) -> str:
    """Load one case; retain a rejected audit after a case transaction rolls back."""
    try:
        return _load_case_transaction(conn, inputs, case)
    except Exception as error:
        if case in inputs.manifest["cases"]:
            with conn.transaction():
                conn.execute(
                    """INSERT INTO ingestion.load_audit
                       (load_id,idempotency_key,input_digest,target_relation,
                        loader_version,loaded_count,rejected_count,result,quarantine_ref)
                       VALUES (%s,%s,%s,'phase2_frozen_case',%s,0,1,'rejected',%s)""",
                    (uuid4(), f"phase2-frozen-case-v1:{case}",
                     inputs.manifest["manifest_sha256"], LOADER_VERSION,
                     type(error).__name__),
                )
        raise


def load_case(inputs: VerifiedInputs, case: str, database: str = "pulse_dev") -> str:
    with connect(database) as conn:
        return load_case_into(conn, inputs, case)
