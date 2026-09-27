# Provisional As-Is process-step catalogue

Each `ASIS` ID is a trace handle for current-state analysis, **not** a requirement. Steps 01–05 describe the frozen public, bot-initiated PR sample; steps 06–08 describe the existing PULSE analytical path, which is **not** shown to be part of those repositories' workflow. Steps 09–10 are organizational hypotheses/open boundaries. The steps are not a mandatory lifecycle chronology. Status terms follow [the evidence model](as-is-evidence-model.md); `GH` denotes [coded public PRs](secondary-research/github-pr-observations.jsonl), `P2` denotes [Phase 2 findings](../phase-2/phase-2-findings.md), and `M1` denotes [Milestone 1 hypotheses](business-problem.md).

## ASIS-01 — Update PR enters the public record

- **Actor/system; trigger; inputs:** Dependabot in all sampled cases; exact schedule/security/release trigger unknown; package update proposal.
- **Activity; output; decision:** Opens a PR with a proposed package change; PR becomes an observable artifact; no upstream or portfolio intake decision is established.
- **Evidence/status; exception; limitation; question:** GH, `secondary-evidence-supported`; none required; `bump` search omitted manual paths. **Q01/Q02:** What actually triggers a stakeholder investigation and who initiates it?

## ASIS-02 — Proposed dependency state and upstream context exposed

- **Actor/system; trigger; inputs:** Dependabot/GitHub PR; PR creation; package version, manifest/lockfile diff, sometimes copied upstream notes or badge link.
- **Activity; output; decision:** Presents old/proposed dependency change and context; reviewers may inspect it, but actual reading is not established.
- **Evidence/status; exception; limitation; question:** GH, `secondary-evidence-supported`; grouped proposals and copied text occur; declaration change does not prove installation. **Q04/Q06/Q07:** Which evidence and point-in-time state matter?

## ASIS-03 — Optional public validation and human review

- **Actor/system; trigger; inputs:** Repository checks where visible and human reviewer where present; PR proposal; diff, comments, and any public check discussion.
- **Activity; output; decision:** A reviewer may comment, approve, request revision, or command the bot; [baseplate.py#1054](https://github.com/reddit/baseplate.py/pull/1054#pullrequestreview-2532549557) reported test failures.
- **Evidence/status; exception; limitation; question:** GH, `secondary-evidence-supported`; only 6/20 base PRs had visible human interaction; check-run histories and private review were not audited. **Q05/Q08:** Is CI enough, and what review work is acceptable?

## ASIS-04 — Visible exception or additional change handled

- **Actor/system; trigger; inputs:** Human reviewer, repository contributor, or Dependabot; a visible concern, command, or stale update; PR diff/comment.
- **Activity; output; decision:** In sampled cases, code changed after a mypy type issue, a grouped proposal retained an older pin, or a rebase command received an up-to-date bot reply.
- **Evidence/status; exception; limitation; question:** GH, `secondary-evidence-supported`; examples are [baseplate.py#1054](https://github.com/reddit/baseplate.py/pull/1054), [uvicorn#2549](https://github.com/Kludex/uvicorn/pull/2549), and [Delphix#598](https://github.com/delphix/virtualization-sdk/pull/598); no universal exception rule or effort is known. **Q08/Q09:** Which exceptions require action versus routine bot maintenance?

## ASIS-05 — Local PR reaches a visible disposition

- **Actor/system; trigger; inputs:** GitHub PR record and a maintainer/bot action where visible; reviewed or unrevised proposal; comments/status.
- **Activity; output; decision:** PR is merged or closed without merge. Explicit reasons include supersession and no-longer-needed responses; no reason is invented when absent.
- **Evidence/status; exception; limitation; question:** GH, `secondary-evidence-supported`; base 9 merged/11 closed, purposive discussion 4 merged/3 closed; disposition does not prove migration/recovery. **Q10:** What signals actual completion?

## ASIS-06 — PULSE collects bounded source evidence (analytical overlay)

- **Actor/system; trigger; inputs:** Existing PULSE collector; declared case/cohort and collection plan; public GitHub/PyPI sources.
- **Activity; output; decision:** Collects planned sources with run outcomes, raw provenance, and deterministic task identity; the pipeline computes bounded source sufficiency while analyst review addresses emitted candidates.
- **Evidence/status; exception; limitation; question:** P2, `observed` in PULSE; core collection complete in 2/2 and 6/6 frozen repositories; source coverage is not event completeness or stakeholder adoption. **Q03/Q04:** Which repositories and sources matter to the real decision?

## ASIS-07 — PULSE reconstructs context and reviews candidates (overlay)

- **Actor/system; trigger; inputs:** Historical path-scoped collector, detector, analyst reviewer; exact-ref states and collected text.
- **Activity; output; decision:** Parses bounded target declarations, emits candidates, keeps accepted evidence separate from rejected candidates.
- **Evidence/status; exception; limitation; question:** P2, `observed` system behavior; declaration evidence 2/8 and two bot-text candidates rejected; older unchanged paths, target installation, and recall remain unresolved. **Q06/Q07/Q09:** What threshold justifies exposure or a friction finding?

## ASIS-08 — PULSE reports findings or UNKNOWN (overlay)

- **Actor/system; trigger; inputs:** Existing report pipeline; verified collection/history/baseline/review artifacts.
- **Activity; output; decision:** Produces deterministic, provenance-aware findings; unavailable prerequisites remain UNKNOWN, not NO.
- **Evidence/status; exception; limitation; question:** P2, `observed` system behavior; zero accepted lifecycle events and no adoption/recovery rate in frozen reports; utility to a user is untested. **Q11/Q12:** What next action follows UNKNOWN, and what provenance is trusted?

## ASIS-09 — Define portfolio scope and investigation priority

- **Actor/system; trigger; inputs:** Decision owner unknown; consequential release or upgrade signal is possible; owned repository set and operational context unknown.
- **Activity; output; decision:** Hypothetically choose repositories and investigation priority. No sampled PR or Phase 2 system run demonstrates an organization's prioritization process.
- **Evidence/status; exception; limitation; question:** M1, `hypothesized`, `pending stakeholder validation`; cannot assign an owner or effort. **Q01/Q02/Q03:** Does this decision exist, who owns it, and what triggers it?

## ASIS-10 — Declare migration or recovery complete

- **Actor/system; trigger; inputs:** Owner, criterion, and production evidence unknown; local PR disposition alone is insufficient.
- **Activity; output; decision:** Organizational completion would require a definition and evidence; no such current process is established here.
- **Evidence/status; exception; limitation; question:** P2 recovery inputs absent; GH only PR disposition; `not observable`, `pending stakeholder validation`. **Q10:** What does “done” mean and which artifact proves it?
