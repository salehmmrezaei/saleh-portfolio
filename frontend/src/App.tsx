import { AboutSection } from './components/AboutSection';
import { ContactSection } from './components/ContactSection';
import { ExperienceSection } from './components/ExperienceSection';
import { Hero } from './components/Hero';
import { ProjectsSection } from './components/ProjectsSection';
import { ProjectDetail } from './components/ProjectDetail';
import { projectDetails, slugify } from './data/projects';
import { SkillsSection } from './components/SkillsSection';
import { GitHubIcon, HomeIcon, LinkedInIcon, MailIcon } from './components/Icons';
import { usePortfolioData } from './hooks/usePortfolioData';
import { useEffect, useState } from 'react';

function App() {
  const { projects, experiences, skills, status } = usePortfolioData();
  const [projectSlug, setProjectSlug] = useState(() => window.location.pathname.match(/^\/projects\/([^/]+)$/)?.[1]);
  const staticProjects = Object.values(projectDetails).map((details, index) => ({
    id: index + 1,
    name: details.slug.split('-').map((word) => word[0].toUpperCase() + word.slice(1)).join(' '),
    skills: details.coreStack ?? [],
    url: `https://github.com/salehmmrezaei/${details.slug}`,
    description: [details.overview, ...details.outcomes],
  }));
  const projectCatalog = staticProjects.map((staticProject) => {
    const project = projects.find((candidate) => candidate.url === staticProject.url);
    return project ? { ...project, name: staticProject.name } : staticProject;
  });
  const selectedProject = projectSlug
    ? projectCatalog.find((project) => slugify(project.name) === projectSlug)
    : undefined;

  useEffect(() => {
    const onPopState = () => setProjectSlug(window.location.pathname.match(/^\/projects\/([^/]+)$/)?.[1]);
    window.addEventListener('popstate', onPopState);
    return () => window.removeEventListener('popstate', onPopState);
  }, []);

  useEffect(() => {
    if (projectSlug || window.location.hash !== '#projects') return;
    requestAnimationFrame(() => {
      const pageShell = document.querySelector<HTMLElement>('.page-shell');
      const projectsSection = document.querySelector<HTMLElement>('#projects');
      if (pageShell && projectsSection) {
        pageShell.scrollTo({ top: projectsSection.offsetTop, behavior: 'smooth' });
      }
    });
  }, [projectSlug]);

  if (selectedProject) {
    const selectedIndex = projectCatalog.findIndex((project) => project.id === selectedProject.id);
    const navigate = (slug: string) => { window.history.pushState({}, '', `/projects/${slug}`); setProjectSlug(slug); window.scrollTo(0, 0); };
    const backToProjects = () => {
      window.history.pushState({}, '', '/#projects');
      setProjectSlug(undefined);
    };
    return <ProjectDetail project={selectedProject} projectIndex={selectedIndex} projects={projectCatalog} onNavigate={navigate} onBack={backToProjects} />;
  }

  const scrollHome = () => {
    document.querySelector<HTMLElement>('.page-shell')?.scrollTo({
      top: 0,
      behavior: 'smooth',
    });
    window.history.replaceState(null, '', '#home');
  };

  return (
    <main className="page-shell">
      <div className="site-utility" aria-label="Social links and home">
        <div className="site-social-links">
          <a href="https://www.linkedin.com/in/salehmmrezaei/" target="_blank" rel="noreferrer" aria-label="LinkedIn"><LinkedInIcon /></a>
          <a href="https://github.com/salehmmrezaei" target="_blank" rel="noreferrer" aria-label="GitHub"><GitHubIcon /></a>
          <a href="mailto:salehmmrezaei@gmail.com" aria-label="Email"><MailIcon /></a>
        </div>
        <a className="site-home-link" href="#home" aria-label="Back to home" onClick={(event) => { event.preventDefault(); scrollHome(); }}><HomeIcon /></a>
      </div>
      <Hero onBackHome={scrollHome} />
      <AboutSection onBackHome={scrollHome} />
      <ExperienceSection experiences={experiences} status={status.experiences} onBackHome={scrollHome} />
      <ProjectsSection projects={projectCatalog} status={status.projects} onBackHome={scrollHome} />
      <SkillsSection skills={skills} status={status.skills} onBackHome={scrollHome} />
      <ContactSection onBackHome={scrollHome} />
    </main>
  );
}

export default App;
