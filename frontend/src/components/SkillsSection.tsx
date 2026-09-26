import { ContentMessage } from './ContentMessage';
import { HomeButton } from './Icons';
import { SkillsGrid } from './SkillsGrid';
import type { ContentStatus } from '../hooks/usePortfolioData';
import type { SkillCategory } from '../types';

export function SkillsSection({ skills, status, onBackHome }: { skills: SkillCategory[]; status: ContentStatus; onBackHome: () => void }) {
  return (
    <section className="content-section skills-section snap-section" id="skills">
      <div className="section-heading">
        <p className="eyebrow">WHAT I WORK WITH</p>
        <h2>Skills &amp; Technologies</h2>
        <p className="skills-intro">From LLM systems and retrieval pipelines to production-ready backend infrastructure.</p>
      </div>
      <ContentMessage status={status} label="skills" count={skills.length} />
      {skills.length > 0 && <SkillsGrid skills={skills} />}
      <HomeButton onClick={onBackHome} />
    </section>
  );
}
