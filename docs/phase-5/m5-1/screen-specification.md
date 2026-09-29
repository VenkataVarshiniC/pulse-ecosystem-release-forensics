# Proposed application screens

**PROVISIONAL — STAKEHOLDER VALIDATION PENDING** for audience, workflow value, page order and wording. These are future M5.3 screens, not built UI. All reads require an explicit case version and snapshot; current normal browsing selects the two M4.1B `PUBLISHED_VALIDATION` snapshots and never silently mixes legacy DRAFT rows. Each screen keeps a case/snapshot breadcrumb, source/version context and accessible text statuses. Loading uses a labeled skeleton without false zero counts; network/backend errors show retry and request context; missing/unauthorized resources do not masquerade as empty evidence. The [uncertainty contract](uncertainty-ux.md) applies to every screen.

## 1. Investigation List / Home

- **Question, purpose, actor:** “Which bounded release investigations can I open?” Working investigator; read-only access. Avoid impact/risk ranking.
- **Source and fields:** `core.investigation_case`, `core.dependency_release`, selected `core.analysis_snapshot`, cohort counts from `core.cohort_membership` or governed `analytics.bridge_case_repository`. Show case name, package, target version, declared member count, window, snapshot state/version and a scoped evidence-completeness summary. Do not label a DRAFT case “published.”
- **Actions, navigation, filters, drill:** Open investigation at explicit snapshot; filter by package/release and publication state. Case creation is **not** an MVP action; FR-001's human setup workflow remains provisional. Open → Overview.
- **Empty/loading/error and uncertainty:** No investigations → “No declared investigations available,” not zero impact. Loading placeholder; failed list → retry/error, not empty cohort. Summary UNKNOWN/unavailable remains labeled; no ecosystem score.
- **Acceptance and validation:** A selected case shows exactly its declared cohort/window (AC-BR-001-01, AC-SR-001-01); published replay defaults only to allowlisted IDs. Whether this list is a useful first step awaits a real investigator.

## 2. Investigation Overview

- **Question, purpose, actor:** “Which declared repositories warrant closer inspection, and what is known?” Working investigator. Operational navigation, **not** the deferred Power BI aggregate dashboard.
- **Source and fields:** `core.cohort_membership`, `analytics.bridge_case_repository`, `analytics.fct_repository_investigation`, selected task/finding summaries. Show release, cohort/window, every repository, core collection, historical declaration/pairing, candidate count, finding-state counts, evidence gap and selected snapshot/rule provenance. Do not compute organizational risk or adoption KPI.
- **Actions, navigation, filters, drill:** Select repository → Repository Investigation; open release/method context; filter only within the selected case/snapshot by repository or literal evidence state. Candidate path stays distinct from member findings.
- **Empty/loading/error and uncertainty:** Zero members is invalid case scope, not a valid 0% dashboard. A member with no candidate still appears. Loading does not imply complete collection; failed summary read gives retry; UNKNOWN and 0/0 remain visible.
- **Acceptance and validation:** Preserve 2 pytest and 6 urllib3 members, including zero-candidate members (AC-FR-001-01, AC-FR-010-01, UAT-011). Audience/priority hypotheses await stakeholder validation.

## 3. Repository Investigation

- **Question, purpose, actor:** “What evidence exists for this member, and what can PULSE conclude?” Working investigator or read-only analyst capability.
- **Source and fields:** `core.repository`, selected `core.dependency_observation`, `core.historical_pair`, `core.sufficiency_assessment`, `core.lifecycle_finding`, candidate summaries, task/source outcomes; optional governed mart summary for counts. Show identity, declaration versus resolution, exact-ref/AFTER_ONLY state, five category findings, sufficiency and source gaps, provenance and snapshot/rule context.
- **Actions, navigation, filters, drill:** Navigate to grouped Evidence Explorer, each Finding Detail, Candidate Review, and Artifact Detail. Filter categories/source type without changing the declared member denominator.
- **Empty/loading/error and uncertainty:** Repository outside cohort → scoped not-found; no observations → “No qualifying observation recorded,” with task status; network/backend failure separate. UNKNOWN remains literal and does not become a missing row or bounded NO.
- **Acceptance and validation:** After-only does not prove pre-release absence (AC-FR-004-01); current declaration does not prove target installation (AC-FR-005-01); required-source failure blocks false negative (AC-FR-006-01). The value of this combined view is provisional.

## 4. Evidence Explorer (grouped, not a forced timeline)

