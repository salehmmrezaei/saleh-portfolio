import { useRef } from 'react';
import { ArrowIcon, ExternalLinkIcon } from './Icons';
import type { Experience } from '../types';
import cnrLogo from '../assets/cnr-logo.jpeg';
import denxaLogo from '../assets/denxa-logo.jpeg';
import sulfateSharghLogo from '../assets/sulfate-shargh-logo.jpeg';
import zutreLogo from '../assets/zutre-logo.jpeg';

const companyLogos: Record<string, string> = {
  cnr: cnrLogo,
  zutre: zutreLogo,
  denxa: denxaLogo,
  'sulfate-shargh': sulfateSharghLogo,
};

export function ExperienceCarousel({ experiences }: { experiences: Experience[] }) {
  const rail = useRef<HTMLDivElement>(null);
  const move = (direction: number) => rail.current?.scrollBy({ left: direction * (rail.current.clientWidth * .78), behavior: 'auto' });

  return (
    <div className="experience-carousel">
      <div className="carousel-controls">
        <button type="button" onClick={() => move(-1)} aria-label="Previous experience"><ArrowIcon direction="left" /></button>
        <button type="button" onClick={() => move(1)} aria-label="Next experience"><ArrowIcon /></button>
      </div>
      <div className="experience-rail" ref={rail} tabIndex={0} aria-label="Work experience cards">
        {experiences.map((exp) => (
          <article className="experience-card" key={exp.id}>
            <div className="experience-card-header">
              <a href={exp.url} target="_blank" rel="noreferrer" aria-label={`Visit ${exp.company} website`}>
                {companyLogos[exp.company_slug] ? (
                  <img className="company-logo" src={companyLogos[exp.company_slug]} alt={`${exp.company} logo`} />
                ) : (
                  <div className="company-mark" aria-hidden="true">{exp.company.slice(0, 2).toUpperCase()}</div>
                )}
              </a>
              <a href={exp.url} target="_blank" rel="noreferrer" aria-label={`Open ${exp.company}`}><ExternalLinkIcon /></a>
            </div>
            <h3>{exp.role}</h3>
            <p className="card-company">
              <a href={exp.url} target="_blank" rel="noreferrer">{exp.company}</a>
            </p>
            <div className="tags experience-tags">{exp.skills.map((skill) => <span key={skill}>{skill}</span>)}</div>
            <p className="card-date">{formatDate(exp.start_date)} — {formatDate(exp.end_date)}</p>
            <ul className="experience-description">{exp.description.map((line) => <li key={line}>{line}</li>)}</ul>
          </article>
        ))}
      </div>
    </div>
  );
}

function formatDate(value: string) {
  const date = new Date(`${value}T00:00:00`);
  if (Number.isNaN(date.getTime())) return value;
  return date.toLocaleDateString('en-US', { month: 'short', year: 'numeric' }).toUpperCase();
}
