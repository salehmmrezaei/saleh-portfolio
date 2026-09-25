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
        models.Project(name="RepoPilot AI", description="Production-oriented codebase intelligence platform."),
        models.Project(name="Voice Notes AI", description="Local-first AI application for audio transcription.")
    ]
    db.add_all(projects)
    db.commit()
    return {"message": "Database seeded successfully!"}