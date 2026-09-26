export interface Project {
  id: number;
  name: string;
  skills: string[];
  url: string;
  description: string[];
}

export interface Experience {
  id: number;
  company: string;
  company_slug: string;
  role: string;
  start_date: string;
  end_date: string;
  skills: string[];
  url: string;
  description: string[];
}

export interface Education {
  id: number;
  institution: string;
  degree: string;
  start_date: string;
  end_date: string;
  country: string;
}

export interface SkillCategory {
  id: number;
  title: string;
  skills: string[];
  description: string;
  featured: boolean;
}
