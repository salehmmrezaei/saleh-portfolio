import { ExperienceCarousel } from './ExperienceCarousel';
import { HomeButton } from './Icons';
import { ContentMessage } from './ContentMessage';
import type { ContentStatus } from '../hooks/usePortfolioData';
import type { Experience } from '../types';

export function ExperienceSection({ experiences, status, onBackHome }: { experiences: Experience[]; status: ContentStatus; onBackHome: () => void }) {
  return (
    <section className="content-section experience-section snap-section" id="experience">
      <div className="section-heading"><p className="eyebrow">PROFESSIONAL EXPERIENCES</p></div>
      <ContentMessage status={status} label="experiences" count={experiences.length} />
      {experiences.length > 0 && <ExperienceCarousel experiences={experiences} />}
      <HomeButton onClick={onBackHome} />
    </section>
  );
}
