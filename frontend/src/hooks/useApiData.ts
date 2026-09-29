import { useEffect, useState } from 'react';
import { ApiError, getJson } from '../api/client';
import type { Scope } from '../api/types';

interface RequestState<T> {
  key: string;
  data?: T;
  error?: ApiError;
  status: 'success' | 'error';
}

function responseScope(value: unknown): Scope | null {
  if (!value || typeof value !== 'object') return null;
  const data = value as { scope?: Scope; investigation?: { scope?: Scope } };
  return data.scope ?? data.investigation?.scope ?? null;
}

export function useApiData<T>(
  path: string | null,
  expected?: { caseVersionId: string; snapshotId: string },
) {
  const [attempt, setAttempt] = useState(0);
  const [state, setState] = useState<RequestState<T> | null>(null);
  const key = path ? `${path}::${attempt}` : null;
  const expectedCase = expected?.caseVersionId;
  const expectedSnapshot = expected?.snapshotId;

  useEffect(() => {
    if (!path || !key) return;
    const controller = new AbortController();
    getJson<T>(path, controller.signal)
      .then((data) => {
        const scope = responseScope(data);
        if (scope && expectedCase && expectedSnapshot &&
            (scope.case_version_id !== expectedCase ||
             scope.analysis_snapshot_id !== expectedSnapshot)) {
          throw new ApiError(
            'PROVENANCE_MISMATCH', 'The API returned a different investigation snapshot.', 409,
          );
        }
        setState({ key, status: 'success', data });
      })
      .catch((error: unknown) => {
        if (controller.signal.aborted) return;
        setState({
          key,
          status: 'error',
          error: error instanceof ApiError
            ? error
            : new ApiError('API_ERROR', 'The request failed.', null),
        });
      });
    return () => controller.abort();
  }, [path, key, expectedCase, expectedSnapshot]);

  const current = key && state?.key === key ? state : null;
  return {
    data: current?.data,
    error: current?.error,
    loading: Boolean(key) && !current,
    retry: () => setAttempt((value) => value + 1),
  };
}
