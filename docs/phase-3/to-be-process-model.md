# Provisional To-Be process model

This proposed swimlane/BPMN-style flow is **pending stakeholder reconciliation**. It is not the [observed bot-PR As-Is model](as-is-bpmn.md), and it does not imply that sampled public repositories use PULSE. Solid paths describe the proposed case workflow; optional source inputs and human feedback may repeat. The repository/service owner is an **unvalidated organizational actor**. Lifecycle findings are evidence categories, not a required time sequence.

```mermaid
flowchart TB
  subgraph ecosystem[Upstream dependency ecosystem — source, not PULSE actor]
    U[Release or other potential investigation signal]
  end
  subgraph analyst[Engineer or analyst — proposed role, ownership unvalidated]
    A{Open a bounded case?}
    S[Declare target release, cohort, window, and rationale]
    R[Inspect original evidence and rationale]
    J{Candidate decision}
    T{Enough for bounded closure?}
  end
  subgraph pulse[PULSE — proposed forensic support]
    C[Collect planned sources and preserve raw provenance]
    H[Reconstruct exact-ref context and check source sufficiency]
    G{Evidence state}
    N[Generate explainable candidates and attention suggestions]
    L[Separate accepted, rejected, and unresolved review]
    F[Derive bounded repository findings]
    V[Present declared-cohort view and evidence gaps]
  end
  subgraph repository[Repository and development tools — evidence sources]
    D[Manifests, history, PRs, issues, commits; optional CI, resolved version, releases]
    E[Source unavailable, incomplete, or conflicting]
  end
  subgraph owner[Repository/service owner — possible, unvalidated]
    O[Choose operational next action or completion criterion]
  end
  U --> A
  A -->|yes| S --> C
  A -->|no| X((End: no case))
  D --> C
  D --> E --> H
  C --> H --> G
  G -->|sufficient for a bounded question| N
  G -->|incomplete, unavailable, or conflicting| Q[Expose missing/conflicting evidence and UNKNOWN]
  Q --> R
  N --> R --> J
  J -->|accept| L
  J -->|reject| L
  J -->|needs more evidence| Q
  Q -. optional bounded follow-up .-> C
  L --> F
  Q --> F
  F --> V --> T
  T -->|more investigation| R
  T -->|bounded inquiry can close| O
  O --> Z((End: human disposition, with limits recorded))
```

`UNKNOWN` is not a negative branch. An accepted candidate can support a bounded YES even when another source is missing; a negative finding requires its own source-specific completeness threshold. A rejected candidate never enters accepted evidence. When no candidates are emitted, the report retains the method's recall limit. A collection failure does not remove the repository from the declared cohort. The possible owner lane does not assert a current organization chart or delegate production-risk acceptance to PULSE.

The proposed feedback loop is a human request for more evidence followed by bounded reacquisition or a documented unresolved finding. It is not an autonomous remediation loop. [Human/automation boundaries](human-automation-boundary.md) specify decision ownership; [To-Be process](to-be-process.md) gives the stage and exception definitions.
