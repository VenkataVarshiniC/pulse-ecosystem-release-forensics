import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { cleanup, render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter } from 'react-router-dom';
import { App } from '../src/App';
import type { ArtifactEvidence, Candidate, Finding, InvestigationSummary, Member, Provenance, RepositoryDetail, Scope } from '../src/api/types';

const cv = '11111111-1111-4111-8111-111111111111';
const snap = '22222222-2222-4222-8222-222222222222';
const repoA = '33333333-3333-4333-8333-333333333333';
const repoB = '44444444-4444-4444-8444-444444444444';
const artifact = '55555555-5555-4555-8555-555555555555';
const artifact2 = '66666666-6666-4666-8666-666666666666';
const candidateId = '77777777-7777-4777-8777-777777777777';
const peerId = '88888888-8888-4888-8888-888888888888';
const findingId = '99999999-9999-4999-8999-999999999999';
const scope: Scope = { case_id: cv, case_version_id: cv, case_version: 1, analysis_snapshot_id: snap, snapshot_state: 'PUBLISHED_VALIDATION', rule_version: 'r1', metric_definition_version: 'm1', model_version: 'v1' };
const investigation: InvestigationSummary = { scope, case_name: 'pytest release validation', package_name: 'pytest', package_ecosystem: 'pypi', release_version: '8.0.0', window_start: '2024-01-01T00:00:00Z', window_end: '2024-02-01T00:00:00Z', member_count: 2 };
const otherInvestigation: InvestigationSummary = { ...investigation, scope: { ...scope, case_version_id: repoB, analysis_snapshot_id: artifact2 }, case_name: 'urllib3 release validation', package_name: 'urllib3', release_version: '2.0.0', member_count: 6 };
const memberA: Member = { repository_id: repoA, repository_name: 'example/alpha', identity_status: 'RESOLVED', selection_method: 'DECLARED', eligibility_status: 'ELIGIBLE', candidate_count: 2, unknown_count: 4, bounded_no_count: 1, qualifying_count: 0 };
const memberB: Member = { ...memberA, repository_id: repoB, repository_name: 'example/beta', candidate_count: 0, unknown_count: 5, bounded_no_count: 0 };
const unknown: Finding = { finding_id: findingId, lifecycle_category: 'MIGRATION_FRICTION', question_id: 'friction', finding_status: 'UNKNOWN', reason_code: 'MISSING_SOURCE', confidence_level: null, sufficiency_status: 'INSUFFICIENT', sufficiency_reason_code: 'REQUIRED_SOURCE_MISSING', required_source_set_version: 's1', rule_version: 'r1', source_reasons: [{ source_type: 'issues', reason_code: 'SOURCE_UNAVAILABLE', required: true }], artifact_support_ids: [], observation_support_ids: [], review_support_ids: [] };
const bounded: Finding = { ...unknown, finding_status: 'NO_QUALIFYING_EVIDENCE_FOUND', reason_code: 'NO_QUALIFYING_EVIDENCE', sufficiency_status: 'SUFFICIENT', sufficiency_reason_code: 'REQUIREMENTS_MET', source_reasons: [] };
const observation = { observation_id: cv, artifact_id: artifact, observation_type: 'DEPENDENCY_DECLARATION', declared_constraint: '>=7', resolved_version: null, repository_ref: 'main', path_ref: 'pyproject.toml', observation_time: null, historical_position: 'AFTER', quality_status: 'RECORDED' };
const repository: RepositoryDetail = { scope, member: memberA, source_states: [{ collection_task_id: cv, source_type: 'issues', task_type: 'ISSUE_SEARCH', required: true, terminal_status: 'SOURCE_UNAVAILABLE', error_class: 'RATE_LIMIT' }], observations: [observation], historical_pairs: [{ historical_pair_id: cv, pair_status: 'AFTER_ONLY', path_ref: 'pyproject.toml', before_observation_id: null, after_observation_id: cv, reason: 'NO_BEFORE_ANCHOR', method_version: 'h1' }], findings: [unknown], candidate_count: 2 };
const capture: ArtifactEvidence = { artifact_id: artifact, artifact_type: 'dependency_file', source_type: 'repository_file', capture_method: 'collector', repository_ref: 'main', source_event_time: null, retrieved_at: '2024-02-02T00:00:00Z', content_sha256: 'abcdef0123456789', observations: [observation] };
const candidate: Candidate = { candidate_id: candidateId, artifact_id: artifact, candidate_fingerprint: 'aabbccdd', lifecycle_category: 'MIGRATION_FRICTION', candidate_rule_id: 'rule-1', candidate_rule_version: '1', source_origin: 'COPIED_UPSTREAM', candidate_status: 'EMITTED', candidate_reason: 'TOKEN_MATCH', span_ref: 'L10', review: { review_id: cv, decision: 'REJECT', reason_code: 'COPIED_UPSTREAM', review_note: null, reviewed_at: '2024-02-02T00:00:00Z', review_origin: 'INHERITED', inherited_from_review_id: repoA, reviewer_identity: null }, original_candidate_id: repoB, original_review_id: repoA, review_write_enabled: false };
const provenance: Provenance = { scope, repository_id: repoA, artifact_id: artifact, artifact_type: 'dependency_file', source_type: 'repository_file', source_provider: 'github', capture_method: 'collector', public_locator: null, repository_ref: 'main', source_event_time: null, retrieved_at: '2024-02-02T00:00:00Z', content_sha256: 'abcdef0123456789', collection_task_id: cv, collection_run_id: cv, collection_run_kind: 'collector', task_status: 'SUCCEEDED', run_status: 'COMPLETED', linked_candidate_ids: [candidateId], linked_finding_ids: [], external_public_locators: [] };
const casePath = `/investigations/${cv}?snapshot_id=${snap}`;
const repoPath = `/investigations/${cv}/repositories/${repoA}?snapshot_id=${snap}`;
const evidencePath = `/investigations/${cv}/repositories/${repoA}/evidence?snapshot_id=${snap}`;
const findingPath = `/investigations/${cv}/repositories/${repoA}/findings/${findingId}?snapshot_id=${snap}`;
const candidatePath = `/investigations/${cv}/repositories/${repoA}/candidates/${candidateId}?snapshot_id=${snap}`;
const artifactPath = `/investigations/${cv}/repositories/${repoA}/artifacts/${artifact}?snapshot_id=${snap}`;

