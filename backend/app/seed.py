from datetime import date

from .database import SessionLocal
from .models import Education, Experience, Project, Skill


def seed() -> None:
    with SessionLocal.begin() as db:
        if db.query(Project).first():
            print("Database already contains portfolio data.")
            return

        db.add_all([
            Project(
                name="RepoPilot AI",
                skills=["Python", "FastAPI", "PostgreSQL", "Redis", "Celery", "Docker"],
                url="https://github.com/salehmmrezaei/repopilot-ai",
                description=[
                    "Built a production-oriented codebase intelligence platform for repository ingestion, versioned source indexing, hybrid retrieval, and grounded codebase Q&A.",
                    "Designed asynchronous processing with Redis/Celery and implemented reproducible retrieval evaluation using Recall@K and MRR.",
                ],
            ),
            Project(
                name="Voice Notes AI",
                skills=["Python", "FastAPI", "PostgreSQL", "Redis", "Celery", "Docker"],
                url="https://github.com/salehmmrezaei/voice-notes-ai",
                description=[
                    "Built an end-to-end AI application combining audio ingestion, Faster-Whisper transcription, and local LLM-powered text processing.",
                    "Developed a FastAPI backend and React/TypeScript frontend with validation, error handling, automated tests, CI, and Dockerized deployment.",
                ],
            ),
        ])

        db.add_all([
            Experience(
                company="CNR (ISMN)",
                company_slug="cnr",
                role="AI Engineer",
                start_date=date(2025, 11, 1),
                end_date=date(2026, 8, 31),
                skills=["Python", "Machine Learning", "Data Analysis"],
                url="https://www.cnr.it/",
                description=[
                    "Designed and deployed LLM-powered pipelines for extracting structured information from scientific and technical documents using Python, LangChain, and NLP techniques.",
                    "Built and maintained containerized services with Docker, implementing testing, validation, logging, and error handling for reliable application behavior.",
                ],
            ),
            Experience(
                company="Zutre",
                company_slug="zutre",
                role="R&D AI Engineer",
                start_date=date(2025, 12, 1),
                end_date=date(2026, 6, 30),
                skills=["Python", "Deep Learning", "Computer Vision"],
                url="https://zutre.com",
                description=[
                    "Built end-to-end RAG pipelines covering ingestion, chunking, embeddings, vector indexing, retrieval, context assembly, and generation.",
                    "Evaluated LLMs, embedding models, vector databases, chunking strategies, and retrieval configurations using systematic experiments.",
                ],
            ),
            Experience(
                company="Denxa",
                company_slug="denxa",
                role="Software Engineer",
                start_date=date(2022, 12, 1),
                end_date=date(2023, 5, 31),
                skills=["Python", "Web Development", "Database Design"],
                url="https://www.denxa.ca",
                description=[
                    "Developed Python backend services and REST APIs for data-intensive applications.",
                    "Integrated data-processing and machine-learning components into application workflows.",
                ],
            ),
            Experience(
                company="Sulfate Shargh Co",
                company_slug="sulfate-shargh",
                role="Software Engineer Intern",
                start_date=date(2022, 1, 1),
                end_date=date(2022, 12, 31),
                skills=["Python", "Web Development", "Database Design"],
                url="https://zincsulfate.co",
                description=[
                    "Developed Python backend services and REST APIs for data-intensive applications.",
                    "Supported machine-learning experiments for workflow optimization.",
                ],
            ),
        ])

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
