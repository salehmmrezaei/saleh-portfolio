interface SkillCategory {
  number: string;
  title: string;
  skills: string[];
  description: string;
  featured?: boolean;
}

const skillCategories: SkillCategory[] = [
  {
    number: '01',
    title: 'LLM & Generative AI',
    skills: ['RAG', 'LangChain', 'AI Agents', 'Prompt Engineering', 'LLM Evaluation', 'Vector Databases'],
    description: 'Building retrieval, agentic, and evaluation pipelines for production AI.',
    featured: true,
  },
  {
    number: '02',
    title: 'Backend & Production',
    skills: ['Python', 'FastAPI', 'REST APIs', 'Docker', 'Redis', 'Celery', 'PostgreSQL', 'AWS'],
    description: 'APIs, asynchronous workloads, containerized services, and scalable infrastructure.',
  },
  {
    number: '03',
    title: 'Machine Learning & Data',
    skills: ['PyTorch', 'Scikit-learn', 'Pandas', 'NumPy', 'SQL', 'ETL'],
    description: 'Experimentation, evaluation, data processing, and model-driven applications.',
  },
  {
    number: '04',
    title: 'Full-Stack & Workflow',
    skills: ['React', 'TypeScript', 'Git', 'CI'],
    description: 'Enough frontend and engineering tooling to ship complete AI products.',
  },
];

export function SkillsGrid() {
  return (
    <div className="skills-grid">
      {skillCategories.map((category) => (
        <article className={`skill-category${category.featured ? ' skill-category-featured' : ''}`} key={category.number}>
          <p className="skill-category-number">{category.number} —</p>
          <h3>{category.title}</h3>
          <div className="skill-category-tags">
            {category.skills.map((skill) => <span key={skill}>{skill}</span>)}
          </div>
          <p className="skill-category-description">{category.description}</p>
        </article>
      ))}
    </div>
  );
}
