import {
  educations,
  experiences,
  projects,
  skills,
} from '../data/portfolio';
import type { Education, Experience, Project, SkillCategory } from '../types';

export type ContentStatus = 'loading' | 'loaded' | 'error';

export interface PortfolioStatus {
  projects: ContentStatus;
  experiences: ContentStatus;
  educations: ContentStatus;
  skills: ContentStatus;
}

export interface PortfolioData {
  projects: Project[];
  experiences: Experience[];
  educations: Education[];
  skills: SkillCategory[];
  status: PortfolioStatus;
}

const status: PortfolioStatus = {
  projects: 'loaded',
  experiences: 'loaded',
  educations: 'loaded',
  skills: 'loaded',
};

export function usePortfolioData(): PortfolioData {
  return {
    projects,
    experiences,
    educations,
    skills,
    status,
  };
}