function renderAt(path: string) { return render(<MemoryRouter initialEntries={[path]}><App /></MemoryRouter>); }
function mockApi(handler: (url: URL) => unknown | Response) {
  const fn = vi.fn(async (input: string | URL | Request) => {
    const url = new URL(String(input));
    const result = handler(url);
    return result instanceof Response ? result : new Response(JSON.stringify(result), { status: 200, headers: { 'Content-Type': 'application/json' } });
  });
  vi.stubGlobal('fetch', fn);
  return fn;
}

beforeEach(() => vi.restoreAllMocks());
afterEach(() => { cleanup(); vi.unstubAllGlobals(); });

describe('operational investigation workflow', () => {
  it('renders API investigations and opens the exact case and snapshot', async () => {
    const fetcher = mockApi((url) => url.pathname.endsWith('/investigations') ? { items: [investigation, otherInvestigation] } : { investigation, members: [memberA, memberB] });
    renderAt('/investigations');
    expect(await screen.findByText('2 investigations')).toBeInTheDocument();
    expect(screen.getByText('urllib3')).toBeInTheDocument();
    await userEvent.click(screen.getByRole('link', { name: 'Open pytest release validation' }));
    expect(await screen.findByText('Declared repository cohort')).toBeInTheDocument();
    expect(fetcher.mock.calls.some(([url]) => String(url).includes(`/${cv}?snapshot_id=${snap}`))).toBe(true);
  });
  it('keeps the zero-candidate member in the declared cohort', async () => {
    mockApi(() => ({ investigation, members: [memberA, memberB] }));
    renderAt(casePath);
    const row = await screen.findByRole('row', { name: /example\/beta/ });
    expect(within(row).getByText('No candidate emitted')).toBeInTheDocument();
    expect(within(row).getByRole('link', { name: 'example/beta' })).toHaveAttribute('href', `/investigations/${cv}/repositories/${repoB}?snapshot_id=${snap}`);
  });
  it('separates declaration, resolved observation and AFTER_ONLY history', async () => {
    mockApi((url) => url.pathname.endsWith('/candidates') ? { scope, repository_id: repoA, items: [candidate] } : repository);
    renderAt(repoPath);
    expect(await screen.findByText('Declared constraint')).toBeInTheDocument();
    expect(screen.getByText('Not observed')).toBeInTheDocument();
    expect(screen.getByText('AFTER_ONLY')).toBeInTheDocument();
    expect(screen.getByText(/does not prove earlier absence/)).toBeInTheDocument();
  });
  it('renders UNKNOWN and source unavailable as uncertainty, never zero', async () => {
    mockApi(() => unknown);
    renderAt(findingPath);
    expect(await screen.findByText('The question remains unanswered')).toBeInTheDocument();
    expect(screen.getByText(/does not have sufficient qualifying evidence/)).toBeInTheDocument();
    expect(screen.getByText('Source unavailable')).toBeInTheDocument();
    expect(screen.queryByText('No issue found')).not.toBeInTheDocument();
  });
  it('describes bounded NO as scoped absence of qualifying evidence', async () => {
    mockApi(() => bounded);
    renderAt(findingPath);
    expect(await screen.findByText('A bounded negative finding')).toBeInTheDocument();
    expect(screen.getByText(/does not establish that the event never happened/)).toBeInTheDocument();
  });
  it('preserves missing event time and uses the server cursor with the exact filters', async () => {
    const fetcher = mockApi((url) => ({ scope, repository_id: repoA, items: url.searchParams.has('cursor') ? [{ ...capture, artifact_id: artifact2 }] : [capture], next_cursor: url.searchParams.has('cursor') ? null : artifact }));
    renderAt(evidencePath);
    expect(await screen.findByText('Event time unavailable')).toBeInTheDocument();
    expect(screen.getByText('Retrieved')).toBeInTheDocument();
    await userEvent.type(screen.getByLabelText('Source type'), 'repository_file');
    await userEvent.click(screen.getByRole('button', { name: 'Apply filters' }));
    expect(await screen.findByText('Page 1 · server page size 25')).toBeInTheDocument();
    await userEvent.click(screen.getByRole('button', { name: 'Next page' }));
    expect(await screen.findByText('Page 2 · server page size 25')).toBeInTheDocument();
    expect(fetcher.mock.calls.some(([url]) => String(url).includes(`cursor=${artifact}`) && String(url).includes('source_type=repository_file') && String(url).includes(`snapshot_id=${snap}`))).toBe(true);
  });
  it('labels inherited REJECT, shared artifact and immutable review', async () => {
    mockApi((url) => url.pathname.endsWith('/candidates') ? { scope, repository_id: repoA, items: [candidate, { ...candidate, candidate_id: peerId }] } : candidate);
    renderAt(candidatePath);
    expect(await screen.findByText(/Inherited review: this decision reuses/)).toBeInTheDocument();
    expect(screen.getByText(/2 candidate firings reference one captured artifact/)).toBeInTheDocument();
    expect(screen.getByText(/No — this published record is immutable/)).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /accept|reject/i })).not.toBeInTheDocument();
  });
  it('does not turn a failed evidence request into an empty evidence state', async () => {
    mockApi(() => new Response(JSON.stringify({ code: 'DATABASE_UNAVAILABLE', message: 'Unavailable' }), { status: 503 }));
    renderAt(evidencePath);
    expect(await screen.findByRole('alert')).toHaveTextContent('The local evidence database is unavailable');
    expect(screen.queryByText('No captures on this page')).not.toBeInTheDocument();
  });
  it('reports an invalid snapshot as an error, not an empty cohort', async () => {
    mockApi(() => new Response(JSON.stringify({ code: 'INVALID_SNAPSHOT', message: 'Invalid' }), { status: 404 }));
    renderAt(casePath);
    expect(await screen.findByRole('alert')).toHaveTextContent('That snapshot is not available');
    expect(screen.queryByText('No members returned')).not.toBeInTheDocument();
  });
  it('withholds unsafe public locators and never exposes internal raw paths', async () => {
    mockApi(() => ({ ...provenance, public_locator: 'file:///private/raw/secret.json', external_public_locators: ['file:///private/raw/secret.json'] }));
    renderAt(artifactPath);
    expect(await screen.findByText('Direct source link unavailable')).toBeInTheDocument();
    expect(screen.queryByText('file:///private/raw/secret.json')).not.toBeInTheDocument();
    expect(screen.getByText('Event time unavailable')).toBeInTheDocument();
  });
  it('opens an allowed public locator in a safe new tab', async () => {
    mockApi(() => ({ ...provenance, public_locator: 'https://github.com/example/alpha/issues/1' }));
    renderAt(artifactPath);
    const link = await screen.findByRole('link', { name: 'Open public source ↗' });
    expect(link).toHaveAttribute('rel', 'noopener noreferrer');
    expect(link).toHaveAttribute('href', 'https://github.com/example/alpha/issues/1');
  });
});
