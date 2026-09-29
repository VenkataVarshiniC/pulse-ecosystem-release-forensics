import { Link } from 'react-router-dom';
import { apiPaths } from '../api/client';
import type { InvestigationDetail } from '../api/types';
import { PageHeading, Shell } from '../components/Shell';
import { EmptyState, ErrorState, LoadingState, ScopeMissing, Status } from '../components/States';
import { useApiData } from '../hooks/useApiData';
import { useCaseScope } from '../hooks/useScope';
import { shortId, time } from '../utils/format';
import { routes } from '../utils/routes';

export function InvestigationOverviewPage() {
  const scope = useCaseScope();
  const { data, error, loading, retry } = useApiData<InvestigationDetail>(scope && apiPaths.investigation(scope), scope ?? undefined);
  if (!scope) return <Shell><ScopeMissing /></Shell>;
  const item = data?.investigation;
  return <Shell crumbs={[{ label: item?.package_name || 'Investigation' }]}>
    {loading && <LoadingState what="investigation overview" />}
    {error && <ErrorState error={error} retry={retry} />}
    {item && <>
      <PageHeading eyebrow="Investigation overview" title={`${item.package_name} ${item.release_version}`}
        description={item.case_name} aside={<Status value={item.scope.snapshot_state} />} />
      <div className="fact-strip">
        <div><span>Declared cohort</span><strong>{item.member_count} repositories</strong></div>
        <div><span>Investigation window</span><strong>{time(item.window_start)} – {time(item.window_end)}</strong></div>
        <div><span>Snapshot</span><strong title={item.scope.analysis_snapshot_id}>{shortId(item.scope.analysis_snapshot_id)}</strong></div>
        <div><span>Rule version</span><strong>{item.scope.rule_version}</strong></div>
      </div>
      <section className="section-block">
        <div className="section-title"><div><h2>Declared repository cohort</h2><p>Every selected member remains visible, including those with no candidates.</p></div><span>{data.members.length} members</span></div>
        {data.members.length === 0 ? <EmptyState title="No members returned">This case has no declared repository members in the selected snapshot.</EmptyState>
          : <div className="table-scroll"><table><thead><tr><th scope="col">Repository</th><th scope="col">Evidence state</th><th scope="col">Findings</th><th scope="col">Candidates</th><th scope="col">Explore</th></tr></thead>
            <tbody>{data.members.map((member) => <tr key={member.repository_id}>
              <th scope="row"><Link to={routes.repository({ ...scope, repositoryId: member.repository_id })}>{member.repository_name}</Link><small>{member.identity_status} · {member.eligibility_status}</small></th>
              <td>{member.unknown_count > 0 ? <Status value="UNKNOWN" /> : <span className="muted">No UNKNOWN finding</span>}</td>
              <td>{member.unknown_count} unknown · {member.bounded_no_count} bounded NO{member.qualifying_count > 0 && ` · ${member.qualifying_count} qualifying`}</td>
              <td>{member.candidate_count === 0 ? 'No candidate emitted' : `${member.candidate_count} emitted`}</td>
              <td><Link className="text-link" to={routes.repository({ ...scope, repositoryId: member.repository_id })}>Inspect repository →</Link></td>
            </tr>)}</tbody></table></div>}
      </section>
      <p className="method-note">Lifecycle categories describe evidence questions; they do not prescribe event chronology. Counts describe the selected cohort and snapshot only.</p>
    </>}
  </Shell>;
}
