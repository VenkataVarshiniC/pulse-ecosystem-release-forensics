# Stakeholder discovery plan

**Status:** protocol ready; no participants recruited or interviewed in Milestone 1. The plan tests the [primary-user](primary-user-hypothesis.md), [problem](business-problem.md), and [needs](stakeholder-needs-hypotheses.md) hypotheses without assuming PULSE is the answer.

## Learning objectives

Identify who owns release-impact decisions for a declared set of repositories; reconstruct their last actual workflow and evidence thresholds; understand how they judge repository exposure, friction, remediation, and completion; test whether missing evidence, candidate review, or provenance changes action; and identify current tools that already solve the job. Explore alternative decision-makers and disconfirming cases.

## Participants and recruitment

Aim for **5–8 genuine conversations where feasible**. A minimum target of **3 genuine stakeholder conversations** is needed before treating repeated patterns as provisionally validated; three is a research target, not a guarantee of representativeness or a reason to ignore contradictions. Prioritize engineers accountable for dependency upgrades or release investigations across at least two repositories, then application-team leads who performed a recent case, and people who oversee or consume that decision. Include variation in repository ownership, ecosystem, and tooling where possible. Do not recruit only PULSE supporters or personal acquaintances who cannot describe the workflow.

Qualifying participants should have personally performed, directed, or reviewed a concrete dependency-release investigation or upgrade in the recent past. Screen for their responsibility, number/type of repositories, and ability to discuss a real case without confidential details. Record non-qualifying conversations separately. Recruitment is future work; no outreach or consent is claimed here.

## Format and principles

Use a 20–30 minute semi-structured conversation if practical. Explain the research purpose and request permission to take notes; do not promise anonymity beyond the actual handling policy. Start with the participant's recent work, **not a PULSE pitch**. Ask neutral, open questions about what happened, artifacts they used, decisions made, and counterexamples. Request concrete timelines and examples, while allowing them to omit sensitive information. Save solution reactions until the current workflow is understood; any later PULSE concept feedback must be labeled as reaction, not observed behavior.

## Core interview guide

1. Walk me through the last time a dependency upgrade or upstream release created unexpected work. What triggered it?
2. How did you identify which repositories might be affected? Who decided the set?
3. What information did you look for first, and why?
4. Which tools or sources did you use? Can you describe the evidence each provided?
5. What was hardest to determine? What remained unknown?
6. How did you decide whether action was required for a repository?
7. What evidence made you confident, and what would have changed your mind?
8. Which step took the most effort? Approximately how often does this kind of work occur?
9. When did you consider the migration or incident complete? What evidence marked that point?
10. What information was unavailable, and what did you do without it?
11. How did you communicate or document the result? Who reviewed or acted on it?
12. Which part of that workflow would you most want to improve, if any? Why that part?

Optional probes: What version was actually installed or resolved at the decision point? Did a current declaration differ from historical state? How did you distinguish an automated dependency PR from actual friction? What would an inconclusive/UNKNOWN finding prompt you to do? How many candidates could you reasonably review? Which existing tool already handles this well? Ask these only when relevant, without implying a preferred answer.

## Evidence capture and analysis

For each conversation, record an anonymized participant ID (`P01`, `P02`, ...), role and relevant experience, case trigger, decision and owner, process steps, evidence sources, frequency and severity as reported, pain points, workarounds, trust requirements, human-review tolerance, desired output, direct quotes or faithful paraphrases where permitted, contradictions, and analyst interpretation. Use [the blank findings template](discovery-findings-template.md). Mark whether each statement is a participant report, artifact observation, or analyst inference. Do not turn one person's preference into a universal need. Preserve counterexamples and unsupported hypotheses.

After conversations, compare actual cases by decision, sequence, evidence threshold, and workaround; note how many qualified participants support or contradict each theme. Revisit the primary user and scope. Treat any finding as provisional until supported by documented genuine conversations and reviewed for conflicting evidence. Do not promote needs to formal requirements until later process and requirements milestones. If access or evidence barriers dominate, record that as a possible reason to revise or abandon the proposed workflow.

## Privacy and record handling

Ask permission before recording or quoting. Prefer notes over recordings. Do not commit names, employers, contact details, private repository identifiers, secrets, or personally identifiable interview data unnecessarily. Keep consent/contact records outside the repository under appropriate control. Commit only anonymized summaries with IDs and redacted examples after checking disclosure permission; otherwise retain only aggregate, non-identifying findings. The present repository contains no interview findings.
