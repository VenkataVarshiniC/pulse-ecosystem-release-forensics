import type { ReactNode } from 'react';
import { Link } from 'react-router-dom';

export interface Crumb {
  label: string;
  to?: string;
}

export function Shell({ children, crumbs = [] }: { children: ReactNode; crumbs?: Crumb[] }) {
  return (
    <div className="app-shell">
      <a className="skip-link" href="#main">Skip to content</a>
      <header className="topbar">
        <div className="topbar-inner">
          <Link className="brand" to="/investigations" aria-label="PULSE investigations home">
            <span className="brand-mark" aria-hidden="true"><span /><span /><span /></span>
            <span>PULSE</span>
          </Link>
          <span className="topbar-divider" />
          <span className="topbar-context">Release forensics</span>
          <nav className="topnav" aria-label="Primary navigation">
            <Link to="/investigations">Investigations</Link>
          </nav>
        </div>
      </header>
      <div className="app-content">
        <div className="context-strip">
          <span className="context-dot" />
          Published validation evidence <span className="context-separator">/</span>
          Workflow provisional — stakeholder validation pending
        </div>
        {crumbs.length > 0 && (
          <nav className="breadcrumbs" aria-label="Breadcrumb">
            <ol>
              <li><Link to="/investigations">Investigations</Link></li>
              {crumbs.map((crumb, index) => (
                <li key={`${crumb.label}-${index}`}>
                  <span aria-hidden="true">/</span>
                  {crumb.to ? <Link to={crumb.to}>{crumb.label}</Link> : <span aria-current="page">{crumb.label}</span>}
                </li>
              ))}
            </ol>
          </nav>
        )}
        <main id="main">{children}</main>
        <footer className="footer">PULSE · Bounded evidence, explicit uncertainty</footer>
      </div>
    </div>
  );
}

export function PageHeading({ eyebrow, title, description, aside }: {
  eyebrow: string; title: string; description?: string; aside?: ReactNode;
}) {
  return (
    <div className="page-heading">
      <div>
        <p className="eyebrow">{eyebrow}</p>
        <h1>{title}</h1>
        {description && <p className="page-description">{description}</p>}
      </div>
      {aside && <div className="heading-aside">{aside}</div>}
    </div>
  );
}
