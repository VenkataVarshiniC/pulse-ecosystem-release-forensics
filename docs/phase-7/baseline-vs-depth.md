# Phase 7 baseline versus evidence depth

Evaluation run: `51fe08a5ea3642618d62728dc21a65d4`

Baseline: `m4-1b-published-validation`

Treatment: `p7-boundary-anchor-depth-v1`

The comparison uses the same 8 declared members, 16 member-path history records, and 40 member-question assessments. Baseline digests matched before and after evaluation.

## Historical context

| State | Baseline | Treatment | Delta |
| --- | ---: | ---: | ---: |
| `PAIRED` | 1 | 5 | +4 |
| `AFTER_ONLY` | 6 | 1 | -5 |
| `UNRESOLVED` | 9 | 10 | +1 |
| Total records | 16 | 16 | 0 |

Seven records changed state. Four changes increased exact-ref pairing: opensquat `requirements.txt`, advent-of-code-data `pyproject.toml`, pghoard `requirements.txt`, and map-machine `requirements.txt`. Three legacy `AFTER_ONLY` records became `UNRESOLVED`: both feedi paths lacked an eligible pre-release repository anchor, and scrapelib `pyproject.toml` was incomplete under the exhaustive parser contract. The aggregate pairing gain therefore does not mean every record improved.

## Findings and sufficiency

| Measure | Baseline | Treatment | Delta |
| --- | ---: | ---: | ---: |
| Eligible assessments | 40 | 40 | 0 |
| `SUFFICIENT` | 2 | 6 | +4 |
| `INSUFFICIENT` | 38 | 34 | -4 |
| `UNKNOWN` | 38 | 34 | -4 |
| Bounded NO | 2 | 6 | +4 |
| Positive supported | 0 | 0 | 0 |
| Explicit support links | 0 | 0 | 0 |

The four changes are migration-friction and remediation assessments for advent-of-code-data and map-machine. Each now has complete frozen core/review evidence plus an exact-ref pair with a pre-release target declaration. With no accepted qualifying event, the frozen contract permits bounded NO. This is an evidence-bound decision state, not proof that friction or remediation was absent in reality.

Adoption readiness and observed adoption remain `UNKNOWN` for all eight members because no resolved/installed-version source was planned. Recovery remains `UNKNOWN` because no eligible downstream recovery source or denominator was planned.

## Evidence and experimental measures

| Measure | Result | Interpretation |
| --- | ---: | --- |
| P7-M01 prerequisite coverage | 6/40 (15%) | Questions satisfying all frozen prerequisites |
| P7-M02 paired history | 5/16 (31.25%) | Exact-ref path pairs; not adoption |
| P7-M03 lifecycle sufficiency | 6/40 (15%) | Questions eligible for a bounded answer |
| P7-M04 bounded decision availability | 6/40 (15%) | Six bounded NO, zero positive |
| P7-M05 support-link completeness | Unavailable (0 positive findings) | Zero denominator is not 100% |
| P7-M06 UNKNOWN reason coverage | 34/34 (100%) | Every UNKNOWN has a controlled reason |
| P7-M07 historical method delta | 7/16 (43.75%) | Changed records, including three regressions to unresolved |
| P7-M08 provenance completeness | 48/48 (100%) | All bounded attempts have intact raw provenance |

Treatment attempt availability was 27 `AVAILABLE`, 16 `NOT_FOUND`, 2 `INCOMPLETE`, 3 `STRUCTURALLY_UNAVAILABLE`, and zero `NOT_PLANNED`, `SOURCE_UNAVAILABLE`, or `CONFLICTING`. Prerequisite availability was 22 `AVAILABLE`, 8 `NOT_FOUND`, 2 `INCOMPLETE`, and 24 `NOT_PLANNED`; other states were zero.

The 10 unresolved history records comprise 7 paths absent at both exact refs and 3 paths with an unavailable or ineligible state. The 34 UNKNOWN findings comprise 16 unresolved-version cases, 10 unmet history prerequisites, and 8 unavailable recovery-eligibility cases.

## Candidates and reviews

| Measure | Baseline | Treatment | Delta |
| --- | ---: | ---: | ---: |
| Candidate IDs | 2 | 2 | 0 |
| Accepted | 0 | 0 | 0 |
| Rejected | 2 | 2 | 0 |
| Distinct artifacts | 1 | 1 | 0 |

No detector or review input changed. Two firings remain attached to one shared artifact. `REJECT` does not establish absence of migration friction.

## Interpretation boundary

The treatment improved qualifying history and sufficiency for part of the frozen population, with no false-positive expansion and complete replay provenance. It also made three legacy optimistic history states more conservative. The result supports a bounded experimental method, not a baseline replacement, ecosystem conclusion, adoption claim, compatibility claim, or stakeholder-value claim.
