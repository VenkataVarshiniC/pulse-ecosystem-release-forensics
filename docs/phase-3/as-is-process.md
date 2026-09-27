# Provisional As-Is dependency investigation process

This is the strongest **current-state account** available before stakeholder responses. It joins a public, bot-initiated PR artifact path with a separate PULSE analytical overlay. It is **not** a final stakeholder-validated organizational process. Stages may repeat or be skipped; PULSE lifecycle categories do not imply chronological or causal order. [The evidence model](as-is-evidence-model.md) marks each boundary.

## Trigger and intake

**Secondary-evidence-supported:** Dependabot opened every selected PR in the frozen Milestone 1A frame. A PR body often included upstream release material. The actual trigger—scheduled run, security concern, release notification, or human request—was not established. **Hypothesized:** an organization might separately initiate an investigation after a consequential upstream release; no stakeholder has confirmed that intake step.

## Scope identification

**Hypothesized, pending stakeholder validation:** someone may define a set of owned repositories/services, decide which are relevant, and prioritize investigation. No sampled PR shows that portfolio selection. PULSE's Phase 2 cohorts were predeclared research cases, not an observed organization's work queue. The [primary-user hypothesis](primary-user-hypothesis.md) remains provisional.

## Dependency-state inspection and evidence gathering

**Secondary-evidence-supported:** each selected PR exposes a proposed package-file diff; bot bodies may attach upstream release notes, changelogs, and compatibility-badge links. Review comments or status replies can add local context. [baseplate.py#1054](https://github.com/reddit/baseplate.py/pull/1054) shows why copied mypy release text and a downstream typing explanation must be read separately. The selected PRs do not establish installed target versions or release-time state across repositories.

**PULSE-observed system overlay:** current bounded collection can gather metadata, issues, PRs, commits, and exact-ref path history, with provenance and deterministic reports. Yet Phase 2 established target-package declarations in only 2/8 frozen repositories, lacked comprehensive installed/runtime version evidence, and produced UNKNOWN findings where a prerequisite was missing. These are facts about PULSE's analytical path, not proof that human reviewers use PULSE or inspect all these sources.

## Review and interpretation

**Secondary-evidence-supported:** 6/20 base PRs had visible human interaction; the separate purposive discussion sample had 7/7 by design. Approval, a version-retaining suggestion, and a reported test failure with code change are observable local actions. Check-run histories were not systematically audited, and public silence does not mean no validation or private discussion. **Hypothesized:** a cross-repository investigator may compare evidence across cases; that action is not visible in the sample.

## Exception handling and local decision

**Secondary-evidence-supported:** [uvicorn#2549](https://github.com/Kludex/uvicorn/pull/2549) retained an older `websockets` pin relative to the bot proposal; [baseplate.py#1054](https://github.com/reddit/baseplate.py/pull/1054) included a library-code change after a test-failure review. Eight base PRs carried explicit supersession comments. Three Delphix discussion PRs had human rebase commands followed by “already up to date” bot replies. These are different exception paths, not one mandatory sequence or evidence of wasted effort. The visible local disposition is merge or closure without merge; a close may mean superseded, no longer needed, or another explicitly recorded reason. No universal acceptance rule is established.

## Completion boundary

**Observed local artifact state:** Sample A ended with 9 merged and 11 closed PRs; Sample B with 4 merged and 3 closed PRs. A merge is a PR disposition, **not** proof of dependency installation, organizational migration completion, or production recovery. Phase 2 collected no downstream releases and had no recovery-eligible denominator. The stakeholder's completion criterion remains `pending stakeholder validation`.

The [swimlane](as-is-swimlane.md) and [BPMN-style model](as-is-bpmn.md) depict only the public PR path. The [step catalogue](as-is-process-catalogue.md) carries the unresolved organizational overlay with explicit status and questions.
