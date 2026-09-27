import { ContentMessage } from './ContentMessage';
import { HomeButton } from './Icons';
import type { ContentStatus } from '../hooks/usePortfolioData';
import type { Project } from '../types';

export function ProjectsSection({ projects, status, onBackHome }: { projects: Project[]; status: ContentStatus; onBackHome: () => void }) {
  return (
    <section className="content-section projects-section snap-section" id="projects">
      <div className="section-heading"><p className="eyebrow">SELECTED WORK</p><h2>Projects</h2></div>
      <ContentMessage status={status} label="projects" count={projects.length} />
      <div className="project-rail" tabIndex={0} aria-label="Projects">
        {projects.map((project, index) => <a className="project-card" key={project.id} href={`/projects/${slugify(project.name)}`} aria-label={`View ${project.name} project`}><div><p className="project-number">{String(index + 1).padStart(2, '0')}</p><h3>{project.name}</h3><p>{project.description[0]}</p></div><div className="project-footer"><div className="tags">{project.skills.map((skill) => <span key={skill}>{skill}</span>)}</div><span className="project-cta">View project <span aria-hidden="true">↗</span></span></div></a>)}
      </div>
      <HomeButton onClick={onBackHome} />
    </section>
  );
}

function slugify(value: string) {
  return value.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
}
