from datetime import date

from .database import SessionLocal
from .models import Education, Experience, Project, Skill


def seed() -> None:
    with SessionLocal.begin() as db:
        project_data = [
            {
                "name": "RepoPilot AI",
                "skills": ["Python", "FastAPI", "PostgreSQL/pgvector", "Redis/Celery"],
                "url": "https://github.com/salehmmrezaei/repopilot-ai",
                "description": [
                    "Production-oriented repository intelligence platform for source indexing, hybrid retrieval, and grounded codebase Q&A.",
                    "Built versioned repository indexing with keyword, symbol, and semantic retrieval.",
                    "Implemented grounded AI answers with validated source references, durable background processing, testing, and CI.",
                ],
            },
            {
                "name": "Voice Notes AI",
                "skills": ["Faster-Whisper", "Ollama", "FastAPI", "React"],
                "url": "https://github.com/salehmmrezaei/voice-notes-ai",
                "description": [
                    "Local-first AI application for recording, transcribing, and improving voice notes with speech recognition and local LLMs.",
                    "Built browser recording and audio-upload workflows with local Faster-Whisper transcription and Ollama-powered text cleanup.",
                    "Developed the full-stack application with Docker, validation, structured error handling, automated tests, and GitHub Actions CI.",
                ],
            },
            {
                "name": "Learning from Disagreement for Multilingual Sexism Detection",
                "skills": ["PyTorch", "Transformers", "XLM-RoBERTa", "NLP"],
                "url": "https://github.com/salehmmrezaei/disagreement-aware-sexism-detection",
                "description": [
                    "Transformer-based multilingual NLP system that learns from annotator disagreement using soft labels instead of only majority-vote labels.",
                    "Trained English and Spanish sexism classifiers using hard-label and soft-label learning with KL-divergence loss.",
                    "Built evaluation and ensemble pipelines using multilingual transformer models and official EXIST 2023 evaluation formats.",
                ],
            },
            {
                "name": "Reinforcement Learning Lab",
                "skills": ["PyTorch", "DQN", "Multi-Agent RL", "Gymnasium"],
                "url": "https://github.com/salehmmrezaei/reinforcement-learning-lab",
                "description": [
                    "Collection of reinforcement-learning experiments spanning classical, deep, multi-agent, and neuromorphic approaches.",
                    "Implemented Q-learning, DQN, Double DQN, and multi-agent reinforcement-learning experiments across several control environments.",
                    "Explored hardware-inspired and neuromorphic learning using multi-weight spintronic synapse models.",
                ],
            },
            {
                "name": "Campus Load Forecasting",
                "skills": ["LightGBM", "XGBoost", "Time Series", "Feature Engineering"],
                "url": "https://github.com/salehmmrezaei/time-series-forecasting",
                "description": [
                    "End-to-end machine-learning pipeline for forecasting campus electricity demand from large-scale historical time-series data.",
                    "Cleaned and transformed multi-year, minute-level load data using time-aware preprocessing, lag features, and rolling statistics.",
                    "Compared baseline, Random Forest, XGBoost, and LightGBM models, with LightGBM achieving approximately 4.97% MAPE.",
                ],
            },
            {
                "name": "Online News Popularity Prediction",
                "skills": ["PySpark", "Spark MLlib", "Machine Learning", "Big Data"],
                "url": "https://github.com/salehmmrezaei/news-popularity-prediction",
                "description": [
                    "Big-data classification project for predicting whether online news articles will exceed a target popularity threshold.",
                    "Built a PySpark pipeline covering preprocessing, exploratory analysis, feature engineering, model training, and evaluation.",
                    "Compared Gradient-Boosted Trees, Random Forest, Linear SVM, Logistic Regression, Naive Bayes, and Decision Trees.",
                ],
            },
        ]
        existing_projects = {
            project.url: project for project in db.query(Project).all()
        }
        project_urls = {project_values["url"] for project_values in project_data}
        for project in db.query(Project).all():
            if project.url not in project_urls:
                db.delete(project)
        for project_values in project_data:
            project = existing_projects.get(project_values["url"])
            if project is None:
                db.add(Project(**project_values))
            else:
                for field, value in project_values.items():
                    setattr(project, field, value)

        experience_data = [
            {
                "company": "Zutre",
                "company_slug": "zutre",
                "role": "R&D AI Engineer",
                "start_date": date(2025, 12, 1),
                "end_date": date(2026, 6, 30),
                "skills": ["Python", "RAG", "Vector Databases"],
                "url": "https://zutre.com",
                "description": [
                    "Built end-to-end RAG pipelines covering ingestion, chunking, embeddings, vector indexing, semantic retrieval, context assembly, and LLM generation.",
                    "Evaluated LLMs, embedding models, vector databases, and retrieval strategies to improve quality and support production-oriented component selection.",
                ],
            },
            {
                "company": "CNR (ISMN)",
                "company_slug": "cnr",
                "role": "AI Engineer",
                "start_date": date(2025, 11, 1),
                "end_date": date(2026, 8, 31),
                "skills": ["Python", "LangChain", "AI Agents"],
                "url": "https://www.cnr.it/",
                "description": [
                    "Designed and deployed LLM-powered pipelines for extracting structured information from scientific and technical documents.",
                    "Built agentic workflows combining document processing, prompt orchestration, structured outputs, validation, and automated downstream processing.",
                ],
            },
            {
                "company": "Denxa",
                "company_slug": "denxa",
                "role": "Software Engineer",
                "start_date": date(2022, 12, 1),
                "end_date": date(2023, 5, 31),
                "skills": ["Python", "REST APIs", "Docker"],
                "url": "https://www.denxa.ca",
                "description": [
                    "Developed Python backend services and REST APIs for data-intensive applications, integrating data-processing and machine-learning components.",
                    "Built containerized services with Docker and implemented testing, validation, logging, and error handling for reliable application behavior.",
                ],
            },
            {
                "company": "Sulfate Shargh Co.",
                "company_slug": "sulfate-shargh",
                "role": "Software Engineer Intern",
                "start_date": date(2022, 1, 1),
                "end_date": date(2022, 12, 31),
                "skills": ["Python", "Machine Learning", "Data Processing"],
                "url": "https://zincsulfate.co",
                "description": [
                    "Supported machine-learning experiments for workflow optimization through data preprocessing, model evaluation, and performance comparison.",
                    "Documented experiment results and assisted with improving data and model workflows.",
                ],
            },
        ]
        for experience_values in experience_data:
            experience = db.query(Experience).filter_by(
                company_slug=experience_values["company_slug"],
            ).one_or_none()
            if experience is None:
                db.add(Experience(**experience_values))
            else:
                for field, value in experience_values.items():
                    setattr(experience, field, value)

        db.add_all([
            Education(
                institution="University of Bologna",
                degree="M.Sc. Artificial Intelligence",
                grade="105/110",
                start_date=date(2024, 9, 1),
                end_date=date(2026, 7, 17),
                country="Italy",
            ),
            Education(
                institution="University of Zanjan",
                degree="B.Sc. Computer Engineering",
                grade="16.92/20",
                start_date=date(2017, 9, 1),
                end_date=date(2022, 5, 22),
                country="Iran",
            ),
        ])

        db.add_all([
            Skill(
                title="LLM & Generative AI",
                skills=["RAG", "LangChain", "AI Agents", "Prompt Engineering", "LLM Evaluation", "Vector Databases"],
                description="Building retrieval, agentic, and evaluation pipelines for production AI.",
                featured=True,
            ),
            Skill(
                title="Backend & Production",
                skills=["Python", "FastAPI", "REST APIs", "Docker", "Redis", "Celery", "PostgreSQL", "AWS"],
                description="APIs, asynchronous workloads, containerized services, and scalable infrastructure.",
            ),
            Skill(
                title="Machine Learning & Data",
                skills=["PyTorch", "Scikit-learn", "Pandas", "NumPy", "SQL", "ETL"],
                description="Experimentation, evaluation, data processing, and model-driven applications.",
            ),
            Skill(
                title="Full-Stack & Workflow",
                skills=["React", "TypeScript", "Git", "CI"],
                description="Enough frontend and engineering tooling to ship complete AI products.",
            ),
        ])

    print("Portfolio data seeded successfully.")


if __name__ == "__main__":
    seed()
