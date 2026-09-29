"""The published replay metrics must remain distinct from historical DRAFT values."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPLAY = ROOT / "data/validation/m4-1b-replay-metrics.json"
LEGACY = ROOT / "data/validation/m2-5-metric-baseline.json"
PUBLICATION = ROOT / "data/validation/m4-1b-publication-manifest.json"


def test_replay_metrics_are_case_and_snapshot_scoped() -> None:
    replay = json.loads(REPLAY.read_text(encoding="utf-8"))
    legacy = json.loads(LEGACY.read_text(encoding="utf-8"))
    publication = json.loads(PUBLICATION.read_text(encoding="utf-8"))
    assert len(replay["results"]) == 46
    assert replay["contract_version"] == "m2-5-metric-registry-v1"
    assert replay["release_id"] == publication["release_id"]
    assert publication["metric_output_sha256"] == hashlib.sha256(REPLAY.read_bytes()).hexdigest()
    assert len(set(replay["snapshot_ids"].values())) == 2
    assert not set(replay["snapshot_ids"].values()) & {
        row["analysis_snapshot_id"] for row in legacy["results"]
    }
    assert {case: snapshot["analysis_snapshot_id"]
            for case, snapshot in publication["snapshots"].items()} == replay["snapshot_ids"]
    for case in ("pytest", "urllib3"):
        scoped = [r for r in replay["results"] if r["case"] == case]
        assert len(scoped) == len({r["metric_id"] for r in scoped}) == 23
        assert {r["analysis_snapshot_id"] for r in scoped} == {replay["snapshot_ids"][case]}
    rows = {(r["case"], r["metric_id"]): r for r in replay["results"]}
    assert rows["pytest", "MET-009"]["denominator"] == 0
    assert rows["pytest", "MET-009"]["metric_value"] is None
    assert rows["pytest", "MET-009"]["status"] == "UNAVAILABLE_ZERO_DENOMINATOR"
    assert rows["urllib3", "MET-010"]["metric_value"] == "1.000000"
    for case in ("pytest", "urllib3"):
        assert rows[case, "MET-003"]["status"] == "UNAVAILABLE_EVIDENCE"
        assert rows[case, "MET-003"]["metric_value"] is None
