import { useEffect, useState } from 'react';
import { getEducations, getExperiences, getProjects, getSkills } from '../api/client';
import type { Education, Experience, Project, SkillCategory } from '../types';

export type ContentStatus = 'loading' | 'loaded' | 'error';
export type PortfolioCollection = 'projects' | 'experiences' | 'educations' | 'skills';

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

export function usePortfolioData(): PortfolioData {
  const [data, setData] = useState<Omit<PortfolioData, 'status'>>({
    projects: [],
    experiences: [],
    educations: [],
    skills: [],
  });
  const [status, setStatus] = useState<PortfolioStatus>({
    projects: 'loading',
    experiences: 'loading',
    educations: 'loading',
    skills: 'loading',
  });

  useEffect(() => {
    const controller = new AbortController();
    const load = async <K extends PortfolioCollection>(
      key: K,
      request: (signal: AbortSignal) => Promise<Omit<PortfolioData, 'status'>[K]>,
    ) => {
      try {
        const value = await request(controller.signal);
        setData((current) => ({ ...current, [key]: value }));
        setStatus((current) => ({ ...current, [key]: 'loaded' }));
      } catch (error) {
        if (error instanceof DOMException && error.name === 'AbortError') return;
        console.error(`Error fetching ${key}:`, error);
        setStatus((current) => ({ ...current, [key]: 'error' }));
      }
    };

    void load('projects', getProjects);
    void load('experiences', getExperiences);
    void load('educations', getEducations);
    void load('skills', getSkills);

    return () => controller.abort();
  }, []);

  return { ...data, status };
}
