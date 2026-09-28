# Future ingestion, idempotency and quarantine contract

No loader is implemented here. The immutable raw snapshot is the evidence source; structured rows are interpretations. An operator supplies a declared case version, frozen source plan and raw manifest. Loader refuses paths outside authorized roots and stores no credentials in evidence. Captures from collector, connector_assisted and fixture retain their actual method. Only verified collector task outcomes count as unattended collection; a connector-assisted snapshot may inform explicitly labeled validation, and fixture data is test-only.

## Dependency-safe load order

1. Verify raw manifest locator, expected digest, capture method, source event/retrieval distinction and access permission. Record a load attempt even on failure.
2. Register source definitions, then release and repository identities/aliases; reconcile conflicting natural keys before using them.
3. Register immutable case definition version and frozen membership, then run, planned tasks and attempt journal. Run points to case version. A verified optional not_found records task outcome without an artifact.
4. Register artifact metadata and external provider references; hash bytes again. A collector artifact links to its task, while connector-assisted/fixture artifacts carry explicit no-task provenance and are excluded from collector success.
5. Parse typed observations and historical pairs; validate exact ref/path, source event time and method version.
6. Load immutable candidate baseline, review events, sufficiency assessments and reason/source edges, findings and typed evidence-support edges.
7. Build the versioned snapshot manifest. Run constraints, dbt checks and golden reconciliation; publish only on success.

Task-to-artifact is one-to-many or zero; no task.artifact_id pointer is needed. Load audit captures input ID/digest, target relation, loader version, idempotency key, loaded/rejected counts, timestamp, result and quarantine locator. An explicit mapping file resolves IDs absent from frozen Phase 2 artifacts; it is versioned and hash-verified.

## Idempotency

Use an immutable key per entity: source provider/type/version; release ecosystem/package/version; repository provider/stable ID; case ID/version; membership case-version/repository; run execution ID; task run/plan_task_key; attempt task/number; artifact capture-manifest fingerprint (including locator/ref/method/retrieval/digest); observation artifact/parser/type/path/span/ordinal; historical pair case/member/path/method/version; candidate frozen-baseline canonical firing key; review candidate/cycle/sequence; assessment and finding scoped version keys; snapshot manifest fingerprint. A repeated key with identical digest and canonical attributes is verified no-op. Same key with different content is a conflict, never an update. A fresh capture of identical bytes gets a distinct capture key if its retrieval context differs. Failed load attempts can repeat; only one successful result per idempotency key/target is permitted.

## Failure classes and response

| Condition | Response |
| --- | --- |
| Raw file missing, hash mismatch, unsupported capture method, secret in payload metadata | Reject/quarantine entire affected artifact, preserve audit; block dependent snapshot. |
| Invalid repository identity, duplicate conflicting business key, case/member mismatch | Quarantine identity set; block downstream rows rather than guess alias. |
| Malformed timestamp, enum, ref/path or declaration/resolution type | Quarantine parsed record; retain raw snapshot; source/question becomes incomplete or unavailable, not NO. |
| Dangling candidate/review/finding edge, duplicate terminal review, YES without provenance | Reject affected structured rows; block affected finding and mart publication. |
| Required task failure or missing planned task | Preserve failed state, include member in denominator, publish UNKNOWN where method requires it; required collection metric fails its numerator. |
| Verified optional not_found | Record successful probe outcome and warning/context; never infer historical absence. |
| Unavailable future source or absent eligible denominator | Keep metric unavailable with reason; do not synthesize zero. |

Quarantine records retain source locator, digest, issue code, loader version and audit ID, but avoid duplicating full sensitive payloads. Warnings may accompany a published snapshot only when the affected metric's declared prerequisites are still met; all publication blockers are explicit.
