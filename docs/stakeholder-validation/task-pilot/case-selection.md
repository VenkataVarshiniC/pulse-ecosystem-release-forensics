# Pilot case selection

## Selected study case

Use the existing **published baseline** in the React investigation application, in two bounded parts:

1. **Primary case — pytest 8.0.0**
   Published snapshot `08852d5f-9843-5406-a69b-7039ea2ddaa4`. This case has two declared repositories, ten lifecycle findings, eight UNKNOWN findings, two bounded NO findings, and no detector candidates.
2. **Focused candidate extension — urllib3 2.0.0**
   Published snapshot `bd3a02a5-0c2d-5eec-84fd-8e9b93a238a3`. Use `jamesturk/scrapelib` to examine two inherited REJECT candidate firings that share one captured artifact.

Start from `/investigations` and let the participant navigate. Preserve the exact `snapshot_id` selected by the application.

## Why this pair is suitable

The pytest case tests declared scope, an entirely UNKNOWN repository, a repository containing both UNKNOWN and bounded NO, historical context, missing evidence, and the absence of candidates. The urllib3 extension supplies candidate, inherited-review, shared-artifact, and capture-provenance concepts that pytest cannot exercise.

Together they cover the core semantics without changing evidence or manufacturing a positive finding. The current published baseline contains zero positive findings, and that limitation is part of the task.

## Interface decision

Use the existing React/FastAPI/PostgreSQL workflow as the primary surface because it provides navigable investigation, repository, evidence, finding, candidate, and artifact pages. Do not switch to Power BI during the core task. The Power BI report is a separate analytical surface whose scope filtering has been technically validated; mixing it into this small pilot would make interface effects impossible to interpret.

## Evidence boundary

Do not edit published evidence, submit reviews, run collectors, or expose a DRAFT snapshot. Phase 7 treatment results are experimental and are not the authoritative published result for this pilot. If the local published stack is unavailable or differs from the recorded snapshot, stop the session and mark affected dimensions `NOT_OBSERVED`.
