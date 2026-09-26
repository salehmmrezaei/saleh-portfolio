import { AboutSection } from './components/AboutSection';
import { ContactSection } from './components/ContactSection';
import { EducationSection } from './components/EducationSection';
import { ExperienceSection } from './components/ExperienceSection';
import { Hero } from './components/Hero';
import { ProjectsSection } from './components/ProjectsSection';
import { SkillsSection } from './components/SkillsSection';
import { usePortfolioData } from './hooks/usePortfolioData';

function App() {
  const { projects, experiences, educations, skills, status } = usePortfolioData();

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
