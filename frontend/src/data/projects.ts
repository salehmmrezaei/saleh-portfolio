export interface ProjectDetails {
  slug: string;
  category: string;
  year: string;
  overview: string;
  problem: string;
  pipeline: string[] | PipelineStage[];
  role?: string;
  coreStack?: string[];
  type?: string;
  stack: Record<string, StackGroup>;
  challenges: string[] | ChallengeCaseStudy[];
  outcomes: string[];
}

export interface PipelineStage {
  title: string;
  description: string;
}

export interface ChallengeCaseStudy {
  title: string;
  problem: string;
  approach: string;
}

export interface StackGroup {
  technologies: string[];
  role: string;
}

export function slugify(value: string) {
  return value.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
}

export const projectDetails: Record<string, ProjectDetails> = {
  'repopilot-ai': {
    slug: 'repopilot-ai',
    category: 'AI Developer tooling',
    year: '2026',
    role: 'AI / Full-Stack Engineer',
    coreStack: ['Python', 'FastAPI', 'PostgreSQL/pgvector', 'Redis', 'Celery', 'React', 'TypeScript'],
    type: 'Personal Engineering Project',
    overview: 'A repository intelligence platform that turns immutable source snapshots into searchable code indexes, grounded answers, and durable AI conversations.',
    problem: 'Understanding an unfamiliar repository requires more than semantic search. Relevant context is spread across files, symbols, source locations, and related code, while an AI answer is only useful if the developer can verify where its claims came from.\nRepoPilot was built to make repository understanding inspectable: import a fixed source snapshot, build a structured code index, retrieve evidence through multiple search channels, and generate answers whose references resolve back to the indexed source.',
    pipeline: [
      {
        title: 'Bounded repository import',
        description: 'Resolve a public GitHub repository to its default-branch commit and ingest a bounded, immutable source snapshot without executing repository code.',
      },
      {
        title: 'Versioned static indexing',
        description: 'Parse Python source into symbols and exact source chunks, preserve file and line provenance, and publish each index as an atomic version tied to its source snapshot.',
      },
      {
        title: 'Inspectable hybrid retrieval',
        description: 'Combine lexical search, symbol matching, and optional pgvector similarity with reciprocal-rank fusion to produce bounded, source-linked evidence.',
      },
      {
        title: 'Grounded conversations',
        description: 'Generate structured answers from retrieved evidence, validate source references server-side, and persist completed conversations through durable background runs.',
      },
    ],
    stack: {
      Backend: {
        technologies: ['Python 3.12', 'FastAPI', 'Pydantic', 'SQLAlchemy', 'HTTPX', 'Argon2'],
        role: 'Typed asynchronous API, authentication, repository ownership, retrieval orchestration, and answer services.',
      },
      'Data & Async Execution': {
        technologies: ['PostgreSQL 17', 'pgvector', 'Redis', 'Celery', 'asyncpg', 'Alembic'],
        role: 'Relational source of truth, vector storage, durable jobs, distributed admission controls, migrations, and worker dispatch.',
      },
      'AI & Retrieval': {
        technologies: ['Python AST', 'PostgreSQL FTS', 'pgvector', 'tiktoken', 'OpenAI Responses', 'Structured Outputs'],
        role: 'Code-aware chunking, lexical and symbol search, optional embeddings, reciprocal-rank fusion, structured generation, and citation validation.',
      },
      'Frontend & Quality': {
        technologies: ['React 19', 'TypeScript', 'Vite', 'Zod', 'SSE', 'pytest', 'Vitest', 'Ruff', 'mypy', 'Docker', 'GitHub Actions'],
        role: 'Runtime-validated interface, source inspection, conversations, run progress, streaming, strict checks, tests, containers, and CI.',
      },
    },
    challenges: [
      {
        title: 'Trustworthy grounding',
        problem: 'Model-generated paths or citations cannot be treated as authoritative, and retrieved repository text itself is untrusted input.',
        approach: 'Keep source provenance server-side, pass bounded evidence IDs to the model, validate every returned citation against the retrieved evidence set, and render final references from authoritative index metadata.',
      },
      {
        title: 'Durable asynchronous AI work',
        problem: 'Repository imports, indexing, embeddings, and model generation can outlive HTTP requests, fail mid-flight, or be delivered more than once by a queue.',
        approach: 'Store job state in PostgreSQL, use Redis/Celery only as transport, claim work with expiring lease tokens, fence stale workers, and make publication conditional and transactional.',
      },
      {
        title: 'Retrieval quality without hiding behavior',
        problem: 'Vector similarity alone can miss identifiers and exact code relationships, while retrieval changes are difficult to evaluate consistently.',
        approach: 'Keep lexical, symbol, and semantic channels independently inspectable, merge them with deterministic reciprocal-rank fusion, and compare retrieval variants against versioned evaluation fixtures.',
      },
    ],
    outcomes: [
      'Immutable, versioned repository snapshots with code-aware symbol and chunk indexing',
      'Inspectable lexical, symbol, and optional semantic retrieval with deterministic rank fusion',
      'Grounded AI answers whose citations are validated against authoritative source evidence',
      'Persistent conversations and durable background answer runs that survive browser reloads',
      'Replayable SSE lifecycle events with bounded provisional answer streaming',
      'Resource-bounded workers, ownership controls, migrations, automated tests, and CI',
    ],
  },
  'voice-notes-ai': {
  slug: 'voice-notes-ai',
  category: 'AI application',
  year: '2026',
  role: 'AI / Full-Stack Engineer',
  coreStack: [
    'Python',
    'FastAPI',
    'Faster-Whisper',
    'Ollama',
    'React',
    'TypeScript',
    'Docker',
  ],
  type: 'Personal Engineering Project',

  overview:
    'A local-first voice transcription application that turns recorded, uploaded, or pasted input into editable text using on-device speech recognition and local LLM rewriting.',

  problem:
    'Voice is fast to capture but difficult to turn into polished written content without a second editing step, while cloud transcription and language-model services can require sending recordings and transcripts to external providers.\nVoice Notes AI keeps the standard workflow local: users can record in the browser, upload audio, or paste text, then transcribe speech with Faster-Whisper and optionally rewrite the result through a locally running Ollama model.',

  pipeline: [
    {
      title: 'Capture or import',
      description:
        'Record directly in the browser with MediaRecorder, drag and drop an existing audio file, or paste a transcript into the same processing workspace.',
    },
    {
      title: 'Local transcription',
      description:
        'Validate bounded audio input, write it to a temporary processing file, and transcribe speech locally with a cached Faster-Whisper model.',
    },
    {
      title: 'Configurable text cleanup',
      description:
        'Optionally send the transcript to a local Ollama model using default, formal, or concise prompt modes while preserving the original text for comparison.',
    },
    {
      title: 'Review and reuse',
      description:
        'Present original and cleaned transcripts side by side, surface processing failures as actionable errors, and let the user copy the final text directly from the interface.',
    },
  ],

  stack: {
    Frontend: {
      technologies: [
        'React 19',
        'TypeScript',
        'Vite',
        'MediaRecorder API',
        'Lucide React',
      ],
      role:
        'Browser recording, drag-and-drop uploads, text input, processing configuration, audio previews, and transcript comparison.',
    },

    Backend: {
      technologies: [
        'Python 3.11',
        'FastAPI',
        'Pydantic',
        'HTTPX',
        'Uvicorn',
      ],
      role:
        'Typed audio and text APIs, input validation, temporary-file lifecycle management, and orchestration of local AI services.',
    },

    'Local AI': {
      technologies: [
        'Faster-Whisper',
        'Ollama',
        'Llama 3.2',
      ],
      role:
        'Local speech recognition and optional transcript rewriting without requiring a cloud AI API in the standard workflow.',
    },

    'Delivery & Quality': {
      technologies: [
        'Docker',
        'Docker Compose',
        'Nginx',
        'pytest',
        'Vitest',
        'Testing Library',
        'Oxlint',
        'GitHub Actions',
      ],
      role:
        'Reproducible local deployment, isolated AI services, automated API and client tests, static checks, builds, and continuous integration.',
    },
  },

  challenges: [
    {
      title: 'Unifying multiple input paths',
      problem:
        'Microphone recordings, uploaded audio, and pasted text have different browser lifecycles and processing requirements but need to behave as one predictable workflow.',
      approach:
        'Model the active input source explicitly, coordinate MediaRecorder and temporary object URLs, prevent conflicting input states, and route each source through a shared processing result contract.',
    },
    {
      title: 'Reliable local AI integration',
      problem:
        'Local inference services can be unavailable, slow, misconfigured, or return malformed responses, and transcript cleanup should not be required for basic speech-to-text.',
      approach:
        'Keep transcription and LLM rewriting separate, make cleanup optional, cache the Whisper model, and translate Ollama connection, timeout, missing-model, and response failures into explicit API errors.',
    },
    {
      title: 'Bounded audio processing',
      problem:
        'User-supplied audio can be empty, oversized, unsupported, corrupt, or contain no detectable speech, while temporary processing files must not be left behind.',
      approach:
        'Validate file type and size before inference, distinguish decoding and no-speech failures, process audio through temporary files, and remove them in a guaranteed cleanup path.',
    },
  ],

  outcomes: [
    'Browser microphone recording with hold-to-record keyboard input, audio previews, and drag-and-drop uploads',
    'Local Faster-Whisper transcription with configurable model, device, and compute settings',
    'Optional Ollama-powered rewriting with default, formal, and concise cleanup modes',
    'A standard local workflow that requires no third-party cloud AI API for audio or transcript processing',
    'Bounded audio validation, temporary-file cleanup, and structured FastAPI error handling',
    'Dockerized frontend, backend, and Ollama services with persistent local model storage',
    'Mocked AI integration tests, frontend API tests, production builds, linting, and GitHub Actions CI',
  ],
},
  'disagreement-aware-sexism-detection': {
    slug: 'disagreement-aware-sexism-detection',
    category: 'Multilingual NLP',
    year: '2023',
    overview: 'A multilingual transformer system that learns from annotator disagreement using soft labels rather than only majority votes.',
    problem: 'Majority-vote labels can hide meaningful disagreement and uncertainty in subjective language classification datasets.',
    pipeline: ['Annotator labels', 'Soft-label training', 'Multilingual classifiers', 'Evaluation ensemble'],
    stack: {
      Models: { technologies: ['PyTorch', 'Transformers', 'XLM-RoBERTa'], role: 'Multilingual model training' },
      Methods: { technologies: ['Soft labels', 'KL divergence'], role: 'Learning from annotator disagreement' },
      Evaluation: { technologies: ['EXIST 2023 formats'], role: 'Consistent benchmark evaluation' },
    },
    challenges: ['Representing annotator disagreement in training targets', 'Comparing hard-label and soft-label learning', 'Matching official EXIST 2023 evaluation formats'],
    outcomes: ['English and Spanish sexism classifiers', 'Hard-label and soft-label training objectives', 'Evaluation and ensemble pipelines for EXIST 2023'],
  },
  'reinforcement-learning-lab': {
    slug: 'reinforcement-learning-lab',
    category: 'Reinforcement learning',
    year: '2023',
    overview: 'A collection of classical, deep, multi-agent, and neuromorphic reinforcement-learning experiments.',
    problem: 'Understanding reinforcement learning requires comparing algorithms across control environments and learning assumptions.',
    pipeline: ['Environment setup', 'Agent training', 'Policy evaluation', 'Experiment comparison'],
    stack: {
      Frameworks: { technologies: ['PyTorch', 'Gymnasium'], role: 'Experiment implementation' },
      Algorithms: { technologies: ['Q-learning', 'DQN', 'Double DQN'], role: 'Value-based learning methods' },
      Research: { technologies: ['Multi-Agent RL', 'Neuromorphic models'], role: 'Advanced learning explorations' },
    },
    challenges: ['Comparing algorithms across different environments', 'Stabilizing deep value-learning experiments', 'Exploring neuromorphic learning abstractions'],
    outcomes: ['Reusable Q-learning, DQN, and Double DQN experiments', 'Multi-agent experiments across control environments', 'Hardware-inspired multi-weight spintronic synapse models'],
  },
  'time-series-forecasting': {
    slug: 'time-series-forecasting',
    category: 'Time-series forecasting',
    year: '2022',
    overview: 'An end-to-end machine-learning pipeline for forecasting campus electricity demand from large-scale historical time-series data.',
    problem: 'Minute-level energy demand is noisy, seasonal, and dependent on time-aware feature construction.',
    pipeline: ['Time-aware cleaning', 'Lag and rolling features', 'Model comparison', 'Demand forecast'],
    stack: {
      Models: { technologies: ['LightGBM', 'XGBoost'], role: 'Demand forecasting models' },
      Methods: { technologies: ['Time Series', 'Feature Engineering'], role: 'Time-aware data preparation' },
      Baselines: { technologies: ['Random Forest', 'Baseline models'], role: 'Model comparison reference points' },
    },
    challenges: ['Preventing temporal leakage during preprocessing', 'Working with multi-year minute-level data', 'Comparing models with time-aware evaluation'],
    outcomes: ['Multi-year, minute-level load preprocessing pipeline', 'Compared baseline, Random Forest, XGBoost, and LightGBM', 'LightGBM achieved approximately 4.97% MAPE'],
  },
  'news-popularity-prediction': {
    slug: 'news-popularity-prediction',
    category: 'Big-data machine learning',
    year: '2022',
    overview: 'A PySpark classification project for predicting whether online news articles exceed a target popularity threshold.',
    problem: 'Large article datasets require scalable preprocessing and a consistent comparison of different classification strategies.',
    pipeline: ['Distributed preprocessing', 'Feature engineering', 'Classifier training', 'Popularity prediction'],
    stack: {
      Platform: { technologies: ['PySpark', 'Spark MLlib'], role: 'Distributed data and ML processing' },
      Models: { technologies: ['Gradient-Boosted Trees', 'Random Forest', 'Linear SVM'], role: 'Popularity classification' },
      Analysis: { technologies: ['Machine Learning', 'Big Data'], role: 'Feature and model analysis' },
    },
    challenges: ['Building a repeatable distributed ML pipeline', 'Comparing linear, tree-based, and probabilistic models', 'Selecting useful features for popularity prediction'],
    outcomes: ['Repeatable PySpark preprocessing and feature-engineering pipeline', 'Compared six classification strategies', 'Evaluated popularity threshold predictions at scale'],
  },
};
