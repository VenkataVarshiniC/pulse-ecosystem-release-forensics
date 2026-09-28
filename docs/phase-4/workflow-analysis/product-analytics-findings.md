# Bounded Product Analytics findings

Each denominator refers to the frozen **base** sample unless a separate purposive example is named. These are selected-record descriptions, not population estimates.

## 1. Most base PRs have no visible human interaction

**Observation:** 6/20 base PRs show public human interaction; 14/20 do not. Five of nine merged PRs have interaction, while four of nine merged PRs do not. **Denominator:** 20 base PRs; merger split denominator nine. **Interpretation:** Some proposals reach disposition with minimal public discussion. **Product implication:** Ask whether an exception-first review queue is useful. **Limitation:** Private review and actual attention are invisible; sampled PRs are bot-centered. **Stakeholder question:** Which signals trigger a human decision in the real workflow?

## 2. Approval is a visible but incomplete decision signal

**Observation:** Explicit approval appears in 4/20 base PRs, all among the nine merged. **Denominator:** 20 base PRs, with nine merged for the subset. **Interpretation:** Public review approval is only one route to terminal action. **Product implication:** Decision provenance would need more than approval state. **Limitation:** No systematic checks history or organization policy. **Stakeholder question:** What approval or CI evidence does a decision-maker require?

## 3. Upstream context is common, but local statements are rare

**Observation:** 13/20 base PRs copy upstream notes/changelog; 16/20 show compatibility badge/links; only 1/20 has a substantive downstream technical comment. **Denominator:** 20 base PRs. **Interpretation:** Automatically provided upstream context and downstream-local reasoning are distinct evidence streams. **Product implication:** Keep source origin explicit in any case review. **Limitation:** Presence does not measure usefulness or whether missing local comments reflect uncertainty. **Stakeholder question:** Which context must reviewers cross-check before a version decision?

## 4. Closure often reflects proposal lifecycle

**Observation:** 9/20 base PRs merged and 11/20 closed without merge; eight of the 11 closures explicitly cite supersession. **Denominator:** 20 terminal base PRs, 11 closures for reason mix. **Interpretation:** Closure categories should remain distinct from compatibility outcomes. **Product implication:** Preserve close reason and replacement links rather than treating every closure as failed update. **Limitation:** Supersession is not a measure of work lost or PULSE value. **Stakeholder question:** Do superseded bot PRs create any material triage burden?

## 5. Public exception paths are heterogeneous

**Observation:** 12/20 base PRs have at least one explicit taxonomy label, mostly administrative closure; no base PR has a coded source/test/config change. Separately, one of seven purposive discussion examples documents test failure plus code change. **Denominator:** 20 base; discussion example out of seven with no prevalence claim. **Interpretation:** A single “friction” score would conflate different events. **Product implication:** Keep reason-level paths and evidence links. **Limitation:** Sampling and coding cannot establish exception incidence in production workflows. **Stakeholder question:** Which exception types merit investigation or escalation?

## 6. Resolution time does not measure effort

**Observation:** The 20 terminal base PRs have median 167.25 elapsed hours and IQR 607.7 hours; maximum 5823.4. **Denominator:** 20/20 terminal base PRs with timestamps. **Interpretation:** Public PR lifecycle spans vary widely. **Product implication:** If shown, use a distribution with outlier context. **Limitation:** Cannot infer engineering effort, delay cause, saved time or intervention effect. **Stakeholder question:** What operational timestamps, if any, reflect actual decision effort?
