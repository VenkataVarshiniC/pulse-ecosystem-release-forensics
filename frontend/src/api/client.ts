import type { UUID } from './types';

const configuredBase = import.meta.env.VITE_PULSE_API_BASE_URL || 'http://127.0.0.1:8000/api/v1';
export const API_BASE_URL = configuredBase.replace(/\/$/, '');

export class ApiError extends Error {
  constructor(
    public readonly code: string,
    message: string,
    public readonly status: number | null,
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

export interface ScopeRef {
  caseVersionId: UUID;
  snapshotId: UUID;
}

export interface RepositoryRef extends ScopeRef {
  repositoryId: UUID;
}

const query = (snapshotId: UUID, extra: Record<string, string | number | null | undefined> = {}) => {
  const params = new URLSearchParams({ snapshot_id: snapshotId });
  for (const [key, value] of Object.entries(extra)) {
    if (value !== null && value !== undefined && value !== '') params.set(key, String(value));
  }
  return `?${params.toString()}`;
};

const repositoryBase = ({ caseVersionId, repositoryId }: RepositoryRef) =>
  `/investigations/${caseVersionId}/repositories/${repositoryId}`;

export const apiPaths = {
  investigations: () => '/investigations',
  investigation: ({ caseVersionId, snapshotId }: ScopeRef) =>
    `/investigations/${caseVersionId}${query(snapshotId)}`,
  repository: (scope: RepositoryRef) => `${repositoryBase(scope)}${query(scope.snapshotId)}`,
  evidence: (
    scope: RepositoryRef,
    options: { cursor?: UUID | null; limit?: number; source_type?: string; ref?: string; path?: string } = {},
  ) => `${repositoryBase(scope)}/evidence${query(scope.snapshotId, options)}`,
  findings: (scope: RepositoryRef) => `${repositoryBase(scope)}/findings${query(scope.snapshotId)}`,
  finding: (scope: RepositoryRef, id: UUID) =>
    `${repositoryBase(scope)}/findings/${id}${query(scope.snapshotId)}`,
  candidates: (scope: RepositoryRef) => `${repositoryBase(scope)}/candidates${query(scope.snapshotId)}`,
  candidate: (scope: RepositoryRef, id: UUID) =>
    `${repositoryBase(scope)}/candidates/${id}${query(scope.snapshotId)}`,
  artifact: (scope: RepositoryRef, id: UUID) =>
    `${repositoryBase(scope)}/artifacts/${id}${query(scope.snapshotId)}`,
};

export async function getJson<T>(path: string, signal?: AbortSignal): Promise<T> {
  let response: Response;
  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      signal,
      headers: { Accept: 'application/json' },
    });
  } catch (error) {
    if (error instanceof DOMException && error.name === 'AbortError') throw error;
    throw new ApiError('NETWORK_ERROR', 'Cannot reach the PULSE API. Check the local server.', null);
  }
  let body: unknown;
  try {
    body = await response.json();
  } catch {
    throw new ApiError('INVALID_RESPONSE', 'The API returned an unreadable response.', response.status);
  }
  if (!response.ok) {
    const problem = body as { code?: string; message?: string };
    throw new ApiError(problem.code || 'API_ERROR', problem.message || 'The request failed.', response.status);
  }
  return body as T;
}
