# Identity and version strategy

The internal UUID is a stable row handle, never a substitute for a validated business key. The loader derives repeatable IDs from a namespaced canonical key when the frozen source has one; when it does not, it allocates once and stores a source-key mapping in load audit. A retry reuses the mapping. Conflicting payload for the same canonical key is quarantined rather than overwritten.

| Concept | Identity contract |
| --- | --- |
| Case | case_id identifies the investigation family; case_version_id is a UUID for one immutable definition. Unique (case_id, case_version). Membership and window changes create a new case version. |
| Release | unique (ecosystem, normalized package name, exact version text); publication time is a sourced attribute, not part of identity. Conflicting release metadata is reviewed/versioned, not silently replaced. |
| Repository | provider + provider_repository_id when known; canonical name and aliases are labels. Name-only records remain provisional, with no silent coalescing across renames. |
| Run/task/attempt | execution UUID; task unique within run by plan_task_key; attempts numbered within task. Resume links to original run rather than reusing run ID. |
| Artifact | capture UUID plus unique immutable capture manifest identity (source, locator/query, exact ref if relevant, method, retrieval instant, digest, run/task if any). Content hash alone is not identity: two captures may share bytes. |
| Observation | observation_id stable for one artifact + parser/method version + field/path/span/type/ordinal. New parse interpretation creates a new observation/version; never overwrite source content. |
| Historical pair | pair ID and method version refer to exact before/after observation IDs or explicit missing endpoint; after-only is not a completed pre/post pair. |
| Candidate | candidate_id stable across replay of one frozen baseline, keyed by case version, baseline version, artifact, rule/version, span and firing ordinal. Artifact ID is not candidate ID. |
| Review | review_id per event, sequence per candidate/cycle; one terminal decision per cycle. A changed decision begins a new cycle and a new analytical snapshot, preserving history. |
| Assessment/finding | distinct version numbers per case/member/category/question. Latest is never chosen implicitly; snapshot manifest selects exact IDs. |
| Analysis snapshot | UUID plus unique canonical manifest SHA-256, defined in [snapshot contract](analytical-snapshot-contract.md). One published manifest maps to one ID and exact chosen input/version IDs. |

Source natural IDs, original path/ref, case ID and SHA are retained alongside surrogates for audit. A provider object ID is namespaced by provider and object type. Cross-case reused artifact rows may link into several cases via typed observations; this never changes its capture identity.
