from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from . import models, database
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Add this Pydantic model so FastAPI knows how to structure the JSON
class ProjectSchema(BaseModel):
    id: int
    name: str
    skills: List[str]
    url: str
    description: List[str]

    class Config:
        from_attributes = True

class ExperienceSchema(BaseModel):
    id: int
    company: str
    role: str
    start_date: str
    end_date: str
    skills: List[str]
    url: str
    description: List[str]

    class Config:
        from_attributes = True

class EducationSchema(BaseModel):
    id: int
    institution: str
    degree: str
    grade: str
    start_date: str
    end_date: str
    country: str

    class Config:
        from_attributes = True

@app.get("/")
def read_root():
    return {"message": "Backend is running!"}

# Get all projects
@app.get("/api/projects", response_model=List[ProjectSchema])
def get_projects(db: Session = Depends(get_db)):
    return db.query(models.Project).all()

# Get all education records
@app.get("/api/educations", response_model=List[EducationSchema])
def get_educations(db: Session = Depends(get_db)):
    return db.query(models.Education).all()

# Get all experiences
@app.get("/api/experiences", response_model=List[ExperienceSchema])
def get_experiences(db: Session = Depends(get_db)):
    return db.query(models.Experience).all()

# Seed the database with initial data
@app.post("/api/seed")
def seed_database(db: Session = Depends(get_db)):
    if db.query(models.Project).first():
        return {"message": "Database already seeded!"}
    
    projects = [
        models.Project(
            name="RepoPilot AI",
            skills=["Python", "FastAPI", "PostgreSQL", "Redis", "Celery", "Docker"],
            url="https://github.com/salehmmrezaei/repopilot-ai",
            description=[
                "Built a production-oriented codebase intelligence platform for repository ingestion, versioned source indexing, hybrid retrieval, and grounded codebase Q&A.",
                "Designed asynchronous processing with Redis/Celery and implemented reproducible retrieval evaluation using Recall@K and MRR."
                ]),
        models.Project(
            name="Voice Notes AI",
            skills=["Python", "FastAPI", "PostgreSQL", "Redis", "Celery", "Docker"],
            url="https://github.com/salehmmrezaei/voice-notes-ai",
            description=[
                "Built an end-to-end AI application combining audio ingestion, Faster-Whisper transcription, and local LLM-powered text processing.",
                "Developed a FastAPI backend and React/TypeScript frontend with validation, error handling, automated tests, CI, and Dockerized deployment."
                ]),

    ]
    db.add_all(projects)
    db.commit()

    experiences = [
        models.Experience(
            company="CNR (ISMN)",
            role="AI Engineer",
            start_date="2025-11-01",
            end_date="2026-08-31",
            skills=["Python", "Machine Learning", "Data Analysis"],
            url="https://www.cnr.it/",
            description=[
                "Designed and deployed LLM-powered pipelines for extracting structured information from scientific and technical documents using Python, LangChain, and NLP techniques.",
                "Built and maintained containerized services with Docker, implementing testing, validation, logging, and error handling for reliable application behavior.",
                "Developed and evaluated prompting and information-extraction strategies to improve accuracy, consistency, and reliability across complex scientific documents."
                ]),
        models.Experience(
            company="Zutre",
            role="R&D AI Engineer",
            start_date="2025-12-01",
            end_date="2026-06-30",
            skills=["Python", "Deep Learning", "Computer Vision"],
            url="https://zutre.com",
            description=[
                "Built end-to-end RAG pipelines covering document ingestion, chunking, embeddings, vector database indexing, semantic retrieval, context assembly, and LLM generation.",
                "Evaluated LLMs, embedding models, vector databases, chunking strategies, and retrieval configurations using systematic experiments and retrieval-quality metrics.",
                "Improved RAG quality through retrieval and prompt optimization, comparing candidate architectures to support production-oriented model and component selection."
                ]),
        models.Experience(
            company="Denxa",
            role="Software Engineer",
            start_date="2022-12-01",
            end_date="2023-05-31",
            skills=["Python", "Web Development", "Database Design"],
            url="https://www.denxa.ca",
            description=[
                "Developed Python backend services and REST APIs for data-intensive applications, integrating data-processing and machine-learning components into application workflows.",
                "Evaluated LLMs, embedding models, vector databases, chunking strategies, and retrieval configurations using systematic experiments and retrieval-quality metrics.",
                "Improved RAG quality through retrieval and prompt optimization, comparing candidate architectures to support production-oriented model and component selection."
                ]),
        models.Experience(
            company="Sulfate Shargh Co",
            role="Software Engineer Intern",
            start_date="2022-01-01",
            end_date="2022-12-31",
            skills=["Python", "Web Development", "Database Design"],
            url="https://zincsulfate.co",
            description=[
                "Developed Python backend services and REST APIs for data-intensive applications, integrating data-processing and machine-learning components into application workflows.",
                "Supported machine-learning experiments for workflow optimization, including data preprocessing, model evaluation, performance comparison, and documentation of results."
                ])
    ]
    db.add_all(experiences)
    db.commit()

    educations = [
        models.Education(
            institution="University of Bologna",
            degree="M.Sc. Artificial Intelligence",
            grade="105/110",
            start_date="2024-09-01",
            end_date="2026-07-17",
            country="Italy"
        ),
        models.Education(
            institution="University of Zanjan",
            degree="B.Sc. Computer Engineering",
            grade="16.92/20",
            start_date="2017-09-01",
            end_date="2022-05-22",
            country="Iran"
        )
    ]

    db.add_all(educations)
    db.commit()

    return {"message": "Database seeded successfully!"}