import { useParams, useSearchParams } from 'react-router-dom';
import type { RepositoryRef, ScopeRef } from '../api/client';

const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

export function useCaseScope(): ScopeRef | null {
  const { caseVersionId } = useParams();
  const [search] = useSearchParams();
  const snapshotId = search.get('snapshot_id');
  if (!caseVersionId || !snapshotId || !UUID.test(caseVersionId) || !UUID.test(snapshotId)) {
    return null;
  }
  return { caseVersionId, snapshotId };
}

export function useRepositoryScope(): RepositoryRef | null {
  const caseScope = useCaseScope();
  const { repositoryId } = useParams();
  if (!caseScope || !repositoryId || !UUID.test(repositoryId)) return null;
  return { ...caseScope, repositoryId };
}
