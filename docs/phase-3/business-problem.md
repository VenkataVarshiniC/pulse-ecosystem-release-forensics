# Business-problem hypothesis

## Provisional problem

An engineer investigating the effect of an upstream dependency release across declared downstream repositories may have to correlate scattered, time-sensitive evidence before deciding where to act. Current dependency declarations may not describe release-time state; declarations may not show installed versions; issues and PRs may be irrelevant; and a missing observation can be confused with evidence that nothing happened. This is a **hypothesized workflow problem**, not an observed stakeholder complaint.

## Possible user impact

The investigator may spend effort reconstructing evidence, reviewing irrelevant candidates, and deciding how much confidence to place in incomplete data. Phase 2 demonstrated these evidence gaps within PULSE's frozen validation, but did not measure a human's effort, severity, or frustration. Discovery must establish whether these costs occur in actual work and how users handle them now.

## Possible operational impact

Uncertain repository exposure could affect triage and communication of upgrade status. The frequency, delay, quality, cost, and organizational consequences are unknown. No hours saved, dollar value, adoption rate, or quantified business benefit is claimed. A later baseline should measure the existing workflow only after the decision and population are identified.

## Decision PULSE may support

Which repositories in a declared, owned set require further migration or remediation investigation after a significant dependency release, and what evidence and uncertainty justify that prioritization? This is a decision hypothesis; discovery may show a narrower or different decision.

## Why existing PULSE is insufficient

Phase 2's collector/report path was reproducible, but historical target-package declaration evidence covered only 2/8 frozen repositories; installed target versions and ordinary runtime/CI resolution were unestablished; downstream releases were absent; and two candidates from one Dependabot PR were rejected. The reports appropriately carry UNKNOWN states. Thus the existing system cannot yet reliably determine repository adoption or bounded recovery for those cases, even if a stakeholder wants that decision. See [Phase 2 BA inputs](phase-2-ba-inputs.md).
