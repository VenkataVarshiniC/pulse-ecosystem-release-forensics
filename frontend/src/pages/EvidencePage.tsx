import { useState, type FormEvent } from 'react';
import { Link } from 'react-router-dom';
import { apiPaths } from '../api/client';
import type { EvidencePage as EvidenceResponse } from '../api/types';
import { PageHeading, Shell } from '../components/Shell';
import { EmptyState, ErrorState, LoadingState, ScopeMissing } from '../components/States';
import { useApiData } from '../hooks/useApiData';
import { useRepositoryScope } from '../hooks/useScope';
import { label, shortId, time } from '../utils/format';
import { routes } from '../utils/routes';

interface Filters { source_type: string; ref: string; path: string }
const blank: Filters = { source_type: '', ref: '', path: '' };

export function EvidencePage() {
  const scope = useRepositoryScope();
  const [draft, setDraft] = useState<Filters>(blank);
  const [filters, setFilters] = useState<Filters>(blank);
  const [cursor, setCursor] = useState<string | null>(null);
  const [history, setHistory] = useState<(string | null)[]>([]);
  const path = scope && apiPaths.evidence(scope, { ...filters, cursor, limit: 25 });
  const { data, error, loading, retry } = useApiData<EvidenceResponse>(path, scope ?? undefined);
  if (!scope) return <Shell><ScopeMissing /></Shell>;
  const crumbs = [{ label: 'Investigation', to: routes.investigation(scope) }, { label: 'Repository', to: routes.repository(scope) }, { label: 'Evidence' }];
  const grouped = data?.items.reduce<Record<string, EvidenceResponse['items']>>((groups, item) => {
    (groups[item.source_type] ??= []).push(item);
    return groups;
  }, {});
  function applyFilters(event: FormEvent) {
    event.preventDefault();
    setFilters({ ...draft });
    setCursor(null);
    setHistory([]);
  }
  return <Shell crumbs={crumbs}>
    <PageHeading eyebrow="Evidence explorer" title="Captured evidence"
      description="Source captures in the selected repository and snapshot. Grouping is by source, not event sequence; record identifiers are pagination cursors, not timestamps." />
    <form className="filter-bar" onSubmit={applyFilters} aria-label="Evidence filters">
      <label>Source type<input value={draft.source_type} onChange={(e) => setDraft({ ...draft, source_type: e.target.value })} placeholder="Exact source type" /></label>
      <label>Repository ref<input value={draft.ref} onChange={(e) => setDraft({ ...draft, ref: e.target.value })} placeholder="Exact ref" /></label>
      <label>Path<input value={draft.path} onChange={(e) => setDraft({ ...draft, path: e.target.value })} placeholder="Exact path" /></label>
      <button type="submit" className="button">Apply filters</button>
      <button type="button" className="button button--quiet" onClick={() => { setDraft(blank); setFilters(blank); setCursor(null); setHistory([]); }}>Clear</button>
    </form>
    {loading && <LoadingState what="evidence" />}
    {error && <ErrorState error={error} retry={retry} />}
    {data && <>
      <div className="section-title"><h2>Source captures</h2><span>{data.items.length} on this page</span></div>
      {data.items.length === 0 ? <EmptyState title="No captures on this page">No evidence matches this exact filter within the selected snapshot. Review source task outcomes before drawing a conclusion.</EmptyState>
        : Object.entries(grouped ?? {}).map(([source, items]) => <section className="section-block" key={source} aria-label={`${label(source)} evidence`}>
          <div className="section-title"><h3>{label(source)}</h3><span>{items.length} captures</span></div>
          <div className="table-scroll"><table><thead><tr><th scope="col">Artifact</th><th scope="col">Capture</th><th scope="col">Ref / observation</th><th scope="col">Source event</th><th scope="col">Retrieved</th><th scope="col">Digest</th></tr></thead><tbody>
            {items.map((item) => <tr key={item.artifact_id}>
              <th scope="row"><Link to={routes.artifact(scope, item.artifact_id)}>{label(item.artifact_type)}</Link></th>
              <td>{label(item.capture_method)}</td>
              <td>{item.repository_ref ?? 'Ref unavailable'}<small>{item.observations.length ? item.observations.map((o) => `${label(o.observation_type)} · ${o.path_ref ?? 'path unavailable'}`).join('; ') : 'No observation linked'}</small></td>
              <td>{time(item.source_event_time)}</td><td>{time(item.retrieved_at)}</td>
              <td title={item.content_sha256} className="mono">{shortId(item.content_sha256)}…</td>
            </tr>)}
          </tbody></table></div>
        </section>)}
      <nav className="pagination" aria-label="Evidence pages">
        <button type="button" className="button button--quiet" disabled={history.length === 0} onClick={() => { setCursor(history.at(-1) ?? null); setHistory(history.slice(0, -1)); }}>Previous page</button>
        <span>Page {history.length + 1} · server page size 25</span>
        <button type="button" className="button button--quiet" disabled={!data.next_cursor} onClick={() => { setHistory([...history, cursor]); setCursor(data.next_cursor); }}>Next page</button>
      </nav>
    </>}
  </Shell>;
}
