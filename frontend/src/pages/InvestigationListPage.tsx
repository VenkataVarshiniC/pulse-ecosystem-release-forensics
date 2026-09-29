import { Link } from 'react-router-dom';
import { apiPaths } from '../api/client';
import type { InvestigationList } from '../api/types';
import { PageHeading, Shell } from '../components/Shell';
import { EmptyState, ErrorState, LoadingState, Status } from '../components/States';
import { useApiData } from '../hooks/useApiData';
import { time } from '../utils/format';
import { routes } from '../utils/routes';

export function InvestigationListPage() {
  const { data, error, loading, retry } = useApiData<InvestigationList>(apiPaths.investigations());
  return <Shell>
    <PageHeading eyebrow="Operational investigations" title="Release investigations"
      description="Declared cohorts and published evidence snapshots. Select a release to inspect what is known, what remains uncertain, and why." />
    {loading && <LoadingState what="investigations" />}
    {error && <ErrorState error={error} retry={retry} />}
    {data && (data.items.length === 0
      ? <EmptyState title="No declared investigations">The API returned no published investigations.</EmptyState>
      : <section aria-label="Available investigations" className="section-block">
        <div className="section-title"><h2>Available cases</h2><span>{data.items.length} investigations</span></div>
        <div className="investigation-list">
          {data.items.map((item) => {
            const scope = { caseVersionId: item.scope.case_version_id, snapshotId: item.scope.analysis_snapshot_id };
            return <article className="investigation-row" key={item.scope.case_version_id}>
              <div><p className="eyebrow">{item.package_ecosystem} · {item.package_name}</p>
                <h3><Link to={routes.investigation(scope)}>{item.package_name} <span className="release-version">{item.release_version}</span></Link></h3>
                <p className="muted">{item.case_name}</p></div>
              <div className="investigation-meta"><span><b>{item.member_count}</b> declared repositories</span>
                <span>{time(item.window_start)} → {time(item.window_end)}</span>
                <Status value={item.scope.snapshot_state} /></div>
              <Link className="row-action" to={routes.investigation(scope)} aria-label={`Open ${item.case_name}`}>Open investigation <span aria-hidden="true">↗</span></Link>
            </article>;
          })}
        </div>
      </section>)}
  </Shell>;
}
