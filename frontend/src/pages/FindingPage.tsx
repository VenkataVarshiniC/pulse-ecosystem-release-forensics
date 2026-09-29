import { Link, useParams } from 'react-router-dom';
import { apiPaths } from '../api/client';
import type { Finding } from '../api/types';
import { PageHeading, Shell } from '../components/Shell';
import { EmptyState, ErrorState, LoadingState, ScopeMissing, Status } from '../components/States';
import { useApiData } from '../hooks/useApiData';
import { useRepositoryScope } from '../hooks/useScope';
import { label, shortId } from '../utils/format';
import { routes } from '../utils/routes';

export function FindingPage() {
  const scope = useRepositoryScope();
  const { findingId } = useParams();
  const { data, error, loading, retry } = useApiData<Finding>(scope && findingId ? apiPaths.finding(scope, findingId) : null);
  if (!scope || !findingId) return <Shell><ScopeMissing /></Shell>;
  const crumbs = [{ label: 'Investigation', to: routes.investigation(scope) }, { label: 'Repository', to: routes.repository(scope) }, { label: data ? label(data.lifecycle_category) : 'Finding' }];
  return <Shell crumbs={crumbs}>
    {loading && <LoadingState what="finding" />}{error && <ErrorState error={error} retry={retry} />}
    {data && <>
      <PageHeading eyebrow="Finding detail" title={label(data.lifecycle_category)} description={`Question: ${label(data.question_id)}`}
        aside={<Status value={data.finding_status} />} />
      <div className={`interpretation interpretation--${data.finding_status === 'UNKNOWN' ? 'unknown' : 'bounded'}`}>
        <strong>{data.finding_status === 'UNKNOWN' ? 'The question remains unanswered' : data.finding_status === 'NO_QUALIFYING_EVIDENCE_FOUND' ? 'A bounded negative finding' : 'Qualifying evidence recorded'}</strong>
        <p>{data.finding_status === 'UNKNOWN'
          ? 'PULSE does not have sufficient qualifying evidence to support a bounded conclusion for this question.'
          : data.finding_status === 'NO_QUALIFYING_EVIDENCE_FOUND'
            ? 'Within the declared evidence scope and method, no qualifying evidence was found. This does not establish that the event never happened.'
            : 'Qualifying evidence was recorded within the declared scope. Inspect the support links and provenance below.'}</p>
      </div>
      <div className="two-column"><section className="section-block"><div className="section-title"><h2>Assessment</h2></div>
        <dl className="detail-grid"><div><dt>Finding status</dt><dd><Status value={data.finding_status} /></dd></div><div><dt>Evidence sufficiency</dt><dd><Status value={data.sufficiency_status} /></dd></div>
          <div><dt>Finding reason</dt><dd>{label(data.reason_code)}</dd></div><div><dt>Sufficiency reason</dt><dd>{label(data.sufficiency_reason_code)}</dd></div>
          <div><dt>Confidence basis</dt><dd>{data.confidence_level ? label(data.confidence_level) : 'Not assigned'}</dd></div><div><dt>Rule / source set</dt><dd>{data.rule_version} / {data.required_source_set_version}</dd></div></dl>
        <p className="method-note">Lifecycle categories are forensic evidence questions, not required chronological stages or causal claims.</p>
      </section><section className="section-block"><div className="section-title"><h2>Source requirements</h2></div>
        {data.source_reasons.length === 0 ? <EmptyState title="No source reason recorded">The API did not return a source-specific reason for this finding.</EmptyState>
          : <div className="record-list">{data.source_reasons.map((reason, index) => <div className="source-row" key={`${reason.source_type}-${index}`}><strong>{label(reason.source_type)}</strong><span>{label(reason.reason_code)}</span><small>{reason.required ? 'Required source' : 'Optional source'}</small></div>)}</div>}
      </section></div>
      <section className="section-block"><div className="section-title"><h2>Recorded support</h2></div>
        {data.artifact_support_ids.length + data.observation_support_ids.length + data.review_support_ids.length === 0
          ? <EmptyState title="No explicit support link recorded">Do not infer a source chain from category or status alone. <Link to={routes.evidence(scope)}>Explore available evidence</Link>.</EmptyState>
          : <div className="record-list">
            {data.artifact_support_ids.map((id) => <p key={id}>Artifact <Link className="text-link" to={routes.artifact(scope, id)}>{shortId(id)} → provenance</Link></p>)}
            {data.observation_support_ids.map((id) => <p key={id}>Observation {shortId(id)} · <Link className="text-link" to={routes.evidence(scope)}>Inspect repository evidence</Link></p>)}
            {data.review_support_ids.map((id) => <p key={id}>Review {shortId(id)} · support ID recorded; direct review detail is not supplied by this API.</p>)}
          </div>}
      </section>
    </>}
  </Shell>;
}
