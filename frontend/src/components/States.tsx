import type { ReactNode } from 'react';
import { Link } from 'react-router-dom';
import { ApiError } from '../api/client';
import type { FindingStatus, SufficiencyStatus } from '../api/types';

const labels: Record<string, string> = {
  UNKNOWN: 'UNKNOWN · Unanswered',
  NO_QUALIFYING_EVIDENCE_FOUND: 'Bounded NO',
  QUALIFYING_EVIDENCE: 'Qualifying evidence',
  SUFFICIENT: 'Sufficient',
  INSUFFICIENT: 'Evidence incomplete',
  SOURCE_UNAVAILABLE: 'Source unavailable',
  CONFLICTING: 'Conflicting evidence',
  ACCEPT: 'Accepted',
  REJECT: 'Rejected',
  NEEDS_EVIDENCE: 'Needs evidence',
  PUBLISHED_VALIDATION: 'Published validation',
  DRAFT: 'Draft',
};

export function Status({ value }: { value: string | FindingStatus | SufficiencyStatus }) {
  const tone = value === 'UNKNOWN' || value === 'INSUFFICIENT' || value === 'SOURCE_UNAVAILABLE'
    || value === 'NEEDS_EVIDENCE' ? 'unknown'
    : value === 'NO_QUALIFYING_EVIDENCE_FOUND' ? 'bounded'
      : value === 'QUALIFYING_EVIDENCE' || value === 'SUFFICIENT' || value === 'ACCEPT'
        ? 'positive' : value === 'REJECT' ? 'rejected' : 'neutral';
  return <span className={`status status--${tone}`}>{labels[value] || value}</span>;
}

export function LoadingState({ what }: { what: string }) {
  return (
    <div className="state-panel" role="status" aria-live="polite">
      <span className="loading-mark" aria-hidden="true" />
      <div><strong>Loading {what}</strong><p>Reading the selected investigation snapshot.</p></div>
    </div>
  );
}

const errorCopy: Record<string, string> = {
  INVALID_SNAPSHOT: 'That snapshot is not available for this investigation.',
  NOT_FOUND_IN_SELECTED_COHORT: 'This item is not in the selected repository cohort.',
  PROVENANCE_MISMATCH: 'The selected source link could not be verified.',
  DATABASE_UNAVAILABLE: 'The local evidence database is unavailable.',
  DATABASE_ERROR: 'The database could not complete this request.',
  NETWORK_ERROR: 'The local PULSE API could not be reached.',
  SOURCE_UNAVAILABLE: 'A required source is unavailable.',
  STALE_REVIEW: 'The review changed. Reload before acting.',
  PUBLISHED_IMMUTABLE: 'Published candidate reviews are read-only.',
  INVALID_DECISION_REASON: 'A reason is required for a review decision.',
  REVIEWER_NOT_AUTHORIZED: 'Review authority is not configured.',
};

export function ErrorState({ error, retry }: { error: ApiError; retry?: () => void }) {
  return (
    <div className="state-panel state-panel--error" role="alert">
      <div>
        <strong>Evidence could not be loaded</strong>
        <p>{errorCopy[error.code] || error.message}</p>
        <p className="state-code">{error.code}</p>
        <div className="state-actions">
          {retry && <button type="button" className="button button--quiet" onClick={retry}>Try again</button>}
          <Link to="/investigations" className="text-link">Back to investigations</Link>
        </div>
      </div>
    </div>
  );
}

export function EmptyState({ title, children }: { title: string; children: ReactNode }) {
  return <div className="state-panel state-panel--empty"><div><strong>{title}</strong><p>{children}</p></div></div>;
}

export function ScopeMissing() {
  return (
    <div className="state-panel state-panel--error" role="alert">
      <div>
        <strong>Investigation context is missing</strong>
        <p>Open a published case from the investigation list to retain its exact snapshot.</p>
        <Link className="text-link" to="/investigations">Back to investigations</Link>
      </div>
    </div>
  );
}
