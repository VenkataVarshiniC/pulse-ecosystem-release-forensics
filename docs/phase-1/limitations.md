# Phase 1 limitations

- GitHub search and mutable repository history can change future discovery results. Raw snapshots make the analyzed record reproducible, not the remote search index.
- The validation run used connector-assisted primary-source retrieval and preserved only three of eleven planned tasks. It does not prove unattended, comprehensive live collection.
- Explicit cohorts are purposive. Their metrics apply only to declared members and cannot estimate ecosystem prevalence.
- Public evidence overrepresents repositories with public issues, pull requests, CI, and detailed release notes.
- Text rules favor exact version mentions and can miss implicit events or create contextual false positives. Human review remains required.
- Dependency parsing covers high-value static Python formats. It does not resolve environment markers, lock graphs, dynamic setup code, or every package manager.
- Historical file retrieval is supported by ref, but automated before/after ref selection is not yet implemented.
- A closed issue or compatibility release does not by itself establish recovery. Recovery is omitted without an eligible denominator and qualifying event.
- The validation cohort is one repository. More predeclared cases are needed before comparing rule precision across project types.
