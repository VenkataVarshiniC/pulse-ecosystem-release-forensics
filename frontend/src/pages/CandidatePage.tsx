import { Link, useParams } from 'react-router-dom';
import { apiPaths } from '../api/client';
import type { Candidate, CandidatesResponse } from '../api/types';
import { PageHeading, Shell } from '../components/Shell';
import { EmptyState, ErrorState, LoadingState, ScopeMissing, Status } from '../components/States';
import { useApiData } from '../hooks/useApiData';
import { useRepositoryScope } from '../hooks/useScope';
import { label, shortId, time } from '../utils/format';
import { routes } from '../utils/routes';

export function CandidatePage() {
  const scope = useRepositoryScope();
  const { candidateId } = useParams();
  const detail = useApiData<Candidate>(scope && candidateId ? apiPaths.candidate(scope, candidateId) : null);
  const peers = useApiData<CandidatesResponse>(scope ? apiPaths.candidates(scope) : null, scope ?? undefined);
  if (!scope || !candidateId) return <Shell><ScopeMissing /></Shell>;
  const candidate = detail.data;
  const sharing = peers.data?.items.filter((other) => other.artifact_id === candidate?.artifact_id && other.candidate_id !== candidate?.candidate_id) ?? [];
  const crumbs = [{ label: 'Investigation', to: routes.investigation(scope) }, { label: 'Repository', to: routes.repository(scope) }, { label: 'Candidate' }];
  return <Shell crumbs={crumbs}>
    {detail.loading && <LoadingState what="candidate" />}{detail.error && <ErrorState error={detail.error} retry={detail.retry} />}
    {candidate && <>
      <PageHeading eyebrow="Detector candidate · read only" title={label(candidate.lifecycle_category)}
        description={`Candidate firing ${shortId(candidate.candidate_id)} · ${label(candidate.source_origin)} source`} aside={candidate.review ? <Status value={candidate.review.decision} /> : <span className="status status--neutral">Not reviewed</span>} />
      <div className="interpretation interpretation--unknown"><strong>Review record, not an accepted finding</strong>
        <p>This detector firing is separate from a lifecycle finding. Published review records are read-only; no decision can be submitted here.</p></div>
      <div className="two-column"><section className="section-block"><div className="section-title"><h2>Candidate context</h2></div>
        <dl className="detail-grid"><div><dt>Origin</dt><dd>{label(candidate.source_origin)}</dd></div><div><dt>Emission status</dt><dd>{label(candidate.candidate_status)}</dd></div>
          <div><dt>Rule</dt><dd>{candidate.candidate_rule_id} · {candidate.candidate_rule_version}</dd></div><div><dt>Candidate reason</dt><dd>{candidate.candidate_reason}</dd></div>
          <div><dt>Source span</dt><dd>{candidate.span_ref}</dd></div><div><dt>Fingerprint</dt><dd className="mono">{shortId(candidate.candidate_fingerprint)}…</dd></div></dl>
        <Link className="button" to={routes.artifact(scope, candidate.artifact_id)}>Trace source artifact →</Link>
      </section><section className="section-block"><div className="section-title"><h2>Review provenance</h2><span>Read only</span></div>
        {candidate.review ? <><p><Status value={candidate.review.decision} /> · {label(candidate.review.reason_code)}</p>
          <p>{candidate.review.review_origin === 'INHERITED' ? 'Inherited review: this decision reuses a prior governed review. It was not made by the current viewer or in this published snapshot.' : 'Direct review recorded in the governed source.'}</p>
          <dl className="detail-grid"><div><dt>Review origin</dt><dd>{label(candidate.review.review_origin)}</dd></div><div><dt>Reviewed at</dt><dd>{time(candidate.review.reviewed_at)}</dd></div>
            <div><dt>Original review</dt><dd title={candidate.original_review_id ?? undefined}>{candidate.original_review_id ? shortId(candidate.original_review_id) : 'Not inherited'}</dd></div><div><dt>Original candidate</dt><dd title={candidate.original_candidate_id ?? undefined}>{candidate.original_candidate_id ? shortId(candidate.original_candidate_id) : 'Not inherited'}</dd></div><div><dt>Review note</dt><dd>{candidate.review.review_note ?? 'No note recorded'}</dd></div></dl></>
          : <EmptyState title="No review recorded">The candidate has no review decision in this snapshot.</EmptyState>}
        <p className="method-note">Review write enabled: {candidate.review_write_enabled ? 'API reports eligible, but this interface has no authorized write workflow.' : 'No — this published record is immutable.'}</p>
      </section></div>
      <section className="section-block"><div className="section-title"><h2>Shared source artifact</h2></div>
        {peers.loading && <LoadingState what="related candidate firings" />}
        {peers.error && <ErrorState error={peers.error} retry={peers.retry} />}
        {peers.data && (sharing.length === 0 ? <p>No other candidate firing in this repository is linked to this artifact.</p>
          : <><p>{sharing.length + 1} candidate firings reference one captured artifact. They are not independent source incidents.</p>
            <ul>{sharing.map((other) => <li key={other.candidate_id}><Link to={routes.candidate(scope, other.candidate_id)}>{label(other.lifecycle_category)} · {shortId(other.candidate_id)}</Link></li>)}</ul></>)}
      </section>
    </>}
  </Shell>;
}
