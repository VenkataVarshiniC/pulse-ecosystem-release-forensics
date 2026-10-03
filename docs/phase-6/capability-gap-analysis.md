# Phase 6 capability-gap analysis

## Tested constraint

**Hypothesis:** PULSE can reliably collect and govern evidence, but often cannot acquire enough qualifying historical evidence to answer the lifecycle question.

**Result:** **SUPPORTED for the bounded validation population, with qualifications.** Core collection completed for 8/8 declared members, provenance and replay checks passed, and the same governed population is isolated through the product and Power BI. Yet 38/40 lifecycle findings remain `UNKNOWN`, only 2/40 assessments are sufficient, exact-ref declarations appear for 2/8 members, and paired pre-release context exists for 1/8. Observed adoption and recovery lack eligible evidence/denominators. These results support an evidence-sufficiency constraint after planned-source collection, not a claim that public evidence is universally inadequate.

The phrase “historical evidence” is only one branch. Missing resolved-version, recovery, accepted event, reason-code, and support-link inputs also contribute. The primary constraint is therefore **question-specific qualifying evidence depth**, with historical reconstruction the clearest observed component.

## Collection completeness versus analytical sufficiency

| Concept | Question | Current bounded result | Correct interpretation |
| --- | --- | --- | --- |
| Collection completeness | Did the required tasks in the declared plan finish? | Core metadata/issues/PRs/commits complete for 8/8 members; required tasks 11/11 pytest and 27/27 urllib3. | The plan executed successfully for its approved sources. |
| Analytical sufficiency | Are the prerequisites for a lifecycle finding met? | 2/40 sufficient, 38/40 insufficient. | Most lifecycle questions remain unanswered. |
| Finding outcome | What does qualifying evidence support? | 0 positive, 2 bounded NO, 38 UNKNOWN. | UNKNOWN is not NO; bounded NO is limited to the declared method. |
| Metric availability | Is an eligible numerator/denominator present? | Adoption/recovery unavailable; pytest review rate 0/0 unavailable. | No percentage or zero outcome may be substituted. |

## Root-cause hierarchy

```text
Low lifecycle-question answerability in the bounded validation population
├── A. Required qualifying inputs are absent or sparse
│   ├── release-boundary paired history is sparse
│   ├── qualified resolved/installed-version evidence is absent
│   ├── downstream recovery source and eligible set are absent
│   └── accepted local lifecycle evidence is absent
├── B. Current acquisition method cannot recover some available context
│   ├── fixed-window, path-change anchors miss older unchanged declarations
│   ├── cross-file manifest transitions remain unresolved
│   └── current/after-only declarations cannot establish a pre-release state
├── C. Qualification and linkage are incomplete
│   ├── required-source and reason taxonomy is coarse
│   ├── positive finding-to-support linkage has no live example
│   └── copied-upstream text requires origin-aware review
├── D. Workflow decisions remain unvalidated
│   ├── reviewer authority and burden are unknown
│   ├── required lifecycle questions are not stakeholder-approved
│   └── bounded completion and source thresholds are undefined
└── E. Scale is not yet the demonstrated constraint
    ├── larger cohorts would use the same weak evidence method
    └── current system throughput has no observed blocking failure
```

The hierarchy explains system outputs. It does not prove why maintainers make upgrade decisions or that any organization experiences a business problem.

## Gap analysis

| Gap | Observed evidence | Consequence | Classification | Priority implication |
| --- | --- | --- | --- | --- |
| 1. Acquisition gaps | Target-version runtime/CI, qualified lockfile resolution, and downstream release inputs were not collected. | Adoption and recovery remain unavailable. | Analytical / acquisition | Test only sources tied to an approved question and evidence contract. |
| 2. Historical-context gaps | 2/8 exact-ref declarations; 1/8 paired pre-release member; 6 `AFTER_ONLY` and 9 `UNRESOLVED` context records. | Release-boundary exposure often remains unknown. | Acquisition / analytical | Prespecify a history-depth experiment and pairing acceptance criteria. |
| 3. Source-availability gaps | Public planned sources may not contain installation, CI, private review, or production recovery state. | Better algorithms cannot recover evidence that is inaccessible or nonexistent. | Governance / stakeholder-dependent | Add explicit source-availability states and a stop condition. |
| 4. Evidence-qualification gaps | 38/40 findings are insufficient; several metric contracts lack approved question/source maps or typed reason partitions. | A collected record may remain ineligible for a finding or measure. | Analytical / governance | Define question-specific prerequisites and controlled missingness reasons before expansion. |
| 5. Provenance/linkage gaps | Candidate lineage is complete, but the published finding-support bridge has zero rows and there is no positive finding. | Positive source-chain integrity cannot be exercised on live published evidence. | Analytical / governance | Require explicit support-link completeness for any future positive finding. |
| 6. Review-workflow gaps | Two candidates from one artifact are inherited REJECT; published data are read-only. | Review productivity, authority, and three-outcome operation are untested. | Workflow / stakeholder-dependent | Preserve guardrails; defer workflow expansion until authority and a legitimate DRAFT case exist. |
| 7. Analytical-definition gaps | Required lifecycle question set, useful-completion definition, and recovery eligibility are not approved by stakeholders. | Some desired metrics remain partial, unavailable, or blocked. | Analytical / stakeholder-dependent | Keep proposed measures provisional and gate decisions on definitions. |
| 8. Interface/communication gaps | Technical views explain current states, but no live positive, conflict, source-unavailable, or recovery example exists; comprehension is untested. | Interface correctness cannot establish decision usefulness. | Interface / stakeholder-dependent | Make only evidence-explanation refinements tied to observed data and later stakeholder tests. |
| 9. Stakeholder-validation gaps | G8 has no responses or authorized owner. | Persona, value, priority, review burden, and acceptable evidence remain unknown. | Stakeholder-dependent | Maintain an explicit hold on value and workflow claims. |
| 10. Scaling gaps | No production-scale evidence exists, but local technical QA did not identify scale as the cause of insufficient findings. | Scaling now could multiply UNKNOWN outputs without improving answerability. | Technical / strategic | Defer breadth and production scaling until evidence-depth gates pass. |

## Primary capability gap

The primary gap is **the ability to obtain and qualify the evidence prerequisites for a bounded lifecycle question**, especially paired release-boundary history and question-specific source eligibility. It sits between acquisition and sufficiency rather than in storage, reporting, or interface delivery.

Historical reconstruction is the first bounded test because it has an observed baseline (1/8 paired pre-release members), a known method limitation, and a direct link to whether friction/remediation negatives can be bounded. Resolved-version and recovery evidence should enter only after their question, source, and eligibility contracts are approved; their absence does not justify broad source collection by default.

## Disconfirming evidence and limits

- Two bounded NO findings show that the current method can answer some questions when prerequisites are met.
- The lack of positive findings may reflect the cohort, source availability, detector behavior, or real absence; current evidence cannot distinguish these explanations broadly.
- The separate PR sample contains visible human interaction and specific downstream changes in some artifacts, showing that public sources can sometimes hold relevant evidence. It does not establish coverage for the governed cases.
- A deeper history method may still fail if repositories lack accessible anchors or changed packaging paths. Phase 6 therefore recommends a falsifiable experiment, not an assumed solution.
