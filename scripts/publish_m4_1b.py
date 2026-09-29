"""Publish only fully reconciled replay snapshots as immutable validation releases."""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime

from psycopg import sql
from reconcile_m4_1b import MARTS, reconcile
from run_m4_1b_metric_pack import OUTPUT, canonical_bytes, replay_metrics

from pulse.phase2_postgres.loader import connect
from pulse.phase2_postgres.manifest import ROOT, canonical_digest, sha256
from pulse.phase4_replay_db import INPUT_SHA, REPLAY_SHA, RULE_RELEASE, RULE_SHA, model_digest

MANIFEST = ROOT / "data/validation/m4-1b-publication-manifest.json"
DBT_RESULT = ROOT / "analytics/dbt/target/run_results.json"


def _digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"))
                          .encode("utf-8")).hexdigest()


def mart_fingerprints(conn, snapshot_id: str) -> dict[str, list[str]]:
    result = {}
    for mart in MARTS:
        query = sql.SQL(
            "SELECT (to_jsonb(m) - 'snapshot_state')::text FROM analytics.{} m "
            "WHERE analysis_snapshot_id=%s"
        ).format(sql.Identifier(mart))
        result[mart] = sorted(
            hashlib.sha256(row[0].encode("utf-8")).hexdigest()
            for row in conn.execute(query, (snapshot_id,))
        )
    return result


def dbt_result() -> dict:
    payload = json.loads(DBT_RESULT.read_text(encoding="utf-8"))
    statuses = {"model": 0, "test": 0}
    for item in payload["results"]:
        kind = item["unique_id"].split(".", 1)[0]
        if kind not in statuses or item["status"] != ("pass" if kind == "test" else "success"):
            raise ValueError(f"dbt build was not fully successful: {item['unique_id']}")
        statuses[kind] += 1
    if statuses["model"] != 30 or statuses["test"] < 173:
        raise ValueError(f"dbt build inventory changed: {statuses}")
    return {"version": payload["metadata"]["dbt_version"], "counts": statuses}


def _payload(conn, published_at: str) -> tuple[dict, dict]:
    checks = reconcile(conn)
    dbt = dbt_result()
    replay = replay_metrics(conn)
    ids = checks["snapshot_ids"]
    lineages = conn.execute(
        """SELECT s.analysis_snapshot_id,s.manifest_sha256,l.source_git_commit,
                  l.mart_model_sha256,l.metric_registry_sha256,l.release_id
           FROM core.replay_snapshot_lineage l
           JOIN core.analysis_snapshot s USING(analysis_snapshot_id)
           ORDER BY l.case_id"""
    ).fetchall()
    commits = {r[2].strip() for r in lineages}
    if len(commits) != 1 or {r[3].strip() for r in lineages} != {model_digest()}:
        raise ValueError("Source commit/model hash mismatch across replay snapshots")
    metric_sha = sha256(OUTPUT)
    snapshots = {}
    records = {}
    for case, snapshot_id in ids.items():
        lineage = next(r for r in lineages if str(r[0]) == snapshot_id)
        metrics = [r for r in replay["results"] if r["analysis_snapshot_id"] == snapshot_id]
        if len(metrics) != 23:
            raise ValueError("Publication requires 23 metrics per snapshot")
        mart_rows = mart_fingerprints(conn, snapshot_id)
        metric_fingerprint = _digest(metrics)
        mart_fingerprint = _digest(mart_rows)
        publication_fingerprint = canonical_digest({
            "snapshot_id": snapshot_id,
            "snapshot_manifest_sha256": lineage[1].strip(),
            "metric_output_sha256": metric_fingerprint,
            "mart_output_sha256": mart_fingerprint,
        })
        snapshots[case] = {
            "analysis_snapshot_id": snapshot_id,
            "snapshot_manifest_sha256": lineage[1].strip(),
            "metric_output_sha256": metric_fingerprint,
            "mart_output_sha256": mart_fingerprint,
            "publication_fingerprint": publication_fingerprint,
            "analytical_row_fingerprints": mart_rows,
        }
        records[snapshot_id] = (metric_fingerprint, mart_fingerprint,
                                publication_fingerprint, metrics, mart_rows)
    body = {
        "release_id": replay["release_id"],
        "publication_state": "PUBLISHED_VALIDATION",
        "published_at": published_at,
        "input_manifest_sha256": INPUT_SHA,
        "replay_artifact_sha256": REPLAY_SHA,
        "rule_release_id": RULE_RELEASE,
        "rule_manifest_sha256": RULE_SHA,
        "metric_contract_version": replay["contract_version"],
        "metric_registry_sha256": replay["registry_sha256"],
        "metric_output_sha256": metric_sha,
        "mart_model_version": "m4-1b-" + model_digest()[:16],
        "mart_model_sha256": model_digest(),
        "dbt_version": dbt["version"],
        "dbt_result_counts": dbt["counts"],
        "source_git_commit": next(iter(commits)),
        "snapshots": snapshots,
        "limitations": [
            "Validation release is limited to two frozen cases and eight declared members.",
            "Inherited REJECT decisions are original reviews, not new reviewer actions.",
            "UNKNOWN does not mean zero adoption or recovery.",
            "Stakeholder validation and ecosystem representativeness remain unproven.",
            "PUBLISHED_VALIDATION is controlled analytical availability, not product approval.",
        ],
    }
    return {**body, "manifest_sha256": canonical_digest(body)}, records


