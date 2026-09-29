import type { RepositoryRef, ScopeRef } from '../api/client';
import type { UUID } from '../api/types';

const snapshot = (snapshotId: UUID) => `?snapshot_id=${encodeURIComponent(snapshotId)}`;
const repositoryBase = ({ caseVersionId, repositoryId }: RepositoryRef) =>
  `/investigations/${caseVersionId}/repositories/${repositoryId}`;

export const routes = {
  investigations: '/investigations',
  investigation: ({ caseVersionId, snapshotId }: ScopeRef) =>
    `/investigations/${caseVersionId}${snapshot(snapshotId)}`,
  repository: (scope: RepositoryRef) => `${repositoryBase(scope)}${snapshot(scope.snapshotId)}`,
  evidence: (scope: RepositoryRef) => `${repositoryBase(scope)}/evidence${snapshot(scope.snapshotId)}`,
  finding: (scope: RepositoryRef, id: UUID) =>
    `${repositoryBase(scope)}/findings/${id}${snapshot(scope.snapshotId)}`,
  candidate: (scope: RepositoryRef, id: UUID) =>
    `${repositoryBase(scope)}/candidates/${id}${snapshot(scope.snapshotId)}`,
  artifact: (scope: RepositoryRef, id: UUID) =>
    `${repositoryBase(scope)}/artifacts/${id}${snapshot(scope.snapshotId)}`,
};
