# Cross-evidence synthesis without pooling populations

| Question | Population A: Phase 2 forensic validation (8 repository memberships) | Population B: Phase 3 public PR workflow (20 base + 7 purposive) | Bounded implication |
| --- | --- | --- | --- |
| Automated upstream text | Copied upstream text produced false detector candidates in the urllib3 case, requiring source-origin review. | Copied upstream context appears in 13/20 base PRs; upstream issue links in copied text also 13/20. | Origin-aware interpretation is necessary when a detector reads PR bodies. This is **not** evidence that PR reviewers experienced burden. |
| Historical state | Release-boundary pairing is incomplete/weak for much of the declared forensic cohort. | PRs show proposed old/new versions and file diffs, but not necessarily release-time installed or organizational state. | A current/proposed diff cannot substitute for a historically paired release-boundary observation. |
| Human review | Candidate review and rejection reasons are explicit forensic process stages. | Visible interaction in 6/20 base cases; one base and one discussion case has substantive technical comment. | Concentrating review on cases with local exceptions is a **design hypothesis**, pending stakeholder validation. |
| Outcome meaning | UNKNOWN, sufficiency and bounded NO are distinct; no valid broad adoption/recovery rate. | Merge/closure and elapsed PR time are observable, but compatibility/recovery and effort are not. | Neither population supplies a valid denominator for ecosystem recovery, time saved or PULSE effectiveness. |
| Provenance | Collector, connector-assisted and fixture evidence must remain distinct. | Frozen PR observation coding follows a public candidate frame and cutoff; check histories were not systematically audited. | Preserve source and method when comparing any future evidence, never silently join counts across grains. |

The populations answer different questions and have different selection mechanisms, units and windows. No arithmetic pool, merged rate, causal inference, detector precision or portfolio-prioritization outcome is valid here.
