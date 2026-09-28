# Decision-led SQL and Python analysis backlog

These are query specifications/pseudocode, not executable SQL. Every output carries case version, snapshot ID, selection frame, source-plan/metric version, N, D and unavailable reason. Use NULLIF on a verified denominator; do not COALESCE missing evidence to zero. Implement canonical definitions once in dbt/SQL marts, then let Python read those marts rather than recompute competing metrics.

| Product Analyst question | Proposed SQL method and output | Guard |
| --- | --- | --- |
| Where does the investigation lose evidence coverage? | CTE frozen members; separate per-member conditional task/context/stage aggregates; left join F0–F5 and candidate B1–B3 branches; count distinct grain keys. | Candidate branch optional; no multiplication of branch rates; stage categories not chronological. |
| Which cohorts have paired pre-release versus after-only context? | Group case/release/history status from exact-ref pairs; partition within case/source-plan; show raw N/D. LAG/LEAD by repo/path/ref-time only to inspect source states. | Cross-file moves and older unchanged declarations unresolved; no population/causal comparison. |
| Which rules produce reviewable signal? | CTE one terminal review per candidate/cycle; filtered ACCEPT/REJECT/NEEDS_EVIDENCE aggregates by rule and source origin; rank with percent of reviewed total. | One PR may yield two dependent firings; reviewed-emitted proxy only. |
| Why is a finding UNKNOWN? | Unique member-stage/question denominator CTE; join assessment reason edges; conditional missing-source counts and percent of UNKNOWN plus overall eligible denominator. | Multi-label reasons overlap; blank reason blocks named-reason rate. |
| Which required source is missing? | Anti-join planned required source/member-stage combinations to verified task outcomes, plus optional-not-found separately; completeness matrix. | Collected source does not imply analytical sufficiency. |
| Has a snapshot changed an answer? | Explicit two-snapshot full outer comparison at member/category/question; LAG over publication version for reported transitions with reason and changed input hash. | New live capture is not deterministic replay; no implicit latest row. |
| Is review latency observable? | For trusted emission and terminal timestamps compute intervals and percentile_cont distribution; optional rolling summaries only across comparable repeated cases. | Source event time is not emission time; elapsed clock time is not analyst labor. |
| Which accepted finding lacks provenance? | Anti-join YES finding to typed qualified support, review/observation, artifact and raw digest chain. | Must return zero before publishing MET-021. |
| Is future recovery eligible? | Explicit accepted qualifying event set and bounded window CTE; downstream source join; separate eligibility from observed signal. | Remains unavailable until source and owner-defined method exist; PR merge alone excluded. |

Python's later role: bootstrap intervals for sufficiently sized governed case-local distributions, sensitivity analysis of missingness, exploratory plots and validation diagnostics. It consumes published mart keys and manifest IDs. The current two purposive cases/eight members are too small and selected to support population intervals or causal claims; no inferential result is authorized by this backlog.
