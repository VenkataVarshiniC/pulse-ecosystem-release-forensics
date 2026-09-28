"""Real frozen inputs exercised only inside rolled-back pulse_test transactions."""

from __future__ import annotations

import copy
import json
import os

import pytest

from pulse.phase2_postgres import loader
from pulse.phase2_postgres.manifest import MANIFEST, canonical_digest, verify_inputs
from pulse.phase2_postgres.reconcile import reconcile


class _Rollback(Exception):
    pass


def _test_connection():
    try:
        return loader.connect("pulse_test")
    except Exception as error:
        if os.environ.get("PULSE_REQUIRE_DB_TESTS") == "1":
            pytest.fail(f"pulse_test unavailable: {error}")
        pytest.skip(f"pulse_test unavailable: {error}")


def test_verified_manifest_rejects_changed_capture(tmp_path) -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    manifest["inputs"][0]["sha256"] = "0" * 64
    manifest["manifest_sha256"] = canonical_digest({
        key: value for key, value in manifest.items() if key != "manifest_sha256"
    })
    altered = tmp_path / "altered.json"
    altered.write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(ValueError, match="hash mismatch"):
        verify_inputs(altered)


def test_frozen_load_reconciles_reuses_and_rejects_changed_digest() -> None:
    inputs = verify_inputs()
    with _test_connection() as conn:
        try:
            with conn.transaction():
                assert loader.load_case_into(conn, inputs, "pytest-8.0.0") == "loaded"
                assert loader.load_case_into(conn, inputs, "urllib3-2.0.0") == "loaded"
                assert reconcile(conn)["status"] == "PASS"
                baseline = {
                    table: conn.execute(f"SELECT count(*) FROM {table}").fetchone()[0]
                    for table in (
                        "core.investigation_case", "core.cohort_membership",
                        "ingestion.collection_task", "core.evidence_artifact",
                        "core.dependency_observation", "core.candidate",
                        "core.analyst_review", "core.lifecycle_finding",
                        "ingestion.load_audit",
                    )
                }
                for case in sorted(inputs.manifest["cases"]):
                    assert loader.load_case_into(conn, inputs, case) == "reused"
                assert all(
                    conn.execute(f"SELECT count(*) FROM {table}").fetchone()[0] == count
                    for table, count in baseline.items()
                )
                changed = copy.deepcopy(inputs.manifest)
                changed["manifest_sha256"] = "0" * 64
                changed_inputs = type(inputs)(manifest=changed, files=inputs.files)
                with pytest.raises(ValueError, match="Idempotency conflict"):
                    loader.load_case_into(conn, changed_inputs, "pytest-8.0.0")
                assert conn.execute(
                    "SELECT count(*) FROM ingestion.load_audit WHERE result='rejected'"
                ).fetchone()[0] == 1
                assert conn.execute("""SELECT trim(input_digest) FROM ingestion.load_audit
                    WHERE result='succeeded' AND idempotency_key=%s""",
                    ("phase2-frozen-case-v1:pytest-8.0.0",)
                ).fetchone()[0] == inputs.manifest["manifest_sha256"]
                assert conn.execute("""SELECT count(DISTINCT artifact_id),count(*)
                    FROM core.candidate""").fetchone() == (1, 2)
                assert conn.execute("""SELECT count(*) FROM core.lifecycle_finding
                    WHERE lifecycle_category IN ('observed_adoption','recovery_signal')
                    AND finding_status<>'UNKNOWN'""").fetchone()[0] == 0
                assert conn.execute("""SELECT count(*) FROM core.evidence_artifact
                    WHERE capture_method='fixture'""").fetchone()[0] == 0
                raise _Rollback
        except _Rollback:
            pass


def test_late_case_failure_rolls_back_all_rows(monkeypatch) -> None:
    inputs = verify_inputs()
    with _test_connection() as conn:
        def fail_after_artifacts(*_args, **_kwargs):
            raise ValueError("injected late mapping failure")

        monkeypatch.setattr(loader, "_history_observations", fail_after_artifacts)
        try:
            with conn.transaction():
                with pytest.raises(ValueError, match="injected late"):
                    loader.load_case_into(conn, inputs, "pytest-8.0.0")
                for table in (
                    "core.investigation_case", "core.cohort_membership",
                    "ingestion.collection_task", "core.evidence_artifact",
                ):
                    assert conn.execute(f"SELECT count(*) FROM {table}").fetchone()[0] == 0
                assert conn.execute("""SELECT count(*) FROM ingestion.load_audit
                    WHERE result='rejected'""").fetchone()[0] == 1
                raise _Rollback
        except _Rollback:
            pass
