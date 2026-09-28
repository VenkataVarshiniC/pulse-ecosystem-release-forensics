# Evidence sources attached to selected PRs

| Visible source | Base presence (D=20) | Purposive discussion examples (N=7) | Provenance reading |
| --- | ---: | ---: | --- |
| Manifest/requirements diff | 14 | 6 | PR file change; proposed downstream dependency state. |
| Lockfile diff | 6 | 1 | PR file change; regeneration method unestablished. |
| Release-note section | 10 | 5 | Bot-presented upstream context. |
| Changelog section | 9 | 1 | Bot-presented upstream context. |
| Compatibility badge/link | 16 | 7 | Bot-presented link; score not independently verified. |
| Copied upstream text | 13 | 6 | Imported context, not downstream observation. |
| Upstream issue link in copied text | 13 | 6 | Upstream issue only; no downstream issue inferred. |
| Linked downstream issue | 0 | 0 | None coded in accessible selected record. |
| Substantive downstream review comment | 1 | 1 | Human statement about local constraint/tests. |
| Test result or CI discussion coded | 0 | 1 | Only discussion case reports local test issue; not systematic CI-run audit. |
| Other automated status | 3 | 3 | Bot/status activity; no proof of passed validation. |

All 27 selected PRs exposed a dependency-file diff by eligibility, split between manifest/requirements and lockfile here. Presence categories can overlap, especially release notes/changelog/copied text, and must not be summed into a unique total. The [baseplate.py#1054](https://github.com/reddit/baseplate.py/pull/1054) review comment is downstream evidence distinct from copied mypy notes; [uvicorn#2549](https://github.com/Kludex/uvicorn/pull/2549) records a local pin decision. This supports asking whether automatic upstream context answers the local question; it does not establish that reviewers lacked needed information or that PULSE saves time.
