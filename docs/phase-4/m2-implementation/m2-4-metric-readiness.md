# M2.4 readiness of the 23 governed metric contracts

This is a **field and evidence readiness audit**, not the final metric reporting
layer. `READY` means a snapshot-scoped numerator and denominator can be
formed for the stated frozen-evidence contract, subject to selecting a
PUBLISHED snapshot before external use. None is published yet. It does not
mean every case has a nonzero denominator or that PULSE measured real-world
adoption, recovery or stakeholder success. `PARTIAL_EVIDENCE` means the mart
can expose a bounded diagnostic but the required evidence or classification
is incomplete. `PARTIAL_PLATFORM` means source evidence exists but this M2.4
mart set does not yet implement its distinct audit grain. The table does not
change the 23 definitions in the [lineage contract](../m2-prep/metric-lineage-matrix.md).

| Metric | Required mart | Fields ready? | Evidence ready? | Status | Reason |
| --- | --- | --- | --- | --- | --- |
| MET-001 Core collection | `fct_repository_investigation`, `fct_collection_task`, member bridge | Yes | Yes, planned sources | READY | Required-task completion is bounded to the declared plan, not all possible sources. |
| MET-002 Historical context | Repository and observation facts, member bridge | Yes | Partial external history; enough for declaration coverage | READY | Exact-ref target declaration presence is measurable; broader history is not implied. |
| MET-003 Target-version evidence | Observation and repository facts | Yes, typed resolution fields | No qualified resolved/installed version | UNAVAILABLE_EVIDENCE | Three declarations are not installed-version evidence or adoption. |
| MET-004 Stage source completeness | Task and finding facts | Partial | No versioned category→required-source mapping | PARTIAL_EVIDENCE | Task availability exists, but stage completeness denominator cannot be qualified. |
| MET-005 Stage sufficiency | Finding fact | Yes, literal status | Partial: 38 legacy Boolean outcomes | PARTIAL_EVIDENCE | Two SUFFICIENT are explicit; LEGACY_UNCLASSIFIED cannot become a modern status. |
| MET-006 Investigation outcome | Repository and finding facts | Partial | Stakeholder question/completion set absent | BLOCKED_STAKEHOLDER | No approved organizational completion definition. |
| MET-007 Recovery eligibility | Repository and finding facts | Partial | No accepted event or eligible recovery set | UNAVAILABLE_EVIDENCE | UNKNOWN recovery is not failed or successful recovery. |
| MET-008 Emission coverage | Candidate fact, member bridge | Yes | Yes, frozen candidate baseline | READY | Measures detector activity among declared members only. |
| MET-009 Reviewed acceptance | Candidate fact | Yes | Yes for urllib3; pytest 0/0 | READY | urllib3 0/2; pytest rate unavailable through `NULLIF(denominator,0)`. |
| MET-010 Reviewed rejection | Candidate fact | Yes | Yes for urllib3; pytest 0/0 | READY | urllib3 2/2; pytest rate unavailable. |
| MET-011 Unresolved share | Candidate fact | Yes | Yes for urllib3; pytest 0/0 | READY | No selected unresolved candidate; zero-candidate case has no valid rate. |
| MET-012 UNKNOWN rate | Finding fact, member bridge | Yes for reported categories | Stakeholder-required question set absent | PARTIAL_EVIDENCE | Descriptive reported-category status is possible; not completion-wide rate. |
| MET-013 UNKNOWN reasons | Finding/assessment source reasons | Partial | Controlled stage-level reason partition absent | PARTIAL_EVIDENCE | Source reason text remains available; multi-label reason rate unqualified. |
| MET-014 Conflict rate | Finding/sufficiency fact | Yes, enum supports it | No complete conflict taxonomy/classification | UNAVAILABLE_EVIDENCE | Zero coded conflicts cannot be interpreted as zero actual conflicts. |
| MET-015 Missing-source contribution | Finding and task facts, source-reason links | Partial | Stage-to-required-source attribution absent | PARTIAL_EVIDENCE | Missing sources are qualitative, not a validated contribution rate. |
| MET-016 Required-task completion | Task fact | Yes | Yes, 38 required successes | READY | Plan-bound operational measure. |
| MET-017 Optional not-found | Task fact | Yes | Yes, six optional not_found outcomes | READY | Verified optional 404, not proof of historical absence. |
| MET-018 Retry incidence | Task fact | Yes | Yes, all 54 attempt journals | READY | Zero observed retries from actual attempt numbers. |
| MET-019 Resume reuse | Task fact plus future resume audit | Partial | No resumed run for either frozen release case | PARTIAL_EVIDENCE | HTTPX method evidence is outside this frozen case population. |
| MET-020 Replay success | Separate replay-audit mart | No | Four verified replay attempts exist | PARTIAL_PLATFORM | The distinct `replay_attempt` source is not transformed into these five facts. dbt reruns are not replay attempts. |
| MET-021 YES provenance | Finding fact and support bridge | Yes structurally | No YES finding or positive support chain | UNAVAILABLE_EVIDENCE | Denominator is zero; empty support bridge is correct. |
| MET-022 Candidate density | Candidate fact, member bridge | Yes | Yes, frozen baseline and members | READY | Activity per declared member, not incident prevalence. |
| MET-023 Review duration | Candidate fact | Yes, nullable emission/review clocks | Candidate emission time absent | UNAVAILABLE_EVIDENCE | PR event time cannot replace candidate availability time. |

Current matrix: **10 READY, 7 partial (six evidence and one platform), five
unavailable evidence, one stakeholder blocked**. The earlier M1A audit
reported 12 computable, five partial and six unavailable for its file-level
contract. M2.4 applies stricter *platform* and *evidence* gates: MET-005's
legacy status and MET-020's missing replay mart keep them from READY here.
These changes are classifications of implementation readiness, not revised
historical evidence. No final metric rate table or Power BI measure was built.
