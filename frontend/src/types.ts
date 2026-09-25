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
  grade: string;
  start_date: string;
  end_date: string;
  country: string;
}
