# Candidate equivalence and review policy

The frozen baseline has **2** candidates (both urllib3 from `jamesturk/scrapelib` PR #226); pytest has zero. The new rule-qualified replay also has **2**. Full normalized payload comparison includes case, repository, event time/type, title, artifact URL and evidence span, content SHA-256, lifecycle category, target version, classification rule/reason and confidence. Only candidate ID and review-state fields are excluded. Source origin is derived from the same preserved excerpt; both candidates explicitly contain the copied-upstream release-note marker.

| Relationship | Count | Consequence |
|---|---:|---|
| EXACT_EQUIVALENT | 2 | Inherit original review evidence with original review UUID and candidate ID; new ID is separately recorded. |
| SEMANTICALLY_EQUIVALENT | 0 | Never sufficient for automatic review inheritance. |
| CHANGED | 0 | REVIEW_REQUIRED if encountered. |
| NEW | 0 | REVIEW_REQUIRED if encountered. |
| MISSING | 0 | Blocks full comparison/release until explained. |

Both inherited decisions remain **REJECT**. The original reason/note/time/source basis are preserved, and the reuse policy is `exact-candidate-v1`. This is **inherited review evidence**, not new human review. The two detector firings share one PR artifact and one copied upstream span, so they are not independent observations or accepted friction/remediation. A changed source span, digest, stage, rule, reason, title or other normalized field fails exact equivalence in the test and receives no inherited review.

Machine candidate rows and per-review lineage are in [`replay.json`](../../../data/processed/m4-1/replay.json). `source_origin=COPIED_UPSTREAM` is a bounded span label corroborated by the original human notes; no claim is made that the PR itself is an upstream event.
