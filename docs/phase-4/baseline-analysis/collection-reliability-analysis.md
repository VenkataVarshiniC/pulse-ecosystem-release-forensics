# Collection reliability baseline

The [frozen task audit](frozen-task-audit.json) validates one preserved collector attempt per planned task against each Phase 2 run manifest, including `collector` capture method and raw snapshot hash when an artifact exists. This is an operational audit, not evidence that all relevant public incidents were discovered.

| Case | Planned | Required succeeded | Optional succeeded | Optional verified 404 | Required failures | Tasks with retries | Operational status |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| pytest | 15 | 11/11 | 3/4 | 1/4 | 0 | 0/15 | complete |
| urllib3 | 39 | 27/27 | 7/12 | 5/12 | 0 | 0/39 | complete |

The optional 404s complete the planned probes but do not assert file absence at past refs. `MET-018 = 0/15` and `0/39` is a valid **observed retry-incidence** result because all 54 preserved attempt statistics have retry counts; it does not predict future reliability. The separate HTTPX Milestone 1 smoke/resume run has 11 eligible terminal tasks and **11/11 verified reuse with zero new requests**, with reuse links to prior attempt IDs. This supports MET-019 method feasibility, but **neither frozen release case has a resume run**, so no pytest/urllib3 resume percentage is reported.

The existing Phase 2 reproducer was executed twice in this milestone and matched the frozen report/summary hashes both times: MET-020 **2/2 per case**. [Replay audit](replay-audit.json) preserves hashes and attempts. It establishes stable output for frozen inputs, not fresh API stability. Core collection 2/2 and 6/6 coexists with sparse historical evidence and predominantly UNKNOWN findings: operational completion is not analytical sufficiency.
