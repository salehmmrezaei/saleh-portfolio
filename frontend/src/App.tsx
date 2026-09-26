import { useEffect, useState } from 'react';
import './index.css';
import { ExperienceCarousel } from './components/ExperienceCarousel';
import { ExternalLinkIcon, HomeButton } from './components/Icons';
import { Hero } from './components/Hero';
import { ContactSection } from './components/ContactSection';
import { SkillsGrid } from './components/SkillsGrid';
import type { Education, Experience, Project } from './types';
import aboutPhoto from './assets/about-photo.jpg';

type ContentStatus = 'loading' | 'loaded' | 'error';
const rotatingLines = ['Hi, the name\'s Saleh', 'I build intelligent products.', 'I make AI feel useful.'];

function App() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [experiences, setExperiences] = useState<Experience[]>([]);
  const [educations, setEducations] = useState<Education[]>([]);
  const [status, setStatus] = useState<Record<string, ContentStatus>>({ projects: 'loading', experiences: 'loading', educations: 'loading' });
  const [lineIndex, setLineIndex] = useState(0);
  const [visibleText, setVisibleText] = useState('');
  const [isDeleting, setIsDeleting] = useState(false);

  const scrollHome = () => {
    document.querySelector<HTMLElement>('.page-shell')?.scrollTo({
      top: 0,
      behavior: 'smooth',
    });
    window.history.replaceState(null, '', '#home');
  };

  useEffect(() => {
    const line = rotatingLines[lineIndex];
    const complete = visibleText === line;
    const timer = window.setTimeout(() => {
      const next = isDeleting ? line.slice(0, visibleText.length - 1) : line.slice(0, visibleText.length + 1);
      setVisibleText(next);
      if (!isDeleting && next === line) window.setTimeout(() => setIsDeleting(true), 1500);
      if (isDeleting && next === '') { setIsDeleting(false); setLineIndex((index) => (index + 1) % rotatingLines.length); }
    }, isDeleting ? 45 : complete ? 1500 : 85);
    return () => window.clearTimeout(timer);
  }, [isDeleting, lineIndex, visibleText]);

  useEffect(() => {
    const load = async <T,>(endpoint: string, setter: (value: T[]) => void) => {
      try {
        const response = await fetch(`/api/${endpoint}`);
        if (!response.ok) throw new Error(`Unable to load ${endpoint}`);
        setter(await response.json() as T[]);
        setStatus((current) => ({ ...current, [endpoint]: 'loaded' }));
      } catch (error) {
        console.error(`Error fetching ${endpoint}:`, error);
        setStatus((current) => ({ ...current, [endpoint]: 'error' }));
      }
    };
    void load<Project>('projects', setProjects);
    void load<Experience>('experiences', setExperiences);
    void load<Education>('educations', setEducations);
  }, []);

  const message = (key: string, label: string, count: number) => status[key] === 'loading' ? <p className="empty-state">Loading {label}...</p> : status[key] === 'error' ? <p className="empty-state">{label} are temporarily unavailable.</p> : count === 0 ? <p className="empty-state">No {label} found.</p> : null;

  return (
    <main className="page-shell">
      <Hero visibleText={visibleText} onBackHome={scrollHome} />
      <section className="content-section about-section snap-section" id="about">
        <div className="about-visual">
          <div className="section-heading"><p className="eyebrow">A LITTLE ABOUT ME</p><h2><span className="heading-line">Curious by nature.</span><br /><em>Builder by choice.</em></h2></div>
          <img className="about-photo" src={aboutPhoto} alt="Saleh exploring a forest trail" />
        </div>
        <div className="about-copy">
          <p>Hey 👋 I’m Saleh, an AI Engineer based in Italy with a background in both artificial intelligence and software engineering.
            I completed my M.Sc. in Artificial Intelligence at the University of Bologna, and my work has focused on building practical AI systems with LLMs, RAG, AI agents, NLP, and machine learning.</p>
          <p>I enjoy turning ideas and prototypes into reliable applications, whether that means designing RAG pipelines, building agentic workflows, developing Python/FastAPI backends, or experimenting with new models and evaluation methods.</p>
          <p>Outside of work, I’m always exploring new AI tools, improving my projects, and learning how to build better systems that are useful, scalable, and production-ready.</p>
        </div>
        <HomeButton onClick={scrollHome} />
      </section>
      <section className="content-section experience-section snap-section" id="experience">
        <div className="section-heading"><p className="eyebrow">PROFESSIONAL EXPERIENCES</p></div>
        {message('experiences', 'experiences', experiences.length)}
        {experiences.length > 0 && <ExperienceCarousel experiences={experiences} />}
        <HomeButton onClick={scrollHome} />
      </section>
      <section className="content-section projects-section snap-section" id="projects">
        <div className="section-heading"><p className="eyebrow">SELECTED WORK</p><h2>Projects</h2></div>
        {message('projects', 'projects', projects.length)}
        <div className="project-grid">{projects.map((project) => <article className="project-card" key={project.id}><div><p className="project-number">0{project.id}</p><h3>{project.name}</h3><p>{project.description.join(' ')}</p></div><div className="project-footer"><div className="tags">{project.skills.map((skill) => <span key={skill}>{skill}</span>)}</div><a href={project.url} target="_blank" rel="noreferrer" aria-label={`View ${project.name}`}><ExternalLinkIcon /></a></div></article>)}</div>
        <HomeButton onClick={scrollHome} />
      </section>
      <section className="content-section skills-section snap-section" id="skills">
        <div className="section-heading">
          <p className="eyebrow">WHAT I WORK WITH</p>
          <h2>Skills &amp; Technologies</h2>
          <p className="skills-intro">From LLM systems and retrieval pipelines to production-ready backend infrastructure.</p>
        </div>
        <SkillsGrid />
        <HomeButton onClick={scrollHome} />
      </section>
      <section className="content-section education-section snap-section" id="education">
        <div className="section-heading"><p className="eyebrow">THE FOUNDATION</p><h2>Education</h2></div>
        {message('educations', 'education records', educations.length)}
        {educations.map((education) => <article className="education-row" key={education.id}><div><h3>{education.degree}</h3><p>{education.institution}, {education.country}</p></div><p>{education.start_date} — {education.end_date}</p></article>)}
        <HomeButton onClick={scrollHome} />
      </section>
      <ContactSection onBackHome={scrollHome} />
    </main>
  );
}

export default App;
