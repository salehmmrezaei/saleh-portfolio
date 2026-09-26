import { ContentMessage } from './ContentMessage';
import { ExternalLinkIcon, HomeButton } from './Icons';
import type { ContentStatus } from '../hooks/usePortfolioData';
import type { Project } from '../types';

export function ProjectsSection({ projects, status, onBackHome }: { projects: Project[]; status: ContentStatus; onBackHome: () => void }) {
  return (
    <section className="content-section projects-section snap-section" id="projects">
      <div className="section-heading"><p className="eyebrow">SELECTED WORK</p><h2>Projects</h2></div>
      <ContentMessage status={status} label="projects" count={projects.length} />
      <div className="project-grid">{projects.map((project) => <article className="project-card" key={project.id}><div><p className="project-number">0{project.id}</p><h3>{project.name}</h3><p>{project.description.join(' ')}</p></div><div className="project-footer"><div className="tags">{project.skills.map((skill) => <span key={skill}>{skill}</span>)}</div><a href={project.url} target="_blank" rel="noreferrer" aria-label={`View ${project.name}`}><ExternalLinkIcon /></a></div></article>)}</div>
      <HomeButton onClick={onBackHome} />
    </section>
  );
}
