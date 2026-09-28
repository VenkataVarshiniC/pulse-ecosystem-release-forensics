# M2.3 data-quality record

**Transformation defects observed: none.** The clean dbt build, 108 tests,
37 reconciliation checks, eight-member spine, typed support checks, source
fingerprints and repeat-build fingerprints passed. The one-artifact,
two-candidate, two-review pattern retained its independent grains. No dbt
view was used to write back to `ingestion` or `core`.

**Source limitations preserved:** only one of two pytest members and none of
six urllib3 members has paired pre-release history. The 16 historical
decisions include six AFTER_ONLY and nine UNRESOLVED records. A missing
source-event clock remains NULL rather than being filled with retrieval
time. Thirty-eight assessments carry the original `LEGACY_UNCLASSIFIED`
status. Thirty-eight lifecycle findings are UNKNOWN and two are bounded
NO_QUALIFYING_EVIDENCE_FOUND. All eight members retain UNKNOWN adoption and
recovery outcomes. There is no accepted candidate review or accepted positive
event chain in these frozen cases. The two current input snapshots are DRAFT,
so no published analytical snapshot exists.

These limitations may make later metrics unavailable or carefully bounded.
They are not defects for dbt to repair. The transformation neither infers
installed versions from declarations nor treats optional `not_found` as
source absence. Historical evidence stages are categories, not a required
chronological or causal sequence. Fixture and connector-assisted methods
remain distinct from unattended collector captures; this frozen PostgreSQL
load has zero of either method, which does not validate unattended collection
for other validation evidence. See the M2.2 [quality record](m2-2-data-quality.md)
for source loading limitations.
