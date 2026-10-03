# M4.2 dashboard validation and closure

Classification: **M4.2 PASS** for the technical Power BI milestone. The edited PBIP was refreshed, rendered, and manually validated in Power BI Desktop after the final filtering repair. G8 stakeholder validation remains **NOT_YET_VALIDATED**; this result does not claim stakeholder approval or UAT completion.

Completed checks:

- PBIR schema: six pages, 50 visuals, zero errors and zero warnings from the Microsoft report-author validator.
- TMDL parser: 24 tables, 22 relationships, 35 measures; all 12 governed relationships active and single-direction many-to-one.
- Static binding audit: all visual field references resolve; page and drillthrough references exist; visual positions fit 1920×1080; all six main-page slicers use strict single selection; seven fact/bridge M queries contain the state and two-ID allowlist.
- Frozen replay reconciliation passed using the local repository virtual environment. Read-only SQL fanout checks found no duplicate member-fact matches.
- Read-only live DAX checks returned pytest as 2 members, 10 findings, 5 observations, and 0 candidates, and urllib3 as 6 members, 30 findings, 6 observations, and 2 candidates.
- Explicit PBIR `DataFilter` interactions connect both strict case/snapshot slicers to every data visual on each main page. The observation table uses the governed bridge repository field, and empty finding combinations return blank.

## Power BI Desktop validation

Desktop validation confirmed:

- Selecting pytest shows only `bsc-wdc/qdislib` and `planetlabs/cosmolog` in member-scoped diagnostics, with no urllib3 leakage; exact-ref observations remain in the pytest scope.
- Selecting urllib3 shows only its six declared repositories, with no pytest leakage; exact-ref observations remain in the urllib3 scope.
- pytest candidate quality renders Candidate Count 0, Candidate Artifact Count 0, Candidate Density 0.00, and both review rates as **Unavailable (0 eligible observations)**.
- urllib3 candidate quality renders Candidate Count 2, Candidate Artifact Count 1, Candidate Density 0.33, acceptance **Inherited review · 0% (0/2)**, and rejection **Inherited review · 100% (2/2)**.
- The two urllib3 candidate firings remain grouped to one shared artifact. Inherited REJECT semantics remain explicit, and the report claims no new reviewer action.
- Repaired KPI/display cards render the governed denominator text without truncation.
- Finding Detail, Observation Detail, and Candidate Detail are hidden from ordinary navigation. Each opens one selected record through drill-through, retains its evidence-semantics text, and returns through the Back button.

The validated analytical boundaries remain: UNKNOWN is not NO; missing evidence is not negative evidence; REJECT is not absence of migration friction; and a candidate firing is not necessarily an independent incident. No screenshot files are committed, and no WCAG certification is claimed. The `.pbix` is not an output of the final text-project validation and is excluded from the closure commit.

Repository quality checks: Ruff passed. Full pytest passed 194 tests with a fresh task-specific base temp directory. The first attempts failed at fixture setup because Windows denied access to pytest's shared temp directory; there were no assertion failures. The scratch directory created inside the checkout was removed after the passing run.
