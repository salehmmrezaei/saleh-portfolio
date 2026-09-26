import { AboutSection } from './components/AboutSection';
import { ContactSection } from './components/ContactSection';
import { EducationSection } from './components/EducationSection';
import { ExperienceSection } from './components/ExperienceSection';
import { Hero } from './components/Hero';
import { ProjectsSection } from './components/ProjectsSection';
import { ProjectDetail } from './components/ProjectDetail';
import { slugify } from './data/projects';
import { SkillsSection } from './components/SkillsSection';
import { usePortfolioData } from './hooks/usePortfolioData';
import { useEffect, useState } from 'react';

function App() {
  const { projects, experiences, educations, skills, status } = usePortfolioData();
  const [projectSlug, setProjectSlug] = useState(() => window.location.pathname.match(/^\/projects\/([^/]+)$/)?.[1]);
  const selectedProject = projectSlug ? projects.find((project) => slugify(project.name) === projectSlug) : undefined;

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
    const selectedIndex = projects.findIndex((project) => project.id === selectedProject.id);
    const navigate = (slug: string) => { window.history.pushState({}, '', `/projects/${slug}`); setProjectSlug(slug); window.scrollTo(0, 0); };
    const backToProjects = () => {
      window.history.pushState({}, '', '/#projects');
      setProjectSlug(undefined);
    };
    return <ProjectDetail project={selectedProject} projectIndex={selectedIndex} projects={projects} onNavigate={navigate} onBack={backToProjects} />;
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
      <Hero onBackHome={scrollHome} />
      <AboutSection onBackHome={scrollHome} />
      <ExperienceSection experiences={experiences} status={status.experiences} onBackHome={scrollHome} />
      <ProjectsSection projects={projects} status={status.projects} onBackHome={scrollHome} />
      <SkillsSection skills={skills} status={status.skills} onBackHome={scrollHome} />
      <EducationSection educations={educations} status={status.educations} onBackHome={scrollHome} />
      <ContactSection onBackHome={scrollHome} />
    </main>
  );
}

export default App;
