import { ContentMessage } from './ContentMessage';
import { HomeButton } from './Icons';
import type { ContentStatus } from '../hooks/usePortfolioData';
import type { Education } from '../types';

export function EducationSection({ educations, status, onBackHome }: { educations: Education[]; status: ContentStatus; onBackHome: () => void }) {
  return (
    <section className="content-section education-section snap-section" id="education">
      <div className="section-heading"><p className="eyebrow">THE FOUNDATION</p><h2>Education</h2></div>
      <ContentMessage status={status} label="education records" count={educations.length} />
      {educations.map((education) => <article className="education-row" key={education.id}><div><h3>{education.degree}</h3><p>{education.institution}, {education.country}</p></div><p>{education.start_date} — {education.end_date}</p></article>)}
      <HomeButton onClick={onBackHome} />
    </section>
  );
}
