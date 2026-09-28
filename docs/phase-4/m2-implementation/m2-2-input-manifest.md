# M2.2 frozen input manifest

The committed [machine manifest](../../../data/manifests/phase2-postgres-load-manifest.json) is the sole load allowlist. It contains 142 files and has canonical SHA-256 `09d66f72862cfaa1a664cb1fc5c42a5b8fe28dbaeb35bd7f42364bdbff50a743`. Each entry records logical root, relative path, case, repository when applicable, role, byte-level SHA-256, capture method and parser interpretation. The manifest fingerprint covers those entries and the logical-root mapping. `verify` checks the manifest fingerprint, every file's digest, case boundary, duplicate entries and path containment before the loader opens a database connection. A mismatch aborts; the loader never refreshes a trusted digest automatically.

The `repo` root resolves to this checkout. The four external logical roots resolve from these environment variables, which may also be placed in the ignored root `.env` file:

| Logical root | Environment variable |
| --- | --- |
| `pytest_collection` | `PULSE_PHASE2_PYTEST_COLLECTION_ROOT` |
| `pytest_history` | `PULSE_PHASE2_PYTEST_HISTORY_ROOT` |
| `urllib3_collection` | `PULSE_PHASE2_URLLIB3_COLLECTION_ROOT` |
| `urllib3_history` | `PULSE_PHASE2_URLLIB3_HISTORY_ROOT` |

Point each variable to the corresponding **unchanged Phase 2 collector output root**, preserving its relative paths. The manifest contains no user-specific absolute path. An authorized developer needs all four frozen roots plus this repository checkout; a missing root or file is a hard failure. The two cases are the only allowed population. The Phase 3/M1B secondary PR dataset is absent from this manifest.

Run from the repository root:

```powershell
python -m uv run python -m pulse.phase2_postgres verify
python -m uv run python -m pulse.phase2_postgres load --case pytest-8.0.0
python -m uv run python -m pulse.phase2_postgres load --case urllib3-2.0.0
python -m uv run python -m pulse.phase2_postgres load --all
python -m uv run python -m pulse.phase2_postgres reconcile
python -m uv run python -m pulse.phase2_postgres lineage
```

`load --all` verifies all inputs before any case write, then commits each case separately. If the second case fails, the first remains committed and the second rolls back. A failed case transaction leaves only a separate `rejected` load-audit record; preflight hash failures never open the database. Repeating an identical load returns `reused` after case-level reconciliation; a changed manifest digest on the same idempotency key is rejected without overwriting the trusted load. The source files remain authoritative; `pulse_dev` is their typed index.

The 142 entries comprise 54 task-attempt journals, 72 raw captures, two collection manifests, two history manifests, two case definitions, two reports, two accepted ledgers, two candidate baselines, two baseline manifests, one shared review ledger and one shared replay audit. The 72 raw captures are 48 release collection captures and 24 historical query/file captures. All are classified `collector`; the other manifest inputs are frozen derived documents, not additional collector captures.
