# Build-versus-integrate boundary, provisional

These are analytical ownership options, **not** implementation authorization. Evidence references are in the [source ledger](source-ledger.md); final choices require a real workflow and access model.

| Capability | Provisional disposition | Evidence and rationale | Decision gate |
| --- | --- | --- | --- |
| Package/version release facts | **Consume existing source** | PyPI and deps.dev already expose releases, versions and advisories [S15,S16]. | Validate terms, cache/provenance and release identity. |
| Git repository/PR/issue/commit history | **Integrate** | GitHub REST APIs and UI already hold raw evidence [S07]. | Access, pagination, retention, private repository rights and completeness. |
| Routine update PR generation/grouping | **Explicitly not own** | Dependabot/Renovate are mature documented alternatives [S01,S02,S08,S09]. | No new product work absent changed user need. |
| Vulnerability/license/risk scanning | **Explicitly not own; integrate references if relevant** | GitHub, Mend, Snyk, Socket, Sonatype cover this [S03,S12–S14,S17–S20]. | Determine whether security signal belongs in a case. |
| Generic CI execution | **Explicitly not own; consume references** | GitHub Actions exposes run logs [S06]; existing CI should remain authoritative. | Qualify run/ref/environment and log retention. |
| Historical release-boundary pairing | **Potentially build narrow orchestration** | Git history/API supply raw material, but PULSE Phase 2 coverage is weak; native target-release pairing not verified [S07; Phase 2]. | Evidence method and stakeholder need before expansion. |
| Downstream event provenance/correlation | **Potentially build narrow review logic** | Raw PR/issue evidence exists [S07]; copied upstream text produced false candidates in Phase 2. | Precision, missed-signal risk and reviewer workload. |
| Source sufficiency, UNKNOWN and case report | **Potentially build/retain** | Adjacent tools have risk/identity provenance [S18,S21]; case-specific evidence sufficiency not verified. | Demonstrate a changed decision from a bounded report. |
| Resolved target-version and recovery claim | **Defer until qualifying source and denominator** | Current PULSE metrics are unavailable; registry metadata and PR merge cannot stand in [S15,S16; Phase 4 M1A]. | Identify actual source, eligible set, window and owner. |
| Cross-repository inventory/dashboard | **Integrate or explicitly not own as a generic feature** | GitHub, Socket and Sonatype already provide cross-repo/app views [S05,S18,S19]. | Only consider case-specific comparison after use validation. |

The proposed future PULSE slice is an **investigation layer over existing systems**, not a new registry, scanner, update bot, CI engine or generic dashboard.