def _validate_existing(conn) -> dict:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    expected, records = _payload(conn, manifest["published_at"])
    if manifest != expected or canonical_bytes(manifest) != MANIFEST.read_bytes():
        raise ValueError("Published release manifest differs from current governed outputs")
    for snapshot_id, (metric_sha, mart_sha, fingerprint, metrics, rows) in records.items():
        record = conn.execute(
            """SELECT s.state,s.publication_manifest_sha256,s.publication_fingerprint,
                      p.metric_output_sha256,p.mart_output_sha256,p.metric_output,
                      p.mart_row_fingerprints
               FROM core.analysis_snapshot s JOIN core.publication_record p
               USING(analysis_snapshot_id) WHERE s.analysis_snapshot_id=%s""",
            (snapshot_id,),
        ).fetchone()
        if record is None or record[0] != "PUBLISHED_VALIDATION" or (
            record[1].strip(), record[2].strip(), record[3].strip(), record[4].strip(),
            record[5], record[6]
        ) != (manifest["manifest_sha256"], fingerprint, metric_sha, mart_sha,
              metrics, rows):
            raise ValueError("Immutable publication database record differs")
    return manifest


def main() -> int:
    with connect("pulse_dev") as conn:
        states = [r[0] for r in conn.execute(
            """SELECT s.state FROM core.replay_snapshot_lineage l
               JOIN core.analysis_snapshot s USING(analysis_snapshot_id)"""
        )]
        if states == ["PUBLISHED_VALIDATION"] * 2:
            manifest = _validate_existing(conn)
            print(f"PASS: existing immutable release {manifest['manifest_sha256']}")
            return 0
        if states != ["DRAFT"] * 2 or MANIFEST.exists():
            raise ValueError(
                "Replay publication requires exactly two DRAFT snapshots and no manifest"
            )
        published_at = datetime.now(UTC).isoformat(timespec="microseconds")
        manifest, records = _payload(conn, published_at)
        MANIFEST.write_bytes(canonical_bytes(manifest))
        try:
            with conn.transaction():
                for snapshot_id, values in records.items():
                    metric_sha, mart_sha, fingerprint, metrics, rows = values
                    conn.execute(
                        """INSERT INTO core.publication_record
                           (analysis_snapshot_id,publication_manifest_sha256,
                            publication_fingerprint,metric_output_sha256,mart_output_sha256,
                            metric_output,mart_row_fingerprints,published_at)
                           VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
                        (snapshot_id, manifest["manifest_sha256"], fingerprint,
                         metric_sha, mart_sha, json.dumps(metrics), json.dumps(rows), published_at),
                    )
                    conn.execute(
                        """UPDATE core.analysis_snapshot SET state='PUBLISHED_VALIDATION',
                                  publication_manifest_sha256=%s,publication_fingerprint=%s,
                                  published_at=%s WHERE analysis_snapshot_id=%s
                                  AND state='DRAFT'""",
                        (manifest["manifest_sha256"], fingerprint, published_at, snapshot_id),
                    )
        except Exception:
            MANIFEST.unlink()
            raise
    print(f"PASS: published validation release {manifest['manifest_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
