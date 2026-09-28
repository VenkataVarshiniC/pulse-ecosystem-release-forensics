# Proposed dbt integrity test matrix

All tests are future contracts, **not executed dbt tests**. Generic unique, not_null, relationships and accepted_values apply to every declared key/FK/status in [source contracts](dbt-source-contracts.md). Severity ERROR blocks the affected snapshot/mart; WARN is only for an explicitly non-required operational diagnostic. Failing rows are retained for inspection, not filtered out. Application checks run before dbt; human review qualifies ambiguous source statements.

| ID/theme | Phase 3 rule | Model/field | Layer; severity; handling |
| --- | --- | --- | --- |
| T01 frozen member anti-join and count | RULE-011 | bridge_case_repository vs core membership; int_case_repository | DBT ERROR; block missing member/changed denominator |
| T02 required task failure vs optional not_found | RULE-001/010 | task/int_repository_evidence | DBT ERROR; block false success, preserve 404 |
| T03 verified artifact hash/method chain | RULE-014 | artifact/source/task/raw manifest | APPLICATION + DBT ERROR; quarantine mismatch |
| T04 declaration cannot become target resolution | RULE-003 | observation/fct_evidence_observation | DATABASE conditional CHECK + DBT ERROR; block MET-003 |
| T05 current absence cannot become historical absence | RULE-002 | observation/historical_pair | DBT ERROR; block historical negative |
| T06 after-only cannot qualify release-window negative | RULE-009 | pair/assessment/finding | APPLICATION + DBT ERROR; block bounded NO |
| T07 candidate not accepted evidence by emission alone | RULE-004 | candidate/review/finding support | DBT ERROR; block YES |
| T08 rejected or unresolved never supports YES | RULE-005/007 | selected review/typed bridge/finding | DBT ERROR; block finding |
| T09 zero emitted cannot imply event absence | RULE-006 | stage sufficiency/finding | APPLICATION + DBT ERROR; block unqualified NO |
| T10 lifecycle chronology is not imposed | RULE-008/013 | finding and report assertions | APPLICATION/HUMAN REVIEW + DBT ERROR for ordered-stage derivations; no causal wording |
| T11 UNKNOWN never maps to bounded NO | RULE-003/010 | sufficiency/finding/mart | DBT ERROR; block publication |
| T12 YES has intact accepted or qualified direct support | RULE-004/014 | finding → bridge → review/observation → artifact | DBT ERROR; block finding |
| T13 recovery requires event/set/window/source | RULE-012 | recovery eligibility proposal | APPLICATION + DBT ERROR; keep metric unavailable |
| T14 matching case/member/category across support chain | RULE-014 | all core FKs and typed bridges | DATABASE FK + DBT ERROR; quarantine mismatch |
| T15 one terminal decision per candidate/cycle | RULE-005/014 | analyst_review/int_candidate_terminal_review | DATABASE partial unique + DBT ERROR; block selected result |
| T16 source event vs retrieval clock separation | RULE-008/013 | artifact/observation/review | APPLICATION + DBT ERROR for fabricated fallback; block time metric |
| T17 snapshot and mart composite grain unique | RULE-011/014 | manifest and every fact | DATABASE unique + DBT ERROR; block mart |
| T18 join cardinality/golden reconciliation | RULE-011/014 | candidate/artifact/member/finding marts | DBT ERROR; compare distinct key sets and counts |
| T19 stage reason/source prerequisite exists | RULE-010 | assessment_source_reason/int_stage_sufficiency | DBT ERROR for publishable MET-013/015; otherwise unavailable |
| T20 fixture/connector exclusion from collector metric | RULE-010/014 | artifact/task/source mart | DBT ERROR; block unattended claim |

Additional generic checks: non-null release and case natural keys, no duplicate member or finding version, referential artifact IDs, allowed capture/decision/status values, nonnegative attempt counts, and valid window order. Human review remains necessary to decide whether a local statement truly qualifies; automated tests cannot prove recall or organizational usefulness. The positive YES path cannot be empirically reconciled against current frozen cases with zero YES findings, so its test requires a governed future fixture before production publication.
