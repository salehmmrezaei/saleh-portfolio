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
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Add this Pydantic model so FastAPI knows how to structure the JSON
class ProjectSchema(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True

@app.get("/")
def read_root():
    return {"message": "Backend is running!"}

# 2. Tell the endpoint to use the schema (response_model=List[ProjectSchema])
@app.get("/api/projects", response_model=List[ProjectSchema])
def get_projects(db: Session = Depends(get_db)):
    return db.query(models.Project).all()

@app.post("/api/seed")
def seed_database(db: Session = Depends(get_db)):
    if db.query(models.Project).first():
        return {"message": "Database already seeded!"}
    
    projects = [
        models.Project(name="RepoPilot AI",
                       skills=["Python", "FastAPI", "PostgreSQL", "Redis", "Celery", "Docker"],
                       url="https://github.com/salehmmrezaei/repilot-ai",
                       description=["Built a production-oriented codebase intelligence platform for repository ingestion, versioned source indexing, hybrid retrieval, and grounded codebase Q&A.", "Designed asynchronous processing with Redis/Celery and implemented reproducible retrieval evaluation using Recall@K and MRR."]),
        models.Project(name="Voice Notes AI",
                       skills=["Python", "FastAPI", "PostgreSQL", "Redis", "Celery", "Docker"],
                       url="https://github.com/salehmmrezaei/voice-notes-ai",
                       description=["Built an end-to-end AI application combining audio ingestion, Faster-Whisper transcription, and local LLM-powered text processing.", "Developed a FastAPI backend and React/TypeScript frontend with validation, error handling, automated tests, CI, and Dockerized deployment."]),

    ]
    db.add_all(projects)
    db.commit()
    return {"message": "Database seeded successfully!"}