import type { SkillCategory } from '../types';

interface SkillsGridProps {
  skills: SkillCategory[];
}

export function SkillsGrid({ skills }: SkillsGridProps) {
  return (
    <div className="skills-grid">
      {skills.map((category, index) => (
        <article className={`skill-category${category.featured ? ' skill-category-featured' : ''}`} key={category.id}>
          <p className="skill-category-number">{String(index + 1).padStart(2, '0')} —</p>
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
