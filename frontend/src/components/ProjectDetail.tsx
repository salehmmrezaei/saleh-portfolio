import { projectDetails, slugify, type ChallengeCaseStudy, type PipelineStage, type ProjectDetails } from '../data/projects';
import type { Project } from '../types';

interface ProjectDetailProps {
  project: Project;
  projectIndex: number;
  projects: Project[];
  onNavigate: (slug: string) => void;
  onBack: () => void;
}

export function ProjectDetail({ project, projectIndex, projects, onNavigate, onBack }: ProjectDetailProps) {
  const details = projectDetails[slugify(project.name)] ?? createFallback(project);
  const role = details.role ?? 'Project builder';
  const projectType = details.type ?? 'Personal Project';
  const coreStack = details.coreStack ?? project.skills;
  const previous = projects[(projectIndex - 1 + projects.length) % projects.length];
  const next = projects[(projectIndex + 1) % projects.length];

  return (
    <main className="project-detail">
      <div className="project-detail-nav">
        <button type="button" className="project-back" onClick={onBack}>← Back to projects</button>
        <div className="project-detail-nav-links">
          <a href={project.url} target="_blank" rel="noreferrer">GitHub ↗</a>
        </div>
      </div>
      <header className="project-detail-header">
        <div className="project-hero-topline">
          <p className="project-number">0{project.id}</p>
          <p className="eyebrow">{details.category} · {details.year}</p>
        </div>
        <h1>{project.name}</h1>
        <p className="project-lede">{details.overview}</p>
        <div className="project-meta" aria-label="Project metadata">
          <div><span>Role</span><strong>{role}</strong></div>
          <div><span>Core stack</span><strong>{coreStack.join(' · ')}</strong></div>
          <div><span>Type</span><strong>{projectType}</strong></div>
          <div><span>Year</span><strong>{details.year}</strong></div>
        </div>
        <a className="project-github" href={project.url} target="_blank" rel="noreferrer">
          <span className="project-github-label">View source on GitHub</span>
          <span className="project-github-arrow" aria-hidden="true">↗</span>
        </a>
      </header>

      <div className="project-detail-layout">
        <div className="project-detail-body">
          <DetailSection title="The problem">{details.problem}</DetailSection>
          <section className="project-detail-section" aria-labelledby="pipeline-heading">
            <h2 id="pipeline-heading">Architecture / pipeline</h2>
            <ol className="project-pipeline">
              {isPipelineStage(details.pipeline)
                ? details.pipeline.map((step, index) => <li key={step.title}><span>{String(index + 1).padStart(2, '0')}</span><strong>{step.title}</strong><p>{step.description}</p></li>)
                : details.pipeline.map((step, index) => <li key={step}><span>{String(index + 1).padStart(2, '0')}</span><strong>{step}</strong></li>)}
            </ol>
          </section>
          <section className="project-detail-section" aria-labelledby="stack-heading">
            <h2 id="stack-heading">Tech stack</h2>
            <div className="stack-groups">
              {Object.entries(details.stack).map(([group, stackGroup]) => (
                <div className="stack-group" key={group}>
                  <h3>{group}</h3>
                  <p>{stackGroup.role}</p>
                  <div className="tags">{stackGroup.technologies.map((technology) => <span key={technology}>{technology}</span>)}</div>
                </div>
              ))}
            </div>
          </section>
          <section className="project-detail-section" aria-labelledby="challenge-heading">
            <h2 id="challenge-heading">Key challenges</h2>
            {isChallengeCaseStudy(details.challenges) ? (
              <div className="challenge-grid">
                {details.challenges.map((challenge, index) => (
                  <article className="challenge-card" key={challenge.title}>
                    <span className="challenge-number">{String(index + 1).padStart(2, '0')}</span>
                    <h3>{challenge.title}</h3>
                    <div><strong>Problem</strong><p>{challenge.problem}</p></div>
                    <div><strong>Approach</strong><p>{challenge.approach}</p></div>
                  </article>
                ))}
              </div>
            ) : (
              <ul>{details.challenges.map((challenge) => <li key={challenge}>{challenge}</li>)}</ul>
            )}
          </section>
          <section className="project-detail-section" aria-labelledby="outcome-heading">
            <h2 id="outcome-heading">Outcomes</h2>
            <ul>{details.outcomes.map((outcome) => <li key={outcome}>{outcome}</li>)}</ul>
          </section>
        </div>
      </div>

      <nav className="project-pagination" aria-label="Project navigation">
        <button className="project-pagination-link project-pagination-previous" type="button" onClick={() => onNavigate(slugify(previous.name))}>
          <span className="project-pagination-arrow" aria-hidden="true">←</span>
          <span><small>Previous project</small>{previous.name}</span>
        </button>
        <button className="project-pagination-link project-pagination-next" type="button" onClick={() => onNavigate(slugify(next.name))}>
          <span><small>Next project</small>{next.name}</span>
          <span className="project-pagination-arrow" aria-hidden="true">→</span>
        </button>
      </nav>
    </main>
  );
}

function isChallengeCaseStudy(challenges: ProjectDetails['challenges']): challenges is ChallengeCaseStudy[] {
  return challenges.length > 0 && typeof challenges[0] !== 'string';
}

function isPipelineStage(pipeline: ProjectDetails['pipeline']): pipeline is PipelineStage[] {
  return pipeline.length > 0 && typeof pipeline[0] !== 'string';
}

function DetailSection({ title, children }: { title: string; children: string }) {
  return <section className="project-detail-section project-text-section"><h2>{title}</h2><p>{children}</p></section>;
}

function createFallback(project: Project): ProjectDetails {
  return {
    slug: slugify(project.name),
    category: 'Engineering project',
    year: '2026',
    overview: project.description[0],
    problem: 'A practical engineering problem addressed through a focused implementation.',
    pipeline: project.description.slice(1),
    stack: { Technologies: { technologies: project.skills, role: 'Core project technologies' } },
    challenges: [],
    outcomes: project.description.slice(1),
  };
}
