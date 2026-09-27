# Provisional primary-user hypothesis

**Proposed primary user:** an engineer with explicit responsibility for dependency upgrades or release-impact investigation across several repositories owned by one organization, often in a platform or dependency-management function. This is a recruiting hypothesis, not a validated persona.

## Job and decision context

After a consequential upstream dependency release, this engineer may need to decide which owned repositories warrant investigation or migration/remediation attention, and what evidence supports that prioritization. They might compare dependency declarations at a relevant point in time, resolved versions, CI or issue signals, and later fixes. Their current sequence, authority, and frequency are unknown.

PULSE might help by bringing bounded repository evidence into one traceable report, showing source and collection limits, and leaving unsupported adoption or recovery states UNKNOWN. The hypothesis is plausible because Phase 2 demonstrated repeatable bounded collection and reporting but also exposed gaps that could block exactly such a decision: historical evidence in only 2/8 repositories, no target-version resolution, no downstream release recovery denominator, and weak event candidates. Technical feasibility and gaps do **not** establish that this user wants the report.

## Competing users and explanations

An application-team lead may make the operative decision for a single service; an open-source maintainer may investigate public downstream friction; a manager or supply-chain team may consume a summary. An existing dependency dashboard, CI workflow, or manual search may already meet the need. A user may care only about a small set of critical repos, making PULSE's current cohort method irrelevant. Discovery should not force these roles into the proposed primary-user model.

## What discovery must establish

Ask participants to reconstruct a recent actual release investigation: their trigger, repository population, decision authority, first evidence source, uncertainty threshold, review effort, and completion criterion. Determine whether they own multiple repositories, whether they need historical release-time state or installed versions, and whether a provenance-rich UNKNOWN result changes what they do. Seek disconfirming cases: no recurring cross-repository decision; existing tooling already sufficient; relevant evidence inaccessible; review cost exceeds value; or an alternative role owns the decision. If those prevail, revise the primary-user hypothesis before writing requirements.
