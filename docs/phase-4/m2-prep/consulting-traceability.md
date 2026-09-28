# Competitive finding → build/integrate → data-model boundary

This applies [M1C build-versus-integrate](../competitive-analysis/build-vs-integrate.md) and [PostgreSQL implications](../competitive-analysis/postgresql-implications.md) without claiming market uniqueness or authorization.

| Finding | Provisional decision | Data-model implication |
| --- | --- | --- |
| Dependabot/Renovate already generate and group updates | Do not build update automation | No update-bot operational tables or generic PR fact from the secondary sample |
| GitHub already owns PR/issues/commit history | Integrate source references | source registry, immutable artifact, provider object refs and exact query/ref |
| CI platforms execute checks and retain variable histories | Reference qualifying check/run evidence only | external_evidence_reference; qualified observation only with ref/environment/version |
| SCA vendors own vulnerability/risk analysis | Do not recreate scanner/risk engine | Optional provider risk reference if a case needs it, no SCA warehouse mirror |
| PyPI/deps.dev expose package/version context | Consume release metadata with provenance | dependency_release sourced identity; not downstream adoption |
| Generic portfolio dashboards exist | Narrow to declared case comparisons | membership and case-local marts, no organization inventory mart |
| PULSE gap is historical pairing and uncertainty method | Potentially build narrow evidence logic after method validation | historical_pair, sufficiency, finding/UNKNOWN, typed support chain |
| Recovery and prioritization meaning remain unvalidated | Defer | no automatic recovery/priority score or human disposition taxonomy |

External systems stay authoritative for their own objects. PULSE holds only source-linked case evidence and interpretation versions.
