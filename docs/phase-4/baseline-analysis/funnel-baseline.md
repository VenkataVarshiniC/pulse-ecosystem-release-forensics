# Investigation pathway baseline

These are **evidence/process counts**, not a consumer funnel, user abandonment, or impact incidence. [Milestone 1 funnel](../investigation-funnel.md) has a declared-member spine and an optional candidate branch with **different grains**. No-candidate members remain in the investigation.

| Stage / grain | pytest 8.0.0 | urllib3 2.0.0 | Interpretation |
| --- | ---: | ---: | --- |
| F0 declared members | 2 | 6 | Frozen denominators; all remain. |
| F1 core planned-source complete / member | 2/2 | 6/6 | Operational source coverage only. |
| F2 exact-ref declaration context / member | 1/2 | 1/6 | One pytest paired pre-release path; urllib3 one after-only path. Not adoption. |
| F3 sufficient for migration-friction category / member-stage | 1/2 | 0/6 | Current bounded method only. Remediation has same counts. Other three categories 0/2 and 0/6. |
| B1 candidate emitted / distinct member; candidate count | 0/2; 0 | 1/6; 2 | Candidate branch optional. |
| B2 terminally reviewed / candidate | 0/0 (unavailable rate) | 2/2 | No review backlog among emitted urllib3 candidates. |
| B3 accepted / terminally reviewed candidate | 0/0 (unavailable rate) | 0/2 | Two rejected firings from one PR; no qualifying event. |
| F4 bounded friction output / member-stage | 1/2 | 0/6 | pytest's one result is `NO_QUALIFYING_EVIDENCE_FOUND`, not no real-world friction. |
| F5 repository outcome coverage | Unavailable | Unavailable | Required completion-question set is stakeholder-dependent (MET-006). |

The apparent F1→F2 decline is an **historical evidence gap**, not a failure by users or proof that non-covered repositories lacked the dependency. B1 is neither required for F3/F4 nor desirable in itself. The two B3 rejections cannot be transformed into NO unless independent stage sufficiency allows a bounded negative. No cross-case rate is pooled.
