# Evidence coverage baseline

All eight frozen members appear below before aggregation. Core coverage is the planned metadata/issues/PRs/commits result; historical context is exact-ref target-package declaration, **not** installed use or adoption. A complete optional current-file probe may return verified 404 without proving historical absence.

| Case / repository | Core | Historical context | Strong pre-release paired path? | Candidates | Friction/remediation sufficiency | Key gap |
| --- | --- | --- | --- | ---: | --- | --- |
| pytest / `bsc-wdc/qdislib` | complete | unresolved | no | 0 | no/no | Missing before or insufficient in-window history. |
| pytest / `planetlabs/cosmolog` | complete | supported declaration | **yes**, `pyproject.toml` | 0 | yes/yes | Target-version resolution and downstream releases absent. |
| urllib3 / `atenreiro/opensquat` | complete | unresolved | no | 0 | no/no | Historical anchor unresolved. |
| urllib3 / `jamesturk/scrapelib` | complete | unresolved | no | 2 | no/no | Historical anchor unresolved; two copied-text candidates rejected. |
| urllib3 / `wimglenn/advent-of-code-data` | complete | **after-only** declaration | no | 0 | no/no | No pre-release paired-path context. |
| urllib3 / `Aiven-Open/pghoard` | complete | unresolved | no | 0 | no/no | Historical anchor unresolved. |
| urllib3 / `facundoolano/feedi` | complete | unresolved | no | 0 | no/no | Missing before paths. |
| urllib3 / `enzet/map-machine` | complete | unresolved | no | 0 | no/no | Historical anchor unresolved. |

By case, MET-001 is **2/2 and 6/6**, MET-002 is **1/2 and 1/6**, and the stronger pre-release paired-path count is **1/2 and 0/6** (diagnostic subcount, not a new adoption metric). Required task success is **11/11 and 27/27**. Optional not-found is **1/4 and 5/12**; those 404s are source/path observations only. `downstream_releases` is `not_collected` in all report members. `historical_dependency` coverage is partial, and ordinary target-version lockfile/runtime/CI resolution was not comprehensively acquired. A stage-required source-set mapping is not persisted as a versioned analytical field, so MET-004 is partial despite available source-class statuses.