- **Question, purpose, actor:** “Which original observations and source captures support or limit this investigation?” Investigator/reviewer capability.
- **Source and fields:** Selected `core.evidence_artifact`, `core.dependency_observation`, `core.historical_pair`, `ingestion.collection_task`/`task_attempt` and `ingestion.source_registry` through API-checked lineage. Show source type/locator, repository, path/ref, observation type, capture method, digest, event time and retrieval time separately, task outcome, and source limitation. Do not expose credentials or full sensitive payload by default.
- **Actions, navigation, filters, drill:** Group by source/category/ref; filter source, path state, capture method and known/unknown time; select observation/artifact → Artifact Detail. Optional sort by defensible event time has “event time unavailable” group. A record appearing later is not proof of a causal sequence.
- **Empty/loading/error and uncertainty:** No selected capture, optional not-found, required failure and unavailable source have distinct messages. Loading and retrieval error must not appear as “no evidence.” Exact-ref missing anchor stays unresolved.
- **Acceptance and validation:** Original locator, capture method and digest-linked snapshot can be traced (AC-SR-002-01, AC-FR-003-01); source outcomes remain distinct (AC-NFR-004-01). Which source details users trust awaits stakeholder work.

## 5. Finding Detail

- **Question, purpose, actor:** “Why is this category UNKNOWN, bounded NO, or qualifying evidence?” Investigator/reviewer capability; read-only.
- **Source and fields:** Selected `core.lifecycle_finding` and `core.sufficiency_assessment`, `core.assessment_source_reason`, recorded support edges and rule/snapshot lineage. Show category/question, literal finding status, sufficiency, reason, required-source set/rule version, confidence basis and actual support count. The current replay has 38 UNKNOWN, two bounded NO and zero positive; do not invent a support edge for a current finding.
- **Actions, navigation, filters, drill:** Return to member, inspect source gap/observation; follow only recorded finding→artifact/observation/review links. Category selection is contextual, not stage order.
- **Empty/loading/error and uncertainty:** Missing selected finding → not-found; empty support set → “No explicit support link recorded”; failed provenance lookup → error, not unsupported “no source.” UNKNOWN and INSUFFICIENT remain distinct; no negative without SUFFICIENT prerequisite.
- **Acceptance and validation:** AC-BR-002-01, AC-FR-009-01, AC-NFR-001-01. Full accepted-finding chain is not demonstrated by the current two-case replay and must be tested with qualifying future evidence.

## 6. Candidate Review

- **Question, purpose, actor:** “What did the detector emit, and what did a human decide?” Working investigator with conditional reviewer capability.
- **Source and fields:** Selected `core.candidate`, `core.analyst_review`, `core.replay_candidate_lineage`, `core.evidence_artifact` and `core.snapshot_candidate`/`snapshot_review`. Show candidate ID, rule/version, category, source-origin span, artifact locator/digest, current decision/reason, `review_origin`, original-review link/time for inherited decisions, and selected snapshot state. Two published candidates share one copied-upstream artifact and have inherited REJECT; show **two firings, one artifact, no accepted event**.
- **Actions, navigation, filters, drill:** Open artifact and original review provenance; filter category/origin/decision. ACCEPT/REJECT/NEEDS_EVIDENCE with required reason is enabled only for an authorized human and a writable DRAFT candidate in a governed review cycle. Current PUBLISHED_VALIDATION candidates are **read-only**. A submitted decision is append-only; findings require separate reanalysis/versioning.
- **Empty/loading/error and uncertainty:** No candidates → “No candidate emitted,” not “no incident”; absent review → “Not reviewed”; NEEDS_EVIDENCE → unresolved. Stale version, duplicate terminal review, invalid reason or published target → actionable rejection without partial write. Network error never implies successful submission.
- **Acceptance and validation:** AC-SR-003-01, AC-FR-007-01, AC-FR-008-01, AC-NFR-003-01; current inherited REJECT must not look like a new reviewer click. Reviewer authority and review burden remain unvalidated.

## 7. Artifact / Provenance Detail

- **Question, purpose, actor:** “Where did this claim come from, and how was it captured?” Investigator/reviewer capability; read-only.
- **Source and fields:** `core.evidence_artifact`, `core.external_evidence_reference`, `ingestion.collection_run`/`collection_task`/`task_attempt`, `ingestion.source_registry`, and selected candidate/finding/observation links. Show original locator, source type, repository, ref/SHA/path, capture method (`collector`, `connector_assisted`, `fixture`), retrieval context/time, source event time if present, content digest, rule and linked candidate/finding IDs. Fixture and connector-assisted evidence must not be described as unattended collection.
- **Actions, navigation, filters, drill:** Return to originating candidate/finding/member; open original public locator when allowed; verify digest and exact-ref lineage. Stable IDs appear in provenance detail, not list cards.
- **Empty/loading/error and uncertainty:** No locator or failed digest/provenance check → explicit unverified state; no generic source link. Loading, authorization and backend errors are distinct. Missing event time remains unknown; retrieval time is not substituted.
- **Acceptance and validation:** AC-SR-002-01, AC-BR-003-01, AC-NFR-001-01 and AC-NFR-005-01; credential exclusion is mandatory. No current positive replay finding exists for a full accepted-chain demonstration.

Across screens, genuine stakeholder responses may revise the working actor, order, labels and completion action. They cannot silently weaken evidence integrity or convert UNKNOWN into NO.
