import { Link, useParams } from 'react-router-dom';
import { apiPaths } from '../api/client';
import type { Provenance } from '../api/types';
import { PageHeading, Shell } from '../components/Shell';
import { EmptyState, ErrorState, LoadingState, ScopeMissing } from '../components/States';
import { useApiData } from '../hooks/useApiData';
import { useRepositoryScope } from '../hooks/useScope';
import { label, shortId, time } from '../utils/format';
import { routes } from '../utils/routes';

function publicUrl(value: string | null): string | null {
  if (!value) return null;
  try {
    const url = new URL(value);
    return url.protocol === 'https:' && !url.username && !url.password &&
      !['localhost', 'host.docker.internal'].includes(url.hostname) &&
      ![...url.searchParams.keys()].some((key) => /token|key|auth|secret|password|signature|credential/i.test(key))
      ? url.href : null;
  } catch { return null; }
}

export function ArtifactPage() {
  const scope = useRepositoryScope();
  const { artifactId } = useParams();
  const { data, error, loading, retry } = useApiData<Provenance>(scope && artifactId ? apiPaths.artifact(scope, artifactId) : null, scope ?? undefined);
  if (!scope || !artifactId) return <Shell><ScopeMissing /></Shell>;
  const crumbs = [{ label: 'Investigation', to: routes.investigation(scope) }, { label: 'Repository', to: routes.repository(scope) }, { label: 'Evidence', to: routes.evidence(scope) }, { label: 'Provenance' }];
  const locator = publicUrl(data?.public_locator ?? null);
  return <Shell crumbs={crumbs}>
    {loading && <LoadingState what="artifact provenance" />}{error && <ErrorState error={error} retry={retry} />}
    {data && <>
      <PageHeading eyebrow="Artifact provenance" title={label(data.artifact_type)}
        description={`Captured ${label(data.source_type)} evidence · ${shortId(data.artifact_id)}`} aside={<span className="status status--neutral">{label(data.capture_method)}</span>} />
      <div className="provenance-chain" aria-label="Provenance chain"><span>Finding / candidate</span><span aria-hidden="true">→</span><span>Artifact</span><span aria-hidden="true">→</span><span>Source / ref</span><span aria-hidden="true">→</span><span>Capture context</span></div>
      <div className="two-column"><section className="section-block"><div className="section-title"><h2>Source identity</h2></div>
        <dl className="detail-grid"><div><dt>Source type</dt><dd>{label(data.source_type)}</dd></div><div><dt>Provider</dt><dd>{label(data.source_provider)}</dd></div>
          <div><dt>Repository ref</dt><dd>{data.repository_ref ?? 'Ref unavailable'}</dd></div><div><dt>Capture method</dt><dd>{label(data.capture_method)}</dd></div></dl>
        {locator ? <p><a className="button" href={locator} target="_blank" rel="noopener noreferrer">Open public source ↗</a></p>
          : <EmptyState title="Direct source link unavailable">The API supplied no safe primary locator for this artifact. Related public references, if recorded, appear below.</EmptyState>}
        {data.external_public_locators.length > 0 && <div><h3>Other public references</h3><ul>{data.external_public_locators.map((value) => <li key={value}>{publicUrl(value) ? <a href={publicUrl(value)!} target="_blank" rel="noopener noreferrer">Open public reference ↗</a> : 'Reference unavailable'}</li>)}</ul></div>}
      </section><section className="section-block"><div className="section-title"><h2>Capture record</h2></div>
        <dl className="detail-grid"><div><dt>Source event time</dt><dd>{time(data.source_event_time)}</dd></div><div><dt>Retrieved at</dt><dd>{time(data.retrieved_at)}</dd></div>
          <div><dt>Collection run kind</dt><dd>{data.collection_run_kind ? label(data.collection_run_kind) : 'Not recorded'}</dd></div><div><dt>Task status</dt><dd>{data.task_status ? label(data.task_status) : 'Not recorded'}</dd></div>
          <div><dt>Run status</dt><dd>{data.run_status ? label(data.run_status) : 'Not recorded'}</dd></div><div><dt>Collection task</dt><dd title={data.collection_task_id ?? undefined}>{data.collection_task_id ? shortId(data.collection_task_id) : 'Not recorded'}</dd></div><div><dt>Collection run</dt><dd title={data.collection_run_id ?? undefined}>{data.collection_run_id ? shortId(data.collection_run_id) : 'Not recorded'}</dd></div><div><dt>Content SHA-256</dt><dd className="mono break-all">{data.content_sha256}</dd></div></dl>
        <p className="method-note">Retrieval time records when PULSE obtained this capture; it is not substituted for an unavailable source event time. Connector-assisted and fixture captures do not demonstrate unattended collector operation.</p>
      </section></div>
      <section className="section-block"><div className="section-title"><h2>Recorded links</h2></div>
        {data.linked_candidate_ids.length + data.linked_finding_ids.length === 0 ? <EmptyState title="No candidate or finding link returned">The artifact remains inspectable evidence, but no support edge is recorded in this response.</EmptyState>
          : <div className="record-list">{data.linked_candidate_ids.map((id) => <p key={id}>Candidate <Link className="text-link" to={routes.candidate(scope, id)}>{shortId(id)} → review context</Link></p>)}
            {data.linked_finding_ids.map((id) => <p key={id}>Finding <Link className="text-link" to={routes.finding(scope, id)}>{shortId(id)} → assessment</Link></p>)}</div>}
      </section>
    </>}
  </Shell>;
}
