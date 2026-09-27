"""Freeze deterministic PR IDs from the screened Milestone 1A candidate frame.

This research helper ranks IDs only; it never reads PR bodies, outcomes, or comments.
Run from the repository root: python docs/phase-3/secondary-research/select_pr_sample.py
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

FRAME = Path(__file__).with_name("github-pr-candidate-frame.json")
QUOTAS = {"base": (7, 7, 6), "discussion": (4, 3, 3)}


def digest(kind: str, key: str) -> str:
    value = f"p3-m1a-v1:{kind}:{key}".encode()
    return hashlib.sha256(value).hexdigest()


def main() -> None:
    data = json.loads(FRAME.read_text(encoding="utf-8"))
    records = data["candidates"]
    if len(records) != data["unique_candidate_count"]:
        raise ValueError("Candidate count changed before selection")

    for record in records:
        if not any(frame.startswith("discussion") for frame in record["frame_membership"]):
            record["human_interaction_screen_count"] = None
        for kind in QUOTAS:
            record[f"{kind}_sha256_digest"] = digest(kind, record["key"])
            record[f"{kind}_sha256_rank"] = None
        record["sample_type"] = None
        record["selection_note"] = None

    selected: set[str] = set()
    counts: dict[str, list[int]] = {"base": [], "discussion": []}
    for kind, quotas in QUOTAS.items():
        for slice_index, quota in enumerate(quotas):
            members = sorted(
                (
                    item
                    for item in records
                    if item["inclusion_decision"] == "eligible"
                    and f"{kind}{slice_index}" in item["frame_membership"]
                ),
                key=lambda item: (item[f"{kind}_sha256_digest"], item["key"]),
            )
            for rank, item in enumerate(members, start=1):
                item[f"{kind}_sha256_rank"] = rank
            chosen = 0
            for item in members:
                if chosen == quota:
                    break
                if item["key"] in selected:
                    continue
                if kind == "discussion" and not item["human_interaction_screen_count"]:
                    continue
                item["sample_type"] = kind
                rank = item[f"{kind}_sha256_rank"]
                item["selection_note"] = f"{kind}{slice_index} sha256 rank {rank}"
                selected.add(item["key"])
                chosen += 1
            counts[kind].append(chosen)

    data["selection"] = {
        "method": "p3-m1a-v1 SHA-256, slice quotas, base before discussion",
        "base_per_slice": counts["base"],
        "discussion_per_slice": counts["discussion"],
        "base_selected_ids": [r["key"] for r in records if r["sample_type"] == "base"],
        "discussion_selected_ids": [r["key"] for r in records if r["sample_type"] == "discussion"],
        "selected_ids_frozen_before_qualitative_coding": True,
    }
    FRAME.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(data["selection"], indent=2))


if __name__ == "__main__":
    main()
