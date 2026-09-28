-- History raw snapshots carry source task/attempt IDs but have no separate
-- frozen planned-task journal. Preserve IDs without inventing planned tasks.
BEGIN;
ALTER TABLE core.evidence_artifact ADD COLUMN source_task_key text;
ALTER TABLE core.evidence_artifact ADD COLUMN source_attempt_key text;
INSERT INTO public.schema_migrations(version, description)
VALUES (4, 'historical capture task and attempt source keys');
COMMIT;
