"""Repository-grounded portfolio chatbot context; audit notes are outside this module."""

PROJECT_KNOWLEDGE = {
    "repopilot-ai": {
        "title": "RepoPilot AI",
        "aliases": ["RepoPilot", "RepoPilot AI", "repopilot-ai", "repository intelligence assistant"],
        "keywords": ["repopilot", "repository understanding", "codebase Q&A", "GitHub repository import", "FastAPI", "React", "PostgreSQL", "pgvector", "Redis", "Celery", "RAG", "hybrid code search", "grounded answers", "investigation agent", "patch proposal", "sandbox execution"],
        "role": "Project published under Saleh's GitHub account; individual authorship of each module is not separately established.",
        "year": "2026 (documented October 2026 source and CI review)",
        "type": "Full-stack codebase intelligence and controlled software-engineering workflow application",
        "overview": "RepoPilot imports GitHub repository snapshots and supports indexed source browsing, keyword/symbol search, optional embedding-backed retrieval, and LLM-generated answers with source references. The same application contains bounded investigation agents, reviewable patch proposals, saved pull-request reviews, and opt-in test execution and repair workflows. It is implemented as a modular monolith, not as independently deployed microservices. Features that depend on external credentials or a sandbox host are implemented in source but are not proven operational in a public production environment.",
        "problem": "Developers need a way to locate relevant code, explain implementation details from inspectable evidence, and investigate changes without granting an autonomous assistant authority to write to GitHub or run arbitrary repository code on the application host.",
        "architecture": "A React/TypeScript/Vite frontend calls an async FastAPI backend. PostgreSQL owns users/sessions, repository source snapshots, Python and TypeScript indexes, search generations, conversation history, durable run states, events, and provider-usage receipts. pgvector stores optional embedding vectors alongside search documents. Redis is used for Celery delivery and shared rate limiting, while a database-backed dispatcher republishes eligible jobs. Celery workers handle import, indexing, search preparation, answering, investigation and execution/repair orchestration. Server-sent events relay persisted run events, including recoverable progress and provisional answer text. A separate, explicitly configured sandbox host is the boundary for approved tests; it is not the web/worker host.",
        "pipeline": [
            {"title": "Import immutable source", "description": "Resolve GitHub repository metadata and a commit, obtain a bounded archive, reject unsafe paths and exclude unsupported or sensitive-looking files, then transactionally persist retained source files and their commit provenance. The import path is archive-based, not a git-clone/history analyzer."},
            {"title": "Static code index", "description": "Parse Python with ast and TypeScript/TSX with tree-sitter under budgets; extract declarations, locations and signatures, then create non-overlapping, byte-bounded exact source slices. Parsing failures fall back to text chunks. Source is treated as data rather than executed."},
            {"title": "Prepare search generation", "description": "Create versioned PostgreSQL search documents from the completed source index. Keyword search works without paid embeddings. Optional OpenAI embeddings use a configured, version-checked provider profile and token budgets; preparation is durable and lease-fenced."},
            {"title": "Retrieve and rank evidence", "description": "PostgreSQL simple full-text lexical ranking and exact symbol-name matching each return bounded candidates. Hybrid mode also runs exact pgvector cosine search restricted to the selected completed search generation. Deduplicate and fuse channels with reciprocal rank fusion, 1/(60 + rank); optionally apply a deterministic local metadata/body-overlap reranker. Build token-bounded evidence carrying immutable commit, path and line references."},
            {"title": "Answer and cite", "description": "Pass bounded JSON evidence and recent bounded conversation context to a configured generation provider. The structured answer contains claims and citation IDs. Validate that IDs are unique per claim and belong to retrieved evidence; without evidence the service abstains instead of invoking generation. Validation checks reference membership, not whether cited source actually entails each claim."},
            {"title": "Investigate, propose, and optionally execute", "description": "Bounded agent calls search/read tools and produces a reviewable diff subject to proposal guards. Saved PR review and explicit approval precede optional sandbox baseline/patched tests. A bounded repair controller records revisions and stop reasons; proposals are not automatically pushed or posted to GitHub."}
        ],
        "stack": {
            "Frontend": {"technologies": ["React", "TypeScript", "Vite"], "role": "Repository browsing, index/search inspection, answer citations, conversations, agent and execution timelines, review UI."},
            "API and persistence": {"technologies": ["Python", "FastAPI", "SQLAlchemy async", "PostgreSQL", "Alembic"], "role": "Authenticated APIs, ownership enforcement, snapshot relationships, durable state transitions and migrations."},
            "Search and embeddings": {"technologies": ["PostgreSQL full-text search", "pgvector", "Python ast", "tree-sitter", "OpenAI embeddings via HTTPX", "tiktoken"], "role": "Static indexing, lexical and exact-symbol search, optional cosine search and bounded evidence construction."},
            "Generation and orchestration": {"technologies": ["OpenAI Responses API via HTTPX", "Celery", "Redis", "server-sent events"], "role": "Optional grounded model calls, durable background work, shared throttling and progress streaming."},
            "Isolation and deployment definitions": {"technologies": ["Docker", "Docker Compose", "dedicated rootless-Docker sandbox design", "Caddy", "Prometheus"], "role": "Local/production stack definitions, optional isolated testing, monitoring configuration; live deployment validation remains outstanding."},
            "Quality": {"technologies": ["pytest", "Vitest", "GitHub Actions", "Ruff", "mypy"], "role": "Unit/API/integration checks, frontend tests, static checks and container builds."}
        },
        "engineering_details": [
            "Search deliberately uses PostgreSQL full-text plus existing symbol metadata and pgvector, avoiding a separate vector service. Exact vector retrieval is filtered by a completed source generation rather than using an approximate global ANN index.",
            "Source snapshots and search generations have provenance and profile/version boundaries; composite foreign keys protect links between chunks, files and search documents.",
            "Database job rows, conditional lease tokens, expiry and dispatcher republishing protect against broker-loss windows, duplicate delivery, cancellation races and stale worker publication. This is at-least-once delivery with fenced effects, not exactly-once external API execution.",
            "Answer worker completion, run event and conversation messages are committed together; cancelled or expired runs cannot publish late answers. Provisional SSE output is not equivalent to finalized validated history.",
            "Usage receipts record known embedding and generation token usage even if answer publication fails; unknown usage is not represented as zero.",
            "The local reranker adds bounded query/body and metadata overlap plus exact symbol bonuses; it is not a neural cross-encoder.",
            "The citation checker rejects unknown or duplicate reference IDs, but does not verify semantic entailment. The chatbot should never describe the citations as formally proving factual correctness.",
            "The backend contains bounded investigation, proposal diff checking, execution and repair code. The project documentation explicitly separates source completeness and CI checks from real OAuth, model and sandbox acceptance."
        ],
        "challenges": [
            {"title": "Trustworthy source grounding", "problem": "Generated explanations can refer to nonexistent files or unsupported references.", "approach": "Give the model bounded source evidence identified by immutable provenance; validate structured citation IDs and refuse source-free answers. Keep human assessment of citation support as a separate, still-needed quality task."},
            {"title": "Durable async work", "problem": "Queue duplication, broker loss, worker restarts and user cancellation can otherwise produce stranded or stale operations.", "approach": "Persist authoritative states in PostgreSQL, republish queued work through a dispatcher, claim with expiring lease tokens and fence transactional publication."},
            {"title": "Cost and retrieval scope", "problem": "Embedding entire repositories and answering long queries can have unpredictable provider cost and context size.", "approach": "Keep keyword mode free of provider calls, use explicit embedding preparation and quotas, cap candidate/chunk/context sizes, and record estimated versus known usage."},
            {"title": "Untrusted code execution", "problem": "Tests of imported repositories must not inherit application credentials or host privileges.", "approach": "Define a separate sandbox service with immutable-image preflight, rootless-Docker requirements, no network, read-only filesystem, non-root user and CPU/memory/process/time restrictions. Its opt-in real-host acceptance is not established by the recorded CI run."}
        ],
        "security_and_reliability": [
            "Session auth uses password hashing, server-side session ownership checks and CSRF/origin protections; shared Redis rate limits guard selected operations.",
            "GitHub URLs and archive processing are constrained; imported source is neither installed nor executed during indexing, and content is escaped in the frontend.",
            "Queries, evidence and model calls are bounded; provider adapters are configured on the server rather than accepting client-supplied provider endpoints.",
            "Sandbox execution is conditional on explicit approval and a dedicated configured host. The implementation rejects absent or insecure rootless-Docker enforcement; no blanket security certification is claimed.",
            "The design does not push patches, post PR reviews, or autonomously modify hosted repositories."
        ],
        "testing_and_quality": [
            "Backend unit/API tests and PostgreSQL/Redis integration cases exercise indexing, retrieval, conversations, leases, agent and execution paths; sandbox cases are opt-in.",
            "Synthetic retrieval, answer, agent and coding evaluation fixtures/runners exist; mock-provider results are not real-model factual accuracy scores.",
            "A 6 October 2026 documented main-branch GitHub Actions run succeeded on non-sandbox tests and static checks. Its six opt-in sandbox tests were skipped.",
            "Repository docs explicitly request real-provider quality evaluation, sandbox-host validation and production operational acceptance."
        ],
        "outcomes": [
            "Source release includes implemented code-understanding, durable chat and bounded engineering-workflow paths.",
            "Recorded CI validates backend/frontend suites, schema migration checks and container builds; this establishes regression checks, not production usage or retrieval quality.",
            "Strongest portfolio evidence for backend architecture, RAG plumbing, asynchronous job safety and API design among these six repositories."
        ],
        "verified_metrics": [
            "GitHub Actions run #65, 6 October 2026, commit 6fcaab0: completed successfully (GitHub run metadata).",
            "Run #65 documented backend non-integration suite: 358 tests passed; 18 integration tests deselected.",
            "Run #65 documented infrastructure integration suite: 12 passed and 6 opt-in sandbox tests skipped.",
            "Run #65 documented frontend: 69 tests passed across 16 files. These are test counts, not code coverage or model-quality measures."
        ],
        "limitations": [
            "No verified public production usage, uptime, business adoption, or end-to-end live OAuth/private-repository acceptance is established.",
            "No verified live-model grounded-answer correctness, retrieval superiority, or citation entailment score is established.",
            "The recorded CI did not exercise the six opt-in sandbox cases; production isolation and HTTPS/backup/restore gates remain environment-specific.",
            "Optional embedding/generation paths depend on provider configuration, consent, budgets and external service availability.",
            "A source-checked patch proposal is not a merged PR; autonomous GitHub writes are intentionally out of scope."
        ],
        "retrieval_terms": ["repopilot", "repopilot ai", "repo pilot", "codebase", "repository intelligence", "github import", "commit pinned", "source snapshot", "static indexing", "python ast", "typescript tsx", "tree sitter", "symbol search", "lexical search", "semantic retrieval", "hybrid retrieval", "reciprocal rank fusion", "rrf", "pgvector", "postgresql", "exact cosine", "search generations", "chunking", "source citations", "citation validation", "grounded answers", "rag", "conversation history", "sse", "celery", "redis", "durable jobs", "leases", "job dispatcher", "openai embeddings", "usage receipts", "agent tools", "diff proposals", "pr review", "sandbox", "test execution", "repair loop", "backend engineering"]
    },
    "voice-notes-ai": {
        "title": "Voice Notes AI",
        "aliases": ["Voice Notes", "Voice Notes AI", "voice-notes-ai", "local voice transcription"],
        "keywords": ["voice notes", "speech to text", "transcription", "Faster-Whisper", "Ollama", "Llama 3.2", "local inference", "React", "FastAPI", "browser recording", "audio upload", "privacy"],
        "role": "Application in Saleh's GitHub repository; individual component attribution is not independently confirmed.",
        "type": "Local-first speech transcription and LLM transcript cleanup web application",
        "overview": "Users can record in the browser, upload supported audio, or paste existing text. The FastAPI backend transcribes uploaded audio using a locally instantiated Faster-Whisper model and can optionally send the transcript to a configured local Ollama chat endpoint for cleanup. Both original and processed text are returned for display. The standard Compose stack does not require a cloud AI API; this is a deployment-mode privacy characteristic, not a promise that every hosting configuration is private.",
        "problem": "Convert casual spoken notes into editable text and optionally improve readability without requiring a third-party transcription or LLM service in the normal self-hosted configuration.",
        "architecture": "React/TypeScript/Vite frontend uses browser MediaRecorder, file input and text forms; it posts JSON to POST /text/process or multipart audio to POST /audio/process. FastAPI coordinates validation, local speech decoding and an HTTPX call to Ollama /api/chat. Faster-Whisper is lazily instantiated and cached with lru_cache. Docker Compose defines separate nginx-served frontend, backend and Ollama containers, and a model-storage volume for Ollama.",
        "pipeline": [
            {"title": "Capture input", "description": "Record with the browser, use hold-V-to-record controls or upload an audio file; alternatively submit already transcribed text."},
            {"title": "Validate and transcribe", "description": "Check filename extension, empty bytes and configured size cap; write upload to a temporary file, invoke cached Faster-Whisper with beam search, join segment text and reject empty-speech results."},
            {"title": "Optionally clean", "description": "Use default, formal or short system prompts and a non-streaming Ollama chat call. When clean_with_llm is false, return original text unchanged and do not call Ollama."},
            {"title": "Respond and clean up", "description": "Return original and cleaned text plus audio metadata. A finally block deletes the temporary upload file even on errors; frontend supports comparison and copying."}
        ],
        "stack": {
            "Frontend": {"technologies": ["React", "TypeScript", "Vite", "MediaRecorder API"], "role": "Recording, uploads, text editing, settings, transcript comparison and API requests."},
            "Backend": {"technologies": ["Python", "FastAPI", "Pydantic", "HTTPX"], "role": "Input validation, two processing routes, error responses and inference orchestration."},
            "Local models": {"technologies": ["Faster-Whisper", "Ollama", "Llama 3.2 (default configured model)"], "role": "On-host speech recognition and optional local LLM transcript rewriting."},
            "Infrastructure and checks": {"technologies": ["Docker Compose", "Docker", "nginx", "pytest", "Vitest", "Testing Library", "GitHub Actions"], "role": "Three-service local stack, automated route/client checks, frontend build and lint."}
        },
        "engineering_details": [
            "Whisper defaults to the base model with CPU/int8 settings; these are configurable, not measured hardware or performance claims.",
            "The audio handler accepts named extension types and enforces a default 25 MiB limit; its current implementation reads the upload fully before checking that limit, so it is not a streaming-size guard.",
            "The Ollama adapter posts system and user messages with stream=false, a 120-second HTTP timeout, and distinguishes connection failure, missing model, timeout, malformed result and unexpected status.",
            "Cleanup prompts explicitly request preservation of facts and meaning, but the application does not have a factual-equivalence validator.",
            "No repository-backed transcript database/history or account system appears in the examined application code."
        ],
        "challenges": [
            {"title": "Local privacy boundary", "problem": "Cloud transcription would expose voice content to an external AI API.", "approach": "Route processing through local Faster-Whisper and a local Ollama endpoint in the standard Compose deployment; qualify privacy by actual deployment network and host controls."},
            {"title": "Unreliable inputs and local-model availability", "problem": "Unsupported files, silence, corrupt audio, a missing Ollama model or slow local inference can interrupt the workflow.", "approach": "Validate inputs, return distinct HTTP errors, make LLM cleanup optional and always delete temporary upload files."}
        ],
        "security_and_reliability": [
            "Standard Compose inference is local rather than a cloud AI service; the container ports are published, so host/network exposure and retention depend on deployment.",
            "Temporary audio files are removed in a finally block; no persistent transcript store is implemented in the inspected backend.",
            "Input and mode validation, controlled CORS development origins, predictable API errors and optional LLM bypass are implemented.",
            "Privacy is a design property, not formal encryption, authentication or security-audit evidence."
        ],
        "testing_and_quality": ["Backend pytest files cover audio/text routes, health, invalid uploads and mocked inference failures.", "Frontend includes API-client Vitest tests; GitHub Actions runs backend pytest and frontend lint, build and Vitest.", "The repository does not provide a reviewed speech-accuracy benchmark or measured inference latency."],
        "outcomes": ["Implemented record/upload/paste-to-transcript workflow with optional rewriting modes.", "Docker Compose and CI definitions provide reproducible development/test setup."],
        "verified_metrics": [],
        "limitations": ["No verified word error rate, transcript cleanup accuracy, privacy audit, production uptime or user statistics.", "Local inference requires available Faster-Whisper model assets and a working Ollama installation/model for cleanup.", "No diarization, timestamped transcript export, durable history or user auth is shown in the current backend; the README calls several of these future improvements.", "The current audio size check follows reading the entire upload into memory."],
        "retrieval_terms": ["voice notes ai", "voice-notes-ai", "voice recording", "voice memo", "speech to text", "transcription", "whisper", "faster whisper", "local speech recognition", "ollama", "llama 3.2", "local llm", "privacy", "offline transcription", "audio upload", "microphone", "mediarecorder", "transcript cleanup", "formal mode", "short mode", "filler words", "temporary files", "fastapi", "react", "docker compose"]
    },
    "disagreement-aware-sexism-detection": {
        "title": "Disagreement-Aware Sexism Detection",
        "aliases": ["Learning from Disagreement for Multilingual Sexism Detection", "disagreement-aware-sexism-detection", "EXIST 2023 sexism detection"],
        "keywords": ["EXIST 2023", "sexism detection", "annotator disagreement", "soft labels", "multilingual NLP", "XLM-RoBERTa", "multilingual BERT", "KL divergence", "PyTorch", "classification", "ensemble"],
        "role": "Research code published in Saleh's GitHub repository; no component-by-component contribution attribution verified.",
        "type": "Multilingual NLP classification and human-label-disagreement experiment",
        "overview": "A PyTorch pipeline for English/Spanish EXIST 2023 sexism identification (Task 1). Rather than using only a majority class, it can use each post's empirical [NO, YES] annotator vote proportions as a soft target. The code also contains a distinct Task 2 three-class training script and Task 3 preprocessing/analysis helpers; the README still describes Task 2 and Task 3 as unimplemented. Do not interpret the Task 3 preprocessing code as a trained Task 3 classifier.",
        "problem": "Subjective labels can mask annotation uncertainty when collapsed to majority vote; the system preserves vote distributions for learning and analyzes errors as disagreement increases.",
        "architecture": "Data loaders convert EXIST JSON records into Pandas frames with text, language, soft vote distributions and hard labels. A PyTorch Dataset tokenizes each post using Hugging Face tokenizers, pads/truncates to the configured maximum length and returns correctly typed labels. TransformerModel wraps a pretrained multilingual AutoModel, attention-masked mean and max pooling, concatenation, dropout and a linear classification head. The trainer chooses KL-divergence soft-target loss or cross-entropy from target tensor dtype. Training scripts fit models, save lowest-validation-loss checkpoints and average softmax predictions; prediction writers export the EXIST JSON schema. A separate official evaluation script can score saved predictions.",
        "pipeline": [
            {"title": "Represent annotation disagreement", "description": "Filter invalid Task 1 votes, count NO/YES, normalize to a two-element probability vector and derive a majority-class target for classical evaluation. Ties map to NO in the Task 1 hard-label rule."},
            {"title": "Tokenize and encode", "description": "Use xlm-roberta-base and bert-base-multilingual-cased tokenizers/encoders; create fixed-length input IDs and attention masks."},
            {"title": "Train with soft or hard labels", "description": "Mean-pool and max-pool nonpadding encoder states, concatenate, apply dropout and classify. KLDivLoss(batchmean) compares log-softmax outputs with annotator target probabilities; hard labels use CrossEntropyLoss."},
            {"title": "Ensemble and evaluate", "description": "Average per-model predicted probabilities, emit hard and soft Task 1 prediction JSON and compute internal classification/soft metrics. Official EXIST evaluation is a separate invocation, and internal KL similarity is not the official ICM-Soft score."},
            {"title": "Inspect difficult cases", "description": "Scripts analyze results by language, vote pattern, disagreement group and false-positive/false-negative category; a separate TF-IDF/logistic regression baseline writes a classification report."}
        ],
        "stack": {
            "NLP models": {"technologies": ["PyTorch", "Hugging Face Transformers", "XLM-RoBERTa", "multilingual BERT"], "role": "Trainable multilingual encoder and classification head."},
            "Data and evaluation": {"technologies": ["Python", "Pandas", "NumPy", "scikit-learn", "EXIST 2023 evaluator"], "role": "Vote distributions, hard baselines, classification scores, official-format prediction output and error analyses."},
            "Explainability": {"technologies": ["LIME"], "role": "Scripts and saved example explanations; not evidence of general causal interpretability."}
        },
        "engineering_details": [
            "The default config uses soft training, maximum sequence length 128, batch size 8, two epochs and AdamW with learning rate 2e-5; these are configurations, not proof of optimal hyperparameters.",
            "Mean pooling masks padding before averaging; max pooling masks padding with a large negative value before taking maxima.",
            "Soft-target evaluation reports internal cross-entropy and exp(-KL) similarity, expressly distinct from the official EXIST ICM-Soft measure.",
            "A TF-IDF word-unigram/bigram plus class-balanced logistic-regression baseline is implemented and has a committed development classification report.",
            "An implemented train_task2.py predicts DIRECT/JUDGEMENTAL/REPORTED for labeled Task 2 examples, whereas the README says Task 2 is future work. Task 3 has annotation frequency analysis, but no verified end-to-end training program.",
            "The hard-target branch of src/engine/evaluator.py has an initialization defect: avg_loss and kl_similarity are assigned only under the soft-target branch, so do not claim a verified working hard-mode end-to-end run."
        ],
        "challenges": [
            {"title": "Ambiguous human labels", "problem": "Majority vote hides annotator differences.", "approach": "Compute the vote distribution per post and train against it using KL divergence; retain hard labels for conventional metrics and comparison."},
            {"title": "Multilingual modeling", "problem": "Posts occur in English and Spanish.", "approach": "Use multilingual pretrained encoders and analyze held-out development errors by language."},
            {"title": "Interpretation of success", "problem": "High accuracy on unanimous posts can conceal poor predictions on disputed posts.", "approach": "Commit disagreement-group and vote-pattern analyses and distinguish internal soft metrics from official EXIST scoring."}
        ],
        "security_and_reliability": ["Uses local dataset files and pretrained model-loading paths; no deployment authentication or production serving system is shown.", "Prediction writers normalize class probabilities and preserve explicit class labels; evaluation code and inputs still require a consistent local environment."],
        "testing_and_quality": ["Committed development predictions, baseline classification report, language summaries, disagreement analyses and error files provide audit artifacts.", "Official EXIST evaluation command and official evaluator code are included, but no committed official ICM-Soft score was verified.", "No complete automated pytest/CI suite was identified in the inspected repository."],
        "outcomes": ["The repository demonstrates a working research implementation for soft-label Task 1 training/inference and interpretable subgroup error analysis.", "Saved development analyses show performance degrades as annotator disagreement grows; this is an observed diagnostic, not evidence that soft targets outperform hard targets."],
        "verified_metrics": [
            "Committed TF-IDF + logistic-regression development classification report: accuracy 0.7428, macro F1 0.7368 on 1,038 examples.",
            "Committed ensemble development error summary: 1,038 examples, 212 classification errors (113 false positives; 99 false negatives).",
            "Committed ensemble disagreement summary: full-agreement group n=366, accuracy 0.9098; high-disagreement group n=104, accuracy 0.5096.",
            "Committed language analysis: English n=489, accuracy 0.8139; Spanish n=549, accuracy 0.7796. These are saved dev-analysis figures, not official test-set scores."
        ],
        "limitations": ["No validated claim that soft-label training beats the hard-label alternative on a controlled comparison; saved official EXIST ICM scores were not verified.", "README incorrectly states that Task 2 code is not implemented; train_task2.py exists, but completed Task 2 experiment scores were not verified.", "Task 3 analysis/preprocessing should not be described as a trained five-category classifier.", "There is a hard-label evaluator bug and no evidenced comprehensive automated regression test suite.", "Datasets and saved development predictions do not establish external deployment or population-level fairness."],
        "retrieval_terms": ["disagreement-aware sexism detection", "learning from disagreement", "exist 2023", "task 1 sexism identification", "task 2 source intention", "annotator votes", "annotator disagreement", "subjective labels", "soft labels", "majority vote", "hard labels", "kl divergence", "soft label loss", "multilingual", "english spanish", "xlm roberta", "mbert", "huggingface transformers", "pytorch", "mean pooling", "max pooling", "ensemble averaging", "icm soft", "official exist evaluation", "tfidf logistic regression", "lime", "error analysis", "language comparison", "classification f1"]
    },
    "reinforcement-learning-lab": {
        "title": "Reinforcement Learning Lab",
        "aliases": ["reinforcement-learning-lab", "RL Lab", "reinforcement learning projects", "CNR-ISMN RL experiments"],
        "keywords": ["reinforcement learning", "DQN", "Double DQN", "tabular Q-learning", "IQL", "parameter-shared DQN", "VDN", "QMIX", "PPO components", "CartPole", "MountainCar", "FrozenLake", "CliffWalking", "multi-agent RL", "spintronic synapse", "neuromorphic"],
        "role": "Collection in Saleh's GitHub repository; README identifies CNR-ISMN internship research, but collaborator-specific contributions are not established.",
        "type": "Collection of classical, deep, multi-agent and hardware-inspired RL experiments",
        "overview": "A multi-directory collection rather than one application or one unified training pipeline. It includes CartPole and FrozenLake DQN programs, a MountainCar Double-DQN implementation, CNR-ISMN tabular and neural experiments, multi-agent Meeting Gridworld algorithms, and simulated multi-weight spintronic-synapse learning. A separate related neuromorphic repository is linked by its README; that separate repository should not be silently counted as implemented in this tree.",
        "problem": "Study control and coordination under delayed rewards, sparse feedback, nonstationary multi-agent environments, and hardware-inspired constraints on weight representation/updates.",
        "architecture": "Individual experiment folders generally separate environment wrappers, Q-networks, replay buffers, agents, training scripts and logging/results. DQN variants use epsilon-greedy action selection and Bellman-target updates over sampled replay. The MountainCar Double DQN branch selects next actions with the online network and evaluates them with a synchronized target network. The Meeting Gridworld project contains individual independent agents (IQL), a parameter-sharing DQN, VDN summation of individual Q-values, and QMIX with a state-conditioned mixing hypernetwork constrained to nonnegative mixing weights using softplus. Other directories model effective weights as programmable multi-weight synaptic conductance states and use gradient-sign-based updates. The cooperative-switch-door directory has environment, actor/critic, advantage, rollout-buffer and PPO-loss building blocks; a complete PPO training result is not established by those files alone.",
        "pipeline": [
            {"title": "Configure environments", "description": "Use Gymnasium-style wrappers for CartPole, FrozenLake, MountainCar and CliffWalking, and custom gridworld environments for cooperative agents."},
            {"title": "Collect experience", "description": "Choose exploratory or greedy actions, step environments, and store states/actions/rewards/next states/done indicators in replay buffers."},
            {"title": "Train value-based learners", "description": "Apply sampled Q-learning updates with neural Q-values; MountainCar Double DQN separates action selection and target evaluation. Track reward and loss and save selected checkpoints in individual scripts."},
            {"title": "Compare multi-agent methods", "description": "Train IQL and parameter-shared DQN as decentralized baselines, VDN as additive value factorization and QMIX as state-conditioned monotonic mixing for centralized training with decentralized action selection."},
            {"title": "Explore device-inspired updates", "description": "Represent some Q-values or network weights through simulated conductance/magnetoresistance states; map backpropagated gradient signs to discrete synaptic state adjustments rather than ordinary floating-point optimizer updates."}
        ],
        "stack": {
            "RL and computation": {"technologies": ["Python", "PyTorch", "NumPy", "Gymnasium"], "role": "Value networks, optimizer/training logic, environment interactions and replay buffers."},
            "Experiments": {"technologies": ["Matplotlib", "saved PyTorch checkpoints", "experiment reports", "TensorBoard-related logging in MARL code"], "role": "Training inspection, checkpointing, plotting and report-based comparisons."},
            "Hardware-inspired simulation": {"technologies": ["custom MultiWeightSynapse and conductance/crosspoint classes"], "role": "Software models of programmable synaptic states; no fabrication or physical-chip validation follows from these Python files."}
        },
        "engineering_details": [
            "CartPole classical DQN uses replay, epsilon decay and RMSprop; a target-network variant in that specific agent is commented-out scaffolding, not active.",
            "MountainCar Double DQN uses an online and target Q-network, SmoothL1 loss and a target computed from online argmax plus target-network gather; observation normalization and reward-shaping wrappers are separate modules.",
            "QMIX's mixing network generates state-dependent weights using hypernetworks and applies softplus to preserve monotonicity. VDN instead sums agent Q-values for centralized learning.",
            "The saved Meeting Gridworld report concerns a 5x5, two-agent meeting task with four-dimensional local observations and discusses five seeds with final-100-training-episode statistics, not a held-out evaluation population.",
            "The collection contains both implemented systems and exploratory/partial pieces; its experiment folders should not be merged into one deployed architecture."
        ],
        "challenges": [
            {"title": "Sparse and delayed control feedback", "problem": "Classical control and navigation tasks can learn slowly from sparse or delayed rewards.", "approach": "Use replay, epsilon-greedy exploration, target networks in applicable variants and environment-specific reward/observation wrappers."},
            {"title": "Multi-agent coordination", "problem": "Independently learning agents create nonstationarity, while shared networks may underfit distinct coordination roles.", "approach": "Compare IQL and parameter sharing with VDN and QMIX's centralized value decomposition under limited observations."},
            {"title": "Physical update restrictions", "problem": "Conventional floating-point updates do not model limited device conductance states.", "approach": "Implement simulated multi-weight synapses/crosspoints and map gradient signs to device-state changes; physical hardware outcomes are not established."}
        ],
        "security_and_reliability": ["Research scripts operate on local simulated environments and checkpoints; no user-facing hosted service, access-control boundary or production security system is evidenced."],
        "testing_and_quality": ["Selected MARL folders contain environment/algorithm tests, and several folders include saved checkpoint and plot artifacts.", "Multi-agent reports document configurations, per-seed comparisons and important variance caveats; they are not standardized external benchmarks.", "The repository has no evidenced unified end-to-end CI/regression suite covering every experiment."],
        "outcomes": ["The codebase demonstrates breadth across tabular Q-learning, DQN, Double DQN, multi-agent value decomposition and neuromorphic simulation.", "In the documented partial-observation meeting experiment, QMIX achieved the highest reported mean success rate but with very high seed-to-seed variability; IQL was more stable than QMIX in that comparison."],
        "verified_metrics": ["Saved 4D Meeting Gridworld experiment report, five seeds, final 100 training episodes per seed: QMIX success 54.00% ± 39.92% standard deviation; IQL 40.00% ± 10.88%; parameter-shared DQN 3.80% ± 1.60%. These are within-training report figures, not independently held-out results."],
        "limitations": ["No single algorithm, quality score or uniform stack applies to all folders; some PPO-related code is only algorithm components.", "Research reports cannot prove physical spintronic hardware performance or generalization outside the stated environments.", "The comparison report covers three algorithms and one observation setting; the presence of VDN code does not establish an equally documented VDN benchmark in that report.", "README claims of solved/max-reward CartPole behavior are not turned into numerical metrics without a corresponding specific saved evaluation artifact."],
        "retrieval_terms": ["reinforcement learning lab", "rl lab", "dqn", "deep q network", "double dqn", "experience replay", "epsilon greedy", "bellman equation", "target network", "q learning", "tabular rl", "frozen lake", "frozenlake", "cartpole", "mountaincar", "cliff walking", "multi agent", "marl", "iql", "independent q learning", "parameter sharing", "ps dqn", "vdn", "value decomposition", "qmix", "mixing network", "hypernetwork", "ctde", "ppo", "meeting gridworld", "cooperative coordination", "neuromorphic", "spintronic", "multi weight synapse", "memristive", "conductance", "sign based updates", "cnr ismn", "pytorch", "gymnasium"]
    },
    "time-series-forecasting": {
        "title": "Time-Series Forecasting",
        "aliases": ["Campus Load Forecasting", "Savona Campus Load Forecasting", "Electrical Load Forecasting", "Forecasting Project", "time-series-forecasting", "electrical load prediction"],
        "keywords": ["campus load", "time series", "electricity demand", "Savona", "15-minute resampling", "lag features", "rolling statistics", "LightGBM", "XGBoost", "Random Forest", "previous-week baseline", "MAE", "RMSE", "MAPE", "temporal leakage"],
        "role": "The repository contains an authored forecasting notebook and README; specific contributions by any collaborators are not independently established.",
        "type": "Notebook-based electrical-load preprocessing, feature engineering and regression-model comparison",
        "overview": "The committed electrical_load_forecasting.ipynb builds and evaluates a short-term campus electrical-load predictor using minute-resolution Savona Campus readings. It handles inconsistent timestamps, sensor-quality problems and missing intervals, aggregates to 15-minute average loads and engineers calendar, lag and rolling predictors. The notebook compares a previous-week persistence baseline with Random Forest, XGBoost and LightGBM on a chronological holdout. Saved notebook evaluation outputs provide traceable MAE, RMSE and MAPE; LightGBM has the lowest reported errors. The README gives a different baseline description and numbers, so the current notebook is authoritative for those details.",
        "problem": "The original load readings include mixed timestamp formats, negative values, duplicated timestamps, short gaps and outages spanning multiple days. The modeling task is to forecast a 15-minute load value using only known time and prior-load characteristics, while avoiding the obvious leakage from random splitting or unshifted target-derived windows.",
        "architecture": "A single Google-Colab-style Python notebook performs Pandas and NumPy preprocessing, Matplotlib/Seaborn exploratory plots, chronological 80/20 splitting, scikit-learn RandomForestRegressor and metrics, XGBRegressor, and LightGBM LGBMRegressor training/evaluation. Data is read from an external source referenced in the notebook; the source CSV is not committed. There is no separate API, database, serving layer, CI or scheduled retraining code in the repository.",
        "pipeline": [
            {"title": "Normalize measurements", "description": "Read load/timestamp columns; use pandas to_datetime(format='mixed', errors='coerce'), floor timestamps to minute precision, replace negative readings with NaN, linearly interpolate initial missing values and deduplicate timestamps keeping the first value."},
            {"title": "Treat missing time intervals", "description": "Build a complete minute index; interpolate short gaps with time-based interpolation limited to 60 missing entries in either direction, forward-fill eligible night-time gaps from 23:00 to 06:59 with an upper bound of 480 entries, and remove remaining missing load measurements."},
            {"title": "Aggregate and engineer features", "description": "Resample cleaned observations to 15-minute averages, drop empty buckets, create hour/minute/day/month/year/weekend columns, use 1/4/96/672-row load lags and shifted rolling means for 4, 96 and 672 rows plus shifted rolling standard deviation over 96 rows; drop rows with unavailable feature history."},
            {"title": "Chronological train/test holdout", "description": "Take the first 80% of retained feature rows (149,968) as training and the final 20% (37,492) as testing; fit regressors only to the training portion. The notebook prints the associated train and test periods."},
            {"title": "Compare regression errors", "description": "Compute prior-week lag_672 persistence predictions and predictions from Random Forest, XGBoost and LightGBM; measure each with mean absolute error, root mean squared error and mean absolute percentage error; plot predictions and LightGBM feature importance."}
        ],
        "stack": {
            "Preprocessing and analysis": {"technologies": ["Python", "Pandas", "NumPy", "Matplotlib", "Seaborn", "Jupyter/Google Colab"], "role": "Datetime normalization, gap filling, 15-minute aggregation, feature generation and plots."},
            "Forecasting": {"technologies": ["scikit-learn RandomForestRegressor", "XGBoost XGBRegressor", "LightGBM LGBMRegressor", "scikit-learn regression metrics"], "role": "Chronological split, regressor training, feature importance and saved error calculations."}
        },
        "engineering_details": [
            "Features are explicit rather than learned automatically from raw waveforms: calendar indicators plus load at shift(1), shift(4), shift(96) and shift(672), and rolling summaries created after shift(1). This avoids including the same-row target directly in lag/rolling columns.",
            "The train/test split preserves time order, unlike a random split that would contaminate the forecast evaluation with later observations.",
            "The selected Random Forest uses n_estimators=100 and random_state=42; XGBoost uses 500 estimators, learning_rate=0.05 and max_depth=6; LightGBM uses 500 estimators, learning_rate=0.05 and num_leaves=31. These are configurations in the executed notebook, not a documented hyperparameter-search result.",
            "The baseline is the previous WEEK in the notebook: lag_672 on nominal 15-minute rows. The README instead describes a previous-DAY baseline and reports different baseline metrics. Current implementation and saved output take precedence.",
            "Short-gap interpolation with limit_direction='both' is applied to the whole series before the split and may use a later observed reading to fill an earlier one. Thus the chronological split and shifted rolling features reduce leakage risk but do not prove full leakage-free evaluation.",
            "Missing 15-minute buckets are dropped before row-based shifts; near outages, shift(96) and shift(672) refer to previous retained rows rather than necessarily exactly 24 hours or seven calendar days earlier.",
            "LightGBM's saved feature-importance table ranks lag_1 and hour highly in that fitted model; feature importance is model-specific and not a causal effect estimate."
        ],
        "challenges": [
            {"title": "Irregular sensor observations", "problem": "Inconsistent precision, duplicates and missing spans create misleading temporal alignment and empty resampling intervals.", "approach": "Align timestamps to a minute index, perform bounded gap handling, drop extended missing regions and average retained values into 15-minute buckets; explicitly identify the risk that subsequent row-wise lags cross removed intervals."},
            {"title": "Temporal leakage", "problem": "Using future target values or random train/test assignment would overstate short-term forecast skill.", "approach": "Use shifted lag and rolling features plus chronological 80/20 evaluation. A remaining caveat is bidirectional pre-split interpolation, so full boundary-level leakage prevention is not established."},
            {"title": "Baseline and nonlinear-model comparison", "problem": "Accuracy must be compared with a simple history-based forecast rather than only between complex regressors.", "approach": "Use notebook's prior-week lag persistence as a reference and compare test MAE/RMSE/MAPE with Random Forest, XGBoost and LightGBM."}
        ],
        "testing_and_quality": ["The committed notebook includes executable cells and saved outputs for data dimensions, cleanup, feature tables, chronological split, fitted models, regression metrics and feature importance.", "No automated test suite, artifact-pinned dataset, walk-forward backtesting or independent reproduction of notebook outputs is committed."],
        "outcomes": ["LightGBM yielded the lowest recorded test MAE, RMSE and MAPE among the four notebook comparisons.", "The notebook saved 149,968 training and 37,492 test feature rows after cleaning and lag-window trimming. The results are retrospective on one chronological holdout, not deployment performance."],
        "verified_metrics": [
            "Executed notebook cell 8: original data shape 2,809,602 rows by 2 columns; after resampling and removing absent buckets, 188,132 15-minute load observations; final feature set has 187,460 rows.",
            "Executed notebook cell 67: chronological train 149,968 rows (2018-01-07 23:00 to 2022-08-11 19:15), test 37,492 rows (2022-08-11 19:30 to 2023-09-07 08:30).",
            "Previous-WEEK lag-672 baseline, saved cell 69: test MAE 21.18893, RMSE 34.34983, MAPE 20.76339%.",
            "Random Forest, saved cell 74: test MAE 5.20838, RMSE 7.91114, MAPE 5.14100%.",
            "XGBoost, saved cell 79: test MAE 5.09716, RMSE 7.74676, MAPE 4.98796%.",
            "LightGBM, saved cell 84: test MAE 5.06961, RMSE 7.69915, MAPE 4.97133%."
        ],
        "limitations": ["The repository does not commit the raw sensor CSV; the notebook loads externally sourced data, so independent reproduction needs access to that dataset.", "Pre-split bidirectional interpolation can incorporate later information, so avoid claiming complete leakage prevention or production-realistic live forecasting.", "Row-based lags are not guaranteed to preserve elapsed-time offsets after gaps have been dropped.", "README's previous-day baseline and its numerical results conflict with the executed notebook's previous-week baseline; prefer notebook figures.", "No model-serving endpoint, deployment, drift monitoring, retraining loop or benchmark across multiple forward test periods is evidenced."],
        "retrieval_terms": ["time series forecasting", "electrical load forecasting", "savona campus", "campus power demand", "electricity demand", "energy forecast", "forecast accuracy", "data_timestamp", "negative load", "mixed timestamps", "missing timestamps", "60 minute interpolation", "night gap filling", "15 minute resampling", "lag 1", "lag 4", "lag 96", "lag 672", "previous week baseline", "previous day baseline readme discrepancy", "rolling mean", "rolling standard deviation", "shift 1", "chronological train test", "temporal leakage", "future leakage", "walk forward", "random forest regressor", "xgboost", "lightgbm", "mae", "rmse", "mape", "forecast metrics", "lag feature importance"]
    },
    "news-popularity-prediction": {
        "title": "News Popularity Prediction",
        "aliases": ["Online News Popularity Prediction", "Online News Popularity (Big Data)", "news-popularity-prediction", "Big Data Analytics news classifier"],
        "keywords": ["online news popularity", "PySpark", "Spark MLlib", "classification", "Random Forest", "Gradient Boosted Trees", "Linear SVC", "Logistic Regression", "Decision Tree", "Naive Bayes", "ROC AUC", "cross-validation"],
        "role": "The two committed notebooks identify Saleh as their author; presented as academic coursework in Big Data Analytics and Text Mining.",
        "year": "2025–2026 (academic year stated in notebook headings)",
        "type": "Academic big-data binary classification comparison with saved Spark notebook outputs",
        "overview": "Uses the UCI Online News Popularity dataset to classify an article as popular if its number of shares exceeds 1,400. Two committed PySpark notebooks contain the training/evaluation workflow and executed output cells. The main notebook compares Random Forest, Gradient-Boosted Trees and Linear SVC; the course-project-work notebook compares Logistic Regression, Decision Tree and Naive Bayes. The repository includes the local CSV and a Docker Compose file, but does not establish a deployed prediction API or live decision-support product.",
        "problem": "Use available tabular article features to predict a binary popularity threshold and compare interpretable/classical and ensemble classification methods under a consistent train/test workflow.",
        "architecture": "Notebook-centered SparkSession with local[*] execution, Spark SQL/DataFrames and Spark ML estimators/evaluators. Each notebook loads the supplied CSV, trims column-name whitespace, builds label = shares > 1400, drops url and shares, applies seed-42 randomSplit([0.7, 0.3]), assembles numerical features and fits scalers on the training split. Main experiments train RF, GBT and linear SVM; course-work experiments train logistic regression, decision trees and Naive Bayes. Spark CrossValidator with three folds tunes estimator hyperparameters on training data, then the selected models are evaluated on the held-out random test portion. Notebook outputs include classification metrics, ROC comparisons and feature importances.",
        "pipeline": [
            {"title": "Load and label", "description": "Read the committed OnlineNewsPopularity.csv with PySpark; define positive class as shares > 1400, then drop shares to avoid directly leaking the target and drop article URL as an identifier."},
            {"title": "Random holdout", "description": "Split 70% train and 30% test with Spark randomSplit seed 42; saved output shows 27,961 training and 11,683 test rows."},
            {"title": "Vectorize and scale", "description": "VectorAssembler produces features; StandardScaler is fit on training rows and applied to both splits. The Naive Bayes path separately uses a training-fitted MinMaxScaler for nonnegative inputs."},
            {"title": "Fit and tune", "description": "Train the two notebooks' six named classifiers and tune selected hyperparameters using three-fold Spark CrossValidator on training rows, using ROC-AUC or Spark F1 as appropriate."},
            {"title": "Evaluate and interpret", "description": "Print random-holdout ROC-AUC where supported, accuracy, Spark weighted F1, and positive-class precision/recall; plot ROC/metric comparisons and inspect tree feature importances or logistic regression coefficients."}
        ],
        "stack": {"Big-data processing": {"technologies": ["Apache Spark", "PySpark", "Spark SQL", "Spark MLlib"], "role": "Tabular loading, split, vectors, transformations, training, cross-validation and metrics."}, "Analysis": {"technologies": ["Python", "Jupyter notebooks", "Pandas", "Matplotlib", "scikit-learn utilities"], "role": "Exploratory summaries, visual comparison and postprocessing of notebook evaluation results."}, "Environment": {"technologies": ["Docker Compose"], "role": "Committed local environment definition, not evidence of production deployment."}},
        "engineering_details": [
            "Both notebook paths remove shares before training; this avoids using the label-defining variable as an explicit predictor.",
            "Both retain the dataset's timedelta feature, visible in trained feature-importance output. Because timedelta describes elapsed time since publication, the notebooks do not fully establish that every feature is known before publication; the before-publication claim should be qualified.",
            "Scaling is fit only on the overall training split, preventing direct test-set contamination, but the scaler is fitted before inner CV folds, so strict fold-isolated preprocessing is not implemented by a Spark Pipeline inside CrossValidator.",
            "Random row splitting is not a chronological or publisher/time-grouped validation design; results should not be presented as prospective production generalization.",
            "Spark MulticlassClassificationEvaluator(metricName='f1') is weighted F1, not specifically the positive-class F1; precisionByLabel and recallByLabel are explicitly computed for label 1.",
            "The notebooks deliberately report no probability ROC-AUC for LinearSVC; do not invent one."
        ],
        "challenges": [{"title": "Target leakage", "problem": "Article share count directly determines the class.", "approach": "Explicitly drop shares from model inputs and fit train/test scalers on the training split only; residual feature-timing and nested-CV caveats remain."}, {"title": "Model selection at scale", "problem": "Different classifiers have different scaling constraints, model complexity and ROC support.", "approach": "Use separate scaling for Naive Bayes, compare six Spark classifiers across two notebooks and tune through three-fold CV."}],
        "testing_and_quality": ["Both notebooks have committed execution outputs showing dataset counts, model scores and tuned comparisons.", "Feature-importance/ROC exploration is saved; no stand-alone automated test suite or temporal backtest is evidenced."],
        "outcomes": ["On the saved main-notebook random holdout, tuned GBT is the highest-AUC model among its three compared classifiers.", "The project shows academic feature engineering and Spark model comparison, not an operational real-time popularity forecasting service."],
        "verified_metrics": [
            "Main notebook output: 39,644 rows and 61 original columns; training 27,961, test 11,683 after seed-42 70/30 random split.",
            "Main notebook tuned Gradient-Boosted Trees test ROC-AUC 0.72543, accuracy 0.66866, Spark weighted F1 0.66860.",
            "Main notebook tuned Random Forest test ROC-AUC 0.69887, accuracy 0.64290, Spark weighted F1 0.64288.",
            "Main notebook tuned Linear SVC test accuracy 0.63246, Spark weighted F1 0.63236; notebook does not report ROC-AUC.",
            "Course-work notebook tuned Logistic Regression test ROC-AUC 0.70067, accuracy 0.64975, Spark weighted F1 0.64950.",
            "Course-work notebook tuned Decision Tree test ROC-AUC 0.57653, accuracy 0.63169, Spark weighted F1 0.63167.",
            "Course-work notebook tuned Naive Bayes test ROC-AUC 0.65917, accuracy 0.61628, Spark weighted F1 0.61627."
        ],
        "limitations": ["The findings are based on a seeded random test split, not a time-forward or out-of-domain test.", "The retained timedelta feature raises a before-publication information-availability concern, despite dropping shares.", "Preprocessing is fitted before cross-validation rather than within fold-specific pipelines; the main held-out test remains separate.", "No deployed prediction service, monitoring, calibration, model registry or benchmark against recent external data is demonstrated."],
        "retrieval_terms": ["news popularity prediction", "online news", "article shares", "popular vs unpopular", "1400 shares", "uci online news popularity", "big data analytics", "pyspark", "spark mllib", "spark sql", "vectorassembler", "standardscaler", "minmaxscaler", "randomsplit", "crossvalidator", "three fold", "random forest", "gradient boosted trees", "gbt", "linear svc", "support vector", "logistic regression", "decision tree", "naive bayes", "roc auc", "weighted f1", "precision recall", "feature importance", "timedelta leakage", "classification"]
    }
}
