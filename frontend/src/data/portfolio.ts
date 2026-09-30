import type { Education, Experience, Project, SkillCategory } from '../types';
import { projectDetails } from './projects';

const PROJECT_NAMES: Record<string, string> = {
  'repopilot-ai': 'RepoPilot AI',
  'voice-notes-ai': 'Voice Notes AI',
  'disagreement-aware-sexism-detection': 'Disagreement-Aware Sexism Detection',
  'reinforcement-learning-lab': 'Reinforcement Learning Lab',
  'time-series-forecasting': 'Time-Series Forecasting',
  'news-popularity-prediction': 'News Popularity Prediction',
};

export const projects: Project[] = Object.values(projectDetails).map(
  (details, index) => ({
    id: index + 1,
    name:
      PROJECT_NAMES[details.slug] ??
      details.slug
        .split('-')
        .map((word) => word[0].toUpperCase() + word.slice(1))
        .join(' '),
    skills: details.coreStack ?? [],
    url: `https://github.com/salehmmrezaei/${details.slug}`,
    description: [details.overview, ...details.outcomes],
  }),
);

export const experiences: Experience[] = [
  {
    id: 1,
    company: 'Zutre',
    company_slug: 'zutre',
    role: 'R&D AI Engineer',
    start_date: '2025-12-01',
    end_date: '2026-06-30',
    skills: ['Python', 'RAG', 'Vector Databases'],
    url: 'https://zutre.com',
    description: [
      'Built end-to-end RAG pipelines covering ingestion, chunking, embeddings, vector indexing, semantic retrieval, context assembly, and LLM generation.',
      'Evaluated LLMs, embedding models, vector databases, and retrieval strategies to improve quality and support production-oriented component selection.',
    ],
  },
  {
    id: 2,
    company: 'CNR (ISMN)',
    company_slug: 'cnr',
    role: 'AI Engineer',
    start_date: '2025-11-01',
    end_date: '2026-08-31',
    skills: ['Python', 'LangChain', 'AI Agents'],
    url: 'https://www.cnr.it/',
    description: [
      'Designed and deployed LLM-powered pipelines for extracting structured information from scientific and technical documents.',
      'Built agentic workflows combining document processing, prompt orchestration, structured outputs, validation, and automated downstream processing.',
    ],
  },
  {
    id: 3,
    company: 'Denxa',
    company_slug: 'denxa',
    role: 'Software Engineer',
    start_date: '2022-12-01',
    end_date: '2023-05-31',
    skills: ['Python', 'REST APIs', 'Docker'],
    url: 'https://www.denxa.ca',
    description: [
      'Developed Python backend services and REST APIs for data-intensive applications, integrating data-processing and machine-learning components.',
      'Built containerized services with Docker and implemented testing, validation, logging, and error handling for reliable application behavior.',
    ],
  },
  {
    id: 4,
    company: 'Sulfate Shargh Co.',
    company_slug: 'sulfate-shargh',
    role: 'Software Engineer Intern',
    start_date: '2022-01-01',
    end_date: '2022-12-31',
    skills: ['Python', 'Machine Learning', 'Data Processing'],
    url: 'https://zincsulfate.co',
    description: [
      'Supported machine-learning experiments for workflow optimization through data preprocessing, model evaluation, and performance comparison.',
      'Documented experiment results and assisted with improving data and model workflows.',
    ],
  },
];

export const educations: Education[] = [
  {
    id: 1,
    institution: 'University of Bologna',
    degree: 'M.Sc. Artificial Intelligence',
    start_date: '2024-09-01',
    end_date: '2026-07-17',
    country: 'Italy',
  },
  {
    id: 2,
    institution: 'University of Zanjan',
    degree: 'B.Sc. Computer Engineering',
    start_date: '2017-09-01',
    end_date: '2022-05-22',
    country: 'Iran',
  },
];

export const skills: SkillCategory[] = [
  {
    id: 1,
    title: 'LLM & Generative AI',
    skills: [
      'RAG',
      'LangChain',
      'AI Agents',
      'Prompt Engineering',
      'LLM Evaluation',
      'Vector Databases',
    ],
    description:
      'Building retrieval, agentic, and evaluation pipelines for production AI.',
    featured: true,
  },
  {
    id: 2,
    title: 'Backend & Production',
    skills: [
      'Python',
      'FastAPI',
      'REST APIs',
      'Docker',
      'Redis',
      'Celery',
      'PostgreSQL',
      'AWS',
    ],
    description:
      'APIs, asynchronous workloads, containerized services, and scalable infrastructure.',
    featured: false,
  },
  {
    id: 3,
    title: 'Machine Learning & Data',
    skills: ['PyTorch', 'Scikit-learn', 'Pandas', 'NumPy', 'SQL', 'ETL'],
    description:
      'Experimentation, evaluation, data processing, and model-driven applications.',
    featured: false,
  },
  {
    id: 4,
    title: 'Full-Stack & Workflow',
    skills: ['React', 'TypeScript', 'Git', 'CI'],
    description:
      'Enough frontend and engineering tooling to ship complete AI products.',
    featured: false,
  },
];
