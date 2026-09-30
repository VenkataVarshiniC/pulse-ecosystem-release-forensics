# M5.4 live frontend captures

These PNGs were captured on 2026-09-30 from the local React app at `127.0.0.1:5173`, backed by live FastAPI at `127.0.0.1:8000` and the governed PostgreSQL published validation rows. They contain no mocked frontend responses, credentials or browser debug overlays. Captures 01–08 and 10 used headless Chrome at laptop/desktop sizes; 09 used the Codex in-app browser with an explicit **390 CSS-pixel** viewport. The narrow capture was checked against `innerWidth=390` and `documentElement.scrollWidth=375`; a preliminary Chrome crop was discarded. Localized timestamps reflect the browser's configured locale and do not change the underlying source/event semantics.

| File | Screen / point illustrated |
| --- | --- |
| [01-investigations.png](01-investigations.png) | Two published investigations, release and cohort context |
| [02-overview-pytest.png](02-overview-pytest.png) | Declared pytest members, including a zero-candidate member |
| [03-repository-cosmolog.png](03-repository-cosmolog.png) | Repository declaration, history and findings |
| [04-evidence-qdislib.png](04-evidence-qdislib.png) | Scoped evidence explorer and separate clocks |
| [05-finding-unknown.png](05-finding-unknown.png) | UNKNOWN and incomplete evidence, not negative evidence |
| [06-candidate-inherited.png](06-candidate-inherited.png) | Inherited REJECT and shared-artifact context |
| [07-artifact-provenance.png](07-artifact-provenance.png) | Source/method/digest/task and event/retrieval context |
| [08-finding-bounded-no.png](08-finding-bounded-no.png) | Method-bounded NO with sufficient evidence |
| [09-narrow-repository.png](09-narrow-repository.png) | True 390px repository layout after mobile QA |
| [10-invalid-snapshot.png](10-invalid-snapshot.png) | Explicit scoped error for invalid snapshot |

To reproduce, start the documented local stack, open the listed page type from `/investigations`, retain its `snapshot_id` query parameter, and capture the real rendered viewport. The stable snapshot IDs are pytest `08852d5f-9843-5406-a69b-7039ea2ddaa4` and urllib3 `bd3a02a5-0c2d-5eec-84fd-8e9b93a238a3`. Do not treat these images as stakeholder acceptance or evidence of unattended external collection.
