"""Guard the generated M2.5 contract and evidence-boundary semantics."""

import hashlib
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "data/validation/m2-5-metric-baseline.json"
REGISTRY = ROOT / "analytics/metrics/metric_registry.yml"
MANIFEST = ROOT / "data/manifests/analytics-release-manifest.json"


def _results():
    return json.loads(BASELINE.read_text(encoding="utf-8"))["results"]


def test_all_contracts_have_scoped_results_and_statuses():
    spec = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    metrics = spec["metrics"]
    assert len(metrics) == 23
    assert {status: sum(m["status"] == status for m in metrics.values()) for status in {
        "READY", "PARTIAL_EVIDENCE", "PARTIAL_PLATFORM", "UNAVAILABLE_EVIDENCE",
        "BLOCKED_STAKEHOLDER",
    }} == {
        "READY": 10, "PARTIAL_EVIDENCE": 6, "PARTIAL_PLATFORM": 1,
        "UNAVAILABLE_EVIDENCE": 5, "BLOCKED_STAKEHOLDER": 1,
    }
    results = _results()
    assert len(results) == 46
    for case in ("pytest", "urllib3"):
        scoped = [r for r in results if r["case"] == case]
        assert {r["metric_id"] for r in scoped} == set(metrics)
        assert len({r["analysis_snapshot_id"] for r in scoped}) == 1
        assert all(r["snapshot_state"] == "DRAFT" for r in scoped)
        assert all(r["contract_status"] == metrics[r["metric_id"]]["status"] for r in scoped)


def test_zero_denominator_and_positive_zero_are_distinct():
    rows = {(r["case"], r["metric_id"]): r for r in _results()}
    pytest_accept = rows["pytest", "MET-009"]
    urllib_accept = rows["urllib3", "MET-009"]
    assert (pytest_accept["numerator"], pytest_accept["denominator"]) == (0, 0)
    assert pytest_accept["metric_value"] is None
    assert pytest_accept["status"] == "UNAVAILABLE_ZERO_DENOMINATOR"
    assert "ZERO_DENOMINATOR" in pytest_accept["unavailable_reason"]
    assert (urllib_accept["numerator"], urllib_accept["denominator"]) == (0, 2)
    assert urllib_accept["metric_value"] == "0.000000"
    assert urllib_accept["unavailable_reason"] is None


def test_golden_denominators_and_non_ready_withholding():
    rows = {(r["case"], r["metric_id"]): r for r in _results()}
    for case, members, history, emitters, candidates in (
        ("pytest", 2, 1, 0, 0), ("urllib3", 6, 1, 1, 2)
    ):
        assert (rows[case, "MET-001"]["numerator"],
                rows[case, "MET-001"]["denominator"]) == (members, members)
        assert (rows[case, "MET-002"]["numerator"],
                rows[case, "MET-002"]["denominator"]) == (history, members)
        assert (rows[case, "MET-008"]["numerator"],
                rows[case, "MET-008"]["denominator"]) == (emitters, members)
        assert (rows[case, "MET-022"]["numerator"],
                rows[case, "MET-022"]["denominator"]) == (candidates, members)
        for metric_id in ("MET-003", "MET-007", "MET-014", "MET-021", "MET-023"):
            assert rows[case, metric_id]["metric_value"] is None
            assert rows[case, metric_id]["numerator"] is None
        assert rows[case, "MET-006"]["status"] == "BLOCKED_STAKEHOLDER"
        assert rows[case, "MET-012"]["metric_value"] is None


def test_manifest_holds_draft_and_binds_generated_evidence():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["publication_decision"] == "HOLD_DRAFT"
    assert manifest["power_bi_gate"] == "BLOCKED_NO_PUBLISHED_SNAPSHOT"
    assert {s["state"] for s in manifest["snapshots"]} == {"DRAFT"}
    assert "UNRESOLVED" in manifest["rule_version"]
    assert manifest["metric_baseline_sha256"] == hashlib.sha256(BASELINE.read_bytes()).hexdigest()
    assert manifest["metric_registry_sha256"] == hashlib.sha256(REGISTRY.read_bytes()).hexdigest()
