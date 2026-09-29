import { Navigate, Route, Routes } from 'react-router-dom';
import { InvestigationListPage } from './pages/InvestigationListPage';
import { InvestigationOverviewPage } from './pages/InvestigationOverviewPage';
import { RepositoryPage } from './pages/RepositoryPage';
import { EvidencePage } from './pages/EvidencePage';
import { FindingPage } from './pages/FindingPage';
import { CandidatePage } from './pages/CandidatePage';
import { ArtifactPage } from './pages/ArtifactPage';
import { Shell } from './components/Shell';

export function App() {
  return <Routes>
    <Route path="/" element={<Navigate to="/investigations" replace />} />
    <Route path="/investigations" element={<InvestigationListPage />} />
    <Route path="/investigations/:caseVersionId" element={<InvestigationOverviewPage />} />
    <Route path="/investigations/:caseVersionId/repositories/:repositoryId" element={<RepositoryPage />} />
    <Route path="/investigations/:caseVersionId/repositories/:repositoryId/evidence" element={<EvidencePage />} />
    <Route path="/investigations/:caseVersionId/repositories/:repositoryId/findings/:findingId" element={<FindingPage />} />
    <Route path="/investigations/:caseVersionId/repositories/:repositoryId/candidates/:candidateId" element={<CandidatePage />} />
    <Route path="/investigations/:caseVersionId/repositories/:repositoryId/artifacts/:artifactId" element={<ArtifactPage />} />
    <Route path="*" element={<Shell><h1>Page not found</h1><p>Open an investigation to restore its case and snapshot context.</p></Shell>} />
  </Routes>;
}
