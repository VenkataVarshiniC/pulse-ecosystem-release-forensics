import { Link } from 'react-router-dom';
import { apiPaths } from '../api/client';
import type { CandidatesResponse, RepositoryDetail } from '../api/types';
import { PageHeading, Shell } from '../components/Shell';
import { EmptyState, ErrorState, LoadingState, ScopeMissing, Status } from '../components/States';
import { useApiData } from '../hooks/useApiData';
import { useRepositoryScope } from '../hooks/useScope';
import { label, time } from '../utils/format';
import { routes } from '../utils/routes';

export function RepositoryPage() {
  const scope = useRepositoryScope();
  const { data, error, loading, retry } = useApiData<RepositoryDetail>(scope && apiPaths.repository(scope), scope ?? undefined);
  const candidates = useApiData<CandidatesResponse>(scope ? apiPaths.candidates(scope) : null, scope ?? undefined);
  if (!scope) return <Shell><ScopeMissing /></Shell>;
  const crumbs = [{ label: 'Investigation', to: routes.investigation(scope) }, { label: data?.member.repository_name || 'Repository' }];
  return <Shell crumbs={crumbs}>
    {loading && <LoadingState what="repository investigation" />}
    {error && <ErrorState error={error} retry={retry} />}
    {data && <>
      <PageHeading eyebrow="Repository investigation" title={data.member.repository_name}
        description="Declaration, historical context, findings, and detector candidates remain separate evidence questions." />
      <div className="fact-strip"><div><span>Cohort identity</span><strong>{label(data.member.identity_status)}</strong></div>
        <div><span>Eligibility</span><strong>{label(data.member.eligibility_status)}</strong></div>
        <div><span>Candidate firings</span><strong>{data.candidate_count}</strong></div>
        <div><span>Snapshot state</span><Status value={data.scope.snapshot_state} /></div></div>
      <div className="quick-links"><Link className="button" to={routes.evidence(scope)}>Explore evidence →</Link><a className="text-link" href="#findings">Jump to findings</a></div>
      <div className="two-column">
        <section className="section-block"><div className="section-title"><h2>Dependency observations</h2><span>{data.observations.length} recorded</span></div>
          <p className="section-intro">A declaration is a constraint in a repository file. A resolved version is a separate observed fact.</p>
          {data.observations.length === 0 ? <EmptyState title="No observation recorded">Inspect source task outcomes and captured evidence before interpreting this gap.</EmptyState>
            : <div className="record-list">{data.observations.map((o) => <div className="record" key={o.observation_id}>
              <div className="record-head"><strong>{label(o.observation_type)}</strong><span>{label(o.quality_status)}</span></div>
              <dl className="detail-grid"><div><dt>Declared constraint</dt><dd>{o.declared_constraint ?? 'Not recorded'}</dd></div><div><dt>Resolved version</dt><dd>{o.resolved_version ?? 'Not observed'}</dd></div><div><dt>Ref / path</dt><dd>{o.repository_ref ?? 'Ref unavailable'} · {o.path_ref ?? 'Path unavailable'}</dd></div><div><dt>Observation time</dt><dd>{time(o.observation_time)}</dd></div></dl>
              <Link className="text-link" to={routes.artifact(scope, o.artifact_id)}>Inspect source artifact →</Link>
            </div>)}</div>}
        </section>
        <section className="section-block"><div className="section-title"><h2>Historical context</h2><span>{data.historical_pairs.length} pairs</span></div>
          {data.historical_pairs.length === 0 ? <EmptyState title="No historical pair recorded">An absent pair does not establish a pre-release state.</EmptyState>
            : <div className="record-list">{data.historical_pairs.map((pair) => <div className="record" key={pair.historical_pair_id}>
              <div className="record-head"><Status value={pair.pair_status} /><span>{pair.path_ref}</span></div>
              <p>{label(pair.reason)}</p><small>Before: {pair.before_observation_id ? 'recorded' : 'unresolved'} · After: {pair.after_observation_id ? 'recorded' : 'unresolved'} · Method {pair.method_version}</small>
            </div>)}</div>}
          <p className="method-note">AFTER_ONLY means a later declaration was observed without a qualifying earlier anchor. It does not prove earlier absence.</p>
        </section>
      </div>
      <section className="section-block" id="findings"><div className="section-title"><h2>Finding questions</h2><span>{data.findings.length} categories</span></div>
        {data.findings.length === 0 ? <EmptyState title="No findings returned">The selected snapshot contains no finding records for this member.</EmptyState>
          : <div className="table-scroll"><table><thead><tr><th scope="col">Category</th><th scope="col">Finding</th><th scope="col">Evidence sufficiency</th><th scope="col">Reason</th><th scope="col">Detail</th></tr></thead><tbody>
            {data.findings.map((f) => <tr key={f.finding_id}><th scope="row">{label(f.lifecycle_category)}</th><td><Status value={f.finding_status} /></td><td><Status value={f.sufficiency_status} /></td><td>{label(f.reason_code)}</td><td><Link className="text-link" to={routes.finding(scope, f.finding_id)}>Inspect finding →</Link></td></tr>)}
          </tbody></table></div>}
      </section>
      <div className="two-column"><section className="section-block"><div className="section-title"><h2>Source task outcomes</h2></div>
        {data.source_states.length === 0 ? <EmptyState title="No source task states returned">Collection coverage is unavailable for this member.</EmptyState> :
          <div className="record-list">{data.source_states.map((s) => <div className="source-row" key={s.collection_task_id}><strong>{label(s.source_type)}</strong><span>{label(s.terminal_status)}</span><small>{s.required ? 'Required' : 'Optional'} · {label(s.task_type)}{s.error_class ? ` · ${label(s.error_class)}` : ''}</small></div>)}</div>}
      </section><section className="section-block"><div className="section-title"><h2>Detector candidates</h2></div>
        {data.candidate_count === 0 ? <EmptyState title="No candidate emitted">This is a detector result for the selected snapshot, not evidence that no incident occurred.</EmptyState>
          : <><p>{data.candidate_count} candidate firing{data.candidate_count === 1 ? '' : 's'} recorded. Each firing has its own review record; firings may share a source artifact.</p>
            {candidates.loading && <LoadingState what="candidate list" />}
            {candidates.error && <ErrorState error={candidates.error} retry={candidates.retry} />}
            {candidates.data && <div className="record-list">{candidates.data.items.map((candidate) => <div className="source-row" key={candidate.candidate_id}>
              <Link to={routes.candidate(scope, candidate.candidate_id)}>{label(candidate.lifecycle_category)} →</Link>
              <span>{candidate.review ? <Status value={candidate.review.decision} /> : 'Not reviewed'}</span>
              <small>Artifact {candidate.artifact_id.slice(0, 8)} · {candidate.review?.review_origin === 'INHERITED' ? 'Inherited review' : 'Review status recorded'}</small>
            </div>)}</div>}</>}
      </section></div>
    </>}
  </Shell>;
}
