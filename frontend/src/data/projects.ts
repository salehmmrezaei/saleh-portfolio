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
  role: 'NLP / Machine Learning Engineer',
  coreStack: [
    'Python',
    'PyTorch',
    'Transformers',
    'XLM-RoBERTa',
    'mBERT',
    'scikit-learn',
    'Pandas',
  ],
  type: 'NLP Research Project',

  overview:
    'A multilingual sexism detection system that preserves annotator disagreement as probability distributions and trains transformer classifiers to model both the predicted class and the uncertainty in subjective labels.',

  problem:
    'Subjective language tasks such as sexism detection often contain genuine disagreement between human annotators. Reducing several judgments to a single majority label removes information about ambiguity and treats uncertain examples as if their labels were absolute.\nThis project preserves the full annotator vote distribution, trains multilingual classifiers against those soft targets, and evaluates performance not only globally but also across disagreement levels, languages, errors, and model behavior.',

  pipeline: [
    {
      title: 'Disagreement-aware labeling',
      description:
        'Convert multiple EXIST 2023 annotator judgments into normalized class distributions while retaining majority labels for conventional classification analysis.',
    },
    {
      title: 'Multilingual representation learning',
      description:
        'Fine-tune XLM-RoBERTa and multilingual BERT on English and Spanish posts using combined mean and max pooling over contextual token representations.',
    },
    {
      title: 'Soft-label optimization',
      description:
        'Train the primary models with KL divergence against annotator probability distributions, with a parallel cross-entropy path for hard-label experiments.',
    },
    {
      title: 'Ensemble and diagnostic evaluation',
      description:
        'Average model probabilities, write official EXIST prediction files, run benchmark evaluation, and analyze results by disagreement level, language, confidence, and error type.',
    },
  ],

  stack: {
    'Models & Training': {
      technologies: [
        'PyTorch',
        'Hugging Face Transformers',
        'XLM-RoBERTa',
        'mBERT',
        'AdamW',
      ],
      role:
        'Multilingual transformer fine-tuning, custom pooling, checkpointing, GPU-aware training, and ensemble probability inference.',
    },

    'Disagreement Learning': {
      technologies: [
        'Soft Labels',
        'KL Divergence',
        'Cross Entropy',
        'Annotator Distributions',
      ],
      role:
        'Preserve human disagreement as probabilistic supervision instead of collapsing every example into a single majority-vote target.',
    },

    'Evaluation & Analysis': {
      technologies: [
        'scikit-learn',
        'EXIST 2023 Evaluator',
        'Pandas',
        'NumPy',
        'LIME',
      ],
      role:
        'Official benchmark formatting and scoring, hard and soft metrics, disagreement- and language-stratified analysis, error analysis, and local explanations.',
    },

    Baselines: {
      technologies: [
        'TF-IDF',
        'Logistic Regression',
        'Soft Voting',
      ],
      role:
        'Provide a classical text-classification reference point and compare it with multilingual transformer-based modeling.',
    },
  },

  challenges: [
    {
      title: 'Preserving subjective supervision',
      problem:
        'Majority voting hides whether annotators strongly agreed or were evenly divided, even though that distinction is important in subjective classification.',
      approach:
        'Represent each example as an empirical label distribution and optimize predicted probabilities against that distribution with KL divergence rather than discarding minority judgments.',
    },
    {
      title: 'Consistent multilingual evaluation',
      problem:
        'English and Spanish examples must share one modeling pipeline while predictions, class ordering, soft probabilities, and evaluation files remain compatible with the official EXIST protocol.',
      approach:
        'Use multilingual encoders, enforce a stable label order throughout preprocessing and inference, normalize ensemble probabilities, and generate the exact hard/soft JSON structure required by the official evaluator.',
    },
    {
      title: 'Understanding where the model fails',
      problem:
        'A single aggregate score cannot show whether errors come from language differences, ambiguous annotations, low confidence, or systematic model behavior.',
      approach:
        'Stratify predictions by annotator disagreement and language, separate false positives and false negatives, inspect confidence margins, analyze annotator demographics, and use LIME for example-level explanations.',
    },
  ],

  outcomes: [
    'Multilingual English-Spanish sexism identification with XLM-RoBERTa and multilingual BERT',
    'Annotator vote distributions preserved as soft training targets instead of majority labels alone',
    'KL-divergence soft-label training with a conventional cross-entropy comparison path',
    'Probability-level ensemble inference with official EXIST 2023 hard and soft prediction output',
    'TF-IDF and logistic-regression baseline for comparison with transformer models',
    'Disagreement-, language-, confidence-, and error-stratified evaluation artifacts',
    'Annotator demographic analysis, LIME explanations, and CPU inference benchmarks',
  ],
},
'reinforcement-learning-lab': {
  slug: 'reinforcement-learning-lab',

  category: 'Reinforcement Learning',

  year: '2026',

  role: 'Reinforcement Learning / Machine Learning Engineer',

  coreStack: [
    'Python',
    'PyTorch',
    'Gymnasium',
    'NumPy',
    'Pandas',
    'Matplotlib',
    'TensorBoard',
  ],

  type: 'Reinforcement Learning Research Project',

  overview:
    'A reinforcement learning research lab spanning tabular Q-learning, Deep Q-Networks, Double DQN, multi-agent coordination, and hardware-aware neuromorphic learning across classic control and custom gridworld environments.',

  problem:
    'Reinforcement learning systems behave very differently as the problem moves from discrete state-action tables to neural value functions, multiple interacting agents, and hardware-constrained synaptic representations. A method that works for a small tabular environment may become unstable with function approximation, while multi-agent learning introduces non-stationarity and coordination problems, and physical synaptic hardware cannot directly reproduce arbitrary floating-point optimizer updates.\nThis project brings those settings into one experimental codebase: establish tabular and deep-RL baselines, study stabilization techniques such as replay memory and target networks, compare independent and cooperative multi-agent methods, and then translate learned Q-functions and neural-network weights into conductance-based multi-weight synaptic models.',

  pipeline: [
    {
      title: 'Environment modeling and RL baselines',

      description:
        'Build reproducible experiments around CartPole, FrozenLake, CliffWalking, and MountainCar together with custom cooperative gridworlds, starting from tabular Q-learning and environment-specific observation, reward, and episode handling.',
    },

    {
      title: 'Deep value-function learning',

      description:
        'Train neural Q-functions with PyTorch using epsilon-greedy exploration, experience replay, Bellman targets, checkpointing, and target networks, including Double DQN for MountainCar to separate next-action selection from target-value evaluation.',
    },

    {
      title: 'Multi-agent coordination',

      description:
        'Model cooperative tasks with multiple simultaneous agents and compare independent, parameter-shared, and value-factorization approaches including IQL, PS-DQN, VDN, and QMIX under repeatable multi-seed training and evaluation protocols.',
    },

    {
      title: 'Hardware-aware synaptic learning',

      description:
        'Replace idealized floating-point parameter updates with multi-weight synaptic representations whose effective values are derived from conductance states, resistive switching, magnetoresistance, and gradient-sign-driven update rules.',
    },
  ],

  stack: {
    'RL Algorithms & Training': {
      technologies: [
        'PyTorch',
        'Tabular Q-Learning',
        'DQN',
        'Double DQN',
        'Experience Replay',
        'Target Networks',
        'Epsilon-Greedy',
      ],

      role:
        'Value-based reinforcement learning, neural Q-function approximation, replay-buffer training, Bellman updates, exploration scheduling, target-network synchronization, checkpointing, and evaluation.',
    },

    'Multi-Agent Reinforcement Learning': {
      technologies: [
        'IQL',
        'Parameter-Shared DQN',
        'VDN',
        'QMIX',
        'PPO Components',
        'Centralized Training',
        'Decentralized Execution',
      ],

      role:
        'Cooperative policy learning, independent-agent baselines, parameter sharing, joint-value factorization, centralized state information, decentralized observations, and algorithm comparison.',
    },

    'Environments & Simulation': {
      technologies: [
        'Gymnasium',
        'CartPole',
        'FrozenLake',
        'CliffWalking',
        'MountainCar',
        'Custom Gridworlds',
        'NumPy',
      ],

      role:
        'Benchmark control environments, discrete and continuous observations, custom multi-agent meeting and switch-door tasks, reproducible resets, environment wrappers, and task-specific simulation.',
    },

    'Neuromorphic & Evaluation': {
      technologies: [
        'Multi-Weight Synapses',
        'Spintronic Conductance Modeling',
        'Memristive Q-Functions',
        'Pandas',
        'Matplotlib',
        'TensorBoard',
        'pytest',
      ],

      role:
        'Hardware-inspired parameter representation, task-specific effective weights, conductance and noise modeling, experiment logging, multi-seed aggregation, weight visualization, reports, and implementation tests.',
    },
  },

  challenges: [
    {
      title: 'Stabilizing learning across heterogeneous environments',

      problem:
        'The repository spans discrete gridworlds and classic-control tasks with different observation spaces, reward structures, episode lengths, and learning dynamics, so one training setup cannot be applied unchanged everywhere.',

      approach:
        'Separate environment-specific behavior from reusable agent logic, use replay memories and epsilon-greedy exploration, introduce target networks for deep value learning, apply Double DQN where overestimation is a concern, and keep seeds, hyperparameters, checkpoints, and evaluation loops explicit for reproducible experiments.',
    },

    {
      title: 'Learning coordination between multiple agents',

      problem:
        'In cooperative environments, each agent changes while the others are learning, making the environment effectively non-stationary; independent policies may fail to coordinate, while parameter sharing can prevent agents from learning sufficiently distinct behavior.',

      approach:
        'Implement multiple coordination strategies rather than assuming one formulation is universally better: compare independent Q-learning, parameter-shared DQN, VDN, and QMIX on the same meeting task, use shared experimental protocols and multi-seed evaluation, and explore centralized information with decentralized action selection for cooperative environments.',
    },

    {
      title: 'Bridging software learning and physical synapses',

      problem:
        'Standard neural-network optimizers assume continuously adjustable floating-point parameters, while neuromorphic and spintronic devices expose discrete or constrained conductance states, device noise, and task-dependent effective weights.',

      approach:
        'Represent Q-values and neural parameters through multi-weight synaptic devices, derive effective weights from parallel and antiparallel conductance states, model resistive and magnetoresistive behavior, and use the sign of backpropagated gradients to drive physically motivated crosspoint updates instead of conventional optimizer steps.',
    },
  ],

  outcomes: [
    'Tabular Q-learning, DQN, and Double DQN experiments across CartPole, FrozenLake, CliffWalking, and MountainCar',

    'Modular agents, neural Q-networks, replay memories, environment wrappers, training loops, checkpoints, and evaluation utilities',

    'Double DQN MountainCar training with separate online and target networks for action selection and target evaluation',

    'Cooperative multi-agent experiments covering IQL, parameter-shared DQN, VDN, and QMIX with repeatable multi-seed evaluation',

    'Custom meeting-gridworld and switch-door environments for studying synchronization, cooperation, decentralized observations, and centralized state information',

    'Tabular and deep-RL experiments using multi-weight synaptic, memristive, and spintronic representations instead of conventional software-only weights',

    'Hardware-aware CartPole learning with task-specific conductance-derived weights, gradient-sign updates, device-noise modeling, experiment logs, reports, and weight visualizations',
  ],
},
'time-series-forecasting': {
  slug: 'time-series-forecasting',

  category: 'Time-Series Forecasting',

  year: '2026',

  role: 'Machine Learning / Data Science Engineer',

  coreStack: [
    'Python',
    'Pandas',
    'NumPy',
    'scikit-learn',
    'XGBoost',
    'LightGBM',
    'Matplotlib',
  ],

  type: 'Applied Machine Learning Project',

  overview:
    'An end-to-end electrical load forecasting pipeline that transforms irregular minute-level campus power data into leakage-safe temporal features and compares ensemble machine learning models for short-term 15-minute load prediction.',

  problem:
    'Real-world energy data is rarely a clean, uniformly sampled time series. The Savona Campus dataset contains several years of electrical-load measurements with mixed timestamp precision, negative readings, duplicated timestamps, thousands of discontinuities, and missing periods ranging from minutes to multiple weeks.\nThis project was built to turn that noisy historical record into a defensible forecasting dataset without fabricating long stretches of demand, then capture daily, weekly, and recent-load dependencies through temporal feature engineering and evaluate whether machine learning models can outperform a simple historical persistence forecast on genuinely future data.',

  pipeline: [
    {
      title: 'Temporal Data Quality Layer',

      description:
        'Transform irregular minute-level electrical measurements into a trustworthy time series by normalizing mixed timestamp formats, resolving duplicate timestamps, preserving invalid readings as missing values, reconstructing the expected one-minute index, and explicitly measuring missing intervals before any modeling step.',
    },

    {
      title: 'Gap-Aware Signal Reconstruction',

      description:
        'Apply different recovery policies according to gap duration and operational context: interpolate only short interruptions, use bounded forward propagation during stable night-time periods, preserve long outages as unknown rather than synthesizing demand, and aggregate the validated signal into 15-minute forecasting intervals.',
    },

    {
      title: 'Leakage-Safe Temporal Feature Layer',

      description:
        'Convert the cleaned signal into a supervised learning matrix using calendar context, autoregressive lags at 15-minute, hourly, daily, and weekly horizons, and shifted rolling statistics that summarize recent level and volatility without exposing the current target value.',
    },

    {
      title: 'Chronological Forecasting & Model Selection',

      description:
        'Preserve temporal causality with an ordered train/test boundary, establish a previous-week persistence benchmark, train Random Forest, XGBoost, and LightGBM regressors on the same feature space, and compare them using MAE, RMSE, MAPE, prediction traces, and feature-importance analysis.',
    },
  ],

  stack: {
    'Data Processing': {
      technologies: [
        'Python',
        'Pandas',
        'NumPy',
        'Datetime Processing',
        'Interpolation',
        'Resampling',
      ],

      role:
        'Mixed-format timestamp parsing, minute-grid reconstruction, invalid-value handling, duplicate removal, bounded gap filling, long-gap filtering, and 15-minute load aggregation.',
    },

    'Time-Series Features': {
      technologies: [
        'Calendar Features',
        'Lag Features',
        'Rolling Means',
        'Rolling Standard Deviation',
        'Autoregressive Features',
      ],

      role:
        'Encode time-of-day, weekday, seasonality, recent load history, daily recurrence, weekly recurrence, local trends, and recent volatility while preventing target leakage.',
    },

    'Forecasting Models': {
      technologies: [
        'scikit-learn',
        'Random Forest',
        'XGBoost',
        'LightGBM',
        'Persistence Baseline',
      ],

      role:
        'Supervised short-term load forecasting, chronological training, tree-ensemble comparison, gradient boosting, and benchmarking against historical load persistence.',
    },

    'Evaluation & Analysis': {
      technologies: [
        'MAE',
        'RMSE',
        'MAPE',
        'Matplotlib',
        'Seaborn',
        'Feature Importance',
        'Google Colab',
      ],

      role:
        'Forecast-error measurement, exploratory analysis, seasonal and outlier inspection, model comparison, prediction visualization, and interpretation of influential temporal predictors.',
    },
  },

  challenges: [
    {
      title: 'Recovering a Forecastable Signal Without Inventing Data',

      problem:
        'The source series was not simply incomplete: it contained mixed timestamp precision, duplicate observations, invalid negative measurements, 4,721 discontinuity events, and 179,468 missing minute-level timestamps, including outages extending for days or weeks. Treating every gap with interpolation would create artificial demand patterns and contaminate downstream training.',

      approach:
        'Reconstruct the complete expected time index first so missingness becomes explicit, then separate short recoverable gaps from long outages. Limit interpolation to short sequences, constrain night-time forward filling to a bounded horizon, and discard unresolved long-gap intervals instead of allowing imputation assumptions to dominate the learned signal.',
    },

    {
      title: 'Designing Temporal Features Without Future Leakage',

      problem:
        'Lag and rolling-window features can produce deceptively strong forecasting results when the current observation or future information leaks into the feature vector. Random train/test splitting introduces the same problem by allowing later temporal regimes into training.',

      approach:
        'Build all rolling statistics from explicitly shifted series, fit models only on historical observations, retain lag dependencies at operationally meaningful horizons, and evaluate against a strictly later test period so model quality reflects genuine forward prediction rather than temporal contamination.',
    },

    {
      title: 'Distinguishing Rare Events From Valid Demand Regimes',

      problem:
        'A conventional IQR rule identified 7.23% of 15-minute observations as outliers. Removing them mechanically would simplify the distribution but could erase legitimate heating, cooling, or high-activity demand periods—the exact conditions an energy forecasting system must handle reliably.',

      approach:
        'Treat statistical outlier detection as an analysis tool rather than an automatic deletion rule. Examine when high-load observations occur, preserve plausible seasonal peaks, and allow tree-based models to learn those regimes while evaluating performance against an explicit persistence baseline.',
    },
  ],

  outcomes: [
    'Converted noisy minute-level campus measurements into an explicit 2,988,584-timestamp temporal index, exposing 179,468 previously missing observations across 4,721 gap events',

    'Designed a gap-aware reconstruction strategy that recovers short interruptions while avoiding synthetic reconstruction of multi-day and multi-week outages',

    'Produced a validated 15-minute forecasting dataset with 188,132 usable observations and a final supervised learning matrix of 187,460 samples',

    'Engineered 15 leakage-safe temporal predictors spanning calendar context, short-term autoregression, daily and weekly recurrence, rolling demand levels, and recent volatility',

    'Evaluated models using a true forward holdout: training on historical data through August 2022 and testing on later observations through September 2023',

    'Reduced MAPE from 20.76% with the previous-week persistence benchmark to 5.14% with Random Forest, 4.99% with XGBoost, and 4.97% with LightGBM',

    'Achieved 5.07 MAE and 7.70 RMSE with LightGBM across 37,492 held-out future observations',

    'Confirmed through feature importance that immediate load history, hour-of-day behavior, and daily/weekly recurrence carry the strongest predictive signal',
  ],
},
'news-popularity-prediction': {
  slug: 'news-popularity-prediction',

  category: 'Big Data Analytics',

  year: '2026',

  role: 'Big Data / Machine Learning Engineer',

  coreStack: [
    'Python',
    'PySpark',
    'Apache Spark',
    'Spark MLlib',
    'Pandas',
    'scikit-learn',
    'Docker',
  ],

  type: 'Big Data Machine Learning Project',

  overview:
    'A Spark-based decision support system for predicting online news popularity before publication, using article-derived features, scalable binary classification, cross-validated model comparison, and feature-level interpretation.',

  problem:
    'Predicting whether an online article will become popular is difficult because popularity depends on interacting signals from keywords, topic, publication timing, article structure, and previously observed content characteristics rather than one dominant feature. The prediction also needs to be formulated without directly exposing the eventual number of shares to the model.\nThis project treats popularity as a scalable binary classification problem over the Online News Popularity dataset: articles with more than 1,400 shares are labeled popular, leakage-prone identifiers and the original share count are excluded, heterogeneous classifiers are trained through Spark MLlib, and their ranking quality, classification performance, hyperparameters, and important predictive features are compared.',

  pipeline: [
    {
      title: 'Leakage-Safe Spark Data Layer',

      description:
        'Load the 39,644-article dataset into Spark, normalize the schema, derive a binary popularity target from the 1,400-share threshold, inspect class balance, and remove both the final share count and URL identifier before any predictive feature construction.',
    },

    {
      title: 'Model-Aware Feature Pipeline',

      description:
        'Assemble article attributes into Spark ML feature vectors while maintaining preprocessing paths that respect algorithm requirements: standardized vectors for linear and general classifiers, and independently fitted non-negative features for Multinomial and Complement Naive Bayes.',
    },

    {
      title: 'Multi-Family Classification Benchmark',

      description:
        'Evaluate complementary model families rather than a single algorithm class: linear decision boundaries with Logistic Regression and Linear SVC, probabilistic learning with Naive Bayes, standalone tree learning, and nonlinear ensemble methods with Random Forest and Gradient-Boosted Trees.',
    },

    {
      title: 'Cross-Validated Selection & Explainability',

      description:
        'Tune model-specific capacity and regularization parameters through three-fold Spark CrossValidator experiments, evaluate the selected estimators on a fixed held-out partition, and map coefficients and tree importance vectors back to semantic article features for model interpretation.',
    },
  ],

  stack: {
    'Big Data Platform': {
      technologies: [
        'Apache Spark 3.5',
        'PySpark',
        'Spark DataFrames',
        'Spark SQL',
        'Docker',
        'Docker Compose',
      ],

      role:
        'Distributed dataset processing, transformation, model execution, reproducible local Spark infrastructure, and scalable experimentation over the complete news dataset.',
    },

    'Feature Engineering': {
      technologies: [
        'VectorAssembler',
        'StandardScaler',
        'MinMaxScaler',
        'Spark SQL Functions',
        'Binary Labeling',
      ],

      role:
        'Construct model-ready feature vectors, prevent target leakage, fit preprocessing from training data only, standardize heterogeneous numerical attributes, and satisfy model-specific feature constraints.',
    },

    'Classification & Tuning': {
      technologies: [
        'Gradient-Boosted Trees',
        'Random Forest',
        'Linear SVC',
        'Logistic Regression',
        'Decision Tree',
        'Naive Bayes',
        'CrossValidator',
        'ParamGridBuilder',
      ],

      role:
        'Compare ensemble, linear, probabilistic, and tree-based classifiers and tune regularization, ensemble size, tree complexity, boosting iterations, and smoothing through Spark-native cross-validation.',
    },

    'Evaluation & Interpretation': {
      technologies: [
        'ROC-AUC',
        'Accuracy',
        'F1 Score',
        'Precision',
        'Recall',
        'Pandas',
        'Matplotlib',
        'Seaborn',
        'scikit-learn',
      ],

      role:
        'Evaluate held-out classification behavior, visualize ROC curves, compare tuned models, inspect coefficients and tree importance scores, and perform focused correlation analysis on influential predictors.',
    },
  },

  challenges: [
    {
      title: 'Constructing a Valid Pre-Publication Target',

      problem:
        'Popularity is defined using the final number of shares, but that same field is present in the source dataset. If it remains in the feature matrix, the classifier effectively receives the answer during training and evaluation, producing meaningless performance.',

      approach:
        'Derive the binary target first using the literature-based threshold of more than 1,400 shares, validate the resulting class distribution, and then explicitly remove the raw share count and article URL before feature-vector assembly.',
    },

    {
      title: 'Supporting Heterogeneous Models in One Spark Workflow',

      problem:
        'The candidate algorithms have incompatible assumptions: Naive Bayes requires non-negative features, linear models are sensitive to feature scale, tree ensembles expose different capacity controls, and Linear SVC does not provide the same probability interface used for ROC-based analysis.',

      approach:
        'Separate preprocessing where mathematically necessary while keeping the train/test boundary common. Fit every scaler only on training data, use MinMaxScaler for Naive Bayes, StandardScaler for the shared vector representation, and evaluate each classifier only with metrics supported by its output semantics.',
    },

    {
      title: 'Balancing Predictive Performance With Explainability',

      problem:
        'A content-popularity classifier is more useful as a decision-support system when it can explain which characteristics influence predictions. Ensemble models improve nonlinear modeling capacity, but their decisions are harder to interpret than those of linear baselines.',

      approach:
        'Benchmark both interpretable and higher-capacity models, use cross-validation for fair model selection, extract Logistic Regression coefficients and tree-based feature importances, compare recurring top-ranked features across estimators, and analyze correlations among the shared signals.',
    },
  ],

  outcomes: [
    'Built an end-to-end Spark ML classification workflow over 39,644 articles and 61 original dataset attributes',

    'Converted continuous engagement into a literature-aligned binary decision target, yielding a nearly balanced dataset of 19,562 popular and 20,082 unpopular articles',

    'Eliminated direct target leakage by separating label construction from predictive features and removing the original share count before model training',

    'Implemented and compared six Spark MLlib classifiers spanning linear, probabilistic, single-tree, bagging, and boosting approaches',

    'Established reproducible model selection through deterministic 70/30 holdout evaluation and model-specific three-fold cross-validation',

    'Selected a tuned Gradient-Boosted Tree configuration with depth 3 and 100 boosting iterations, reaching 0.7254 ROC-AUC, 66.87% accuracy, and 0.6686 F1 on 11,683 held-out articles',

    'Validated Logistic Regression as a competitive interpretable baseline at approximately 0.7007 ROC-AUC, providing a useful comparison between linear transparency and nonlinear ensemble performance',

    'Identified recurring predictive signals across model families, including keyword statistics, weekend publication, self-reference engagement, topic/channel indicators, article recency, and latent topic features',

    'Packaged the experiments in a reproducible Apache Spark 3.5 environment with fixed dependencies, Docker configuration, cross-validation, ROC analysis, model-comparison visualizations, and feature-level interpretation',
  ],
},
};
