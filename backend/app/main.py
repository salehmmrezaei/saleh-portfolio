from .services.turnstile import verify_turnstile_token
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .middleware.request_size import RequestSizeLimitMiddleware
from .services.rate_limit import enforce_contact_rate_limit
from . import models
from .config import get_allowed_origins
from .database import check_database_connection, get_db
from .schemas import (
    ContactRequest,
    ContactResponse,
    EducationSchema,
    ExperienceSchema,
    ProjectSchema,
    SkillSchema,
)
from .services.email import send_contact_email
app = FastAPI(title="Saleh Portfolio API", version="1.0.0")
app.add_middleware(
    RequestSizeLimitMiddleware,
    max_body_size=16 * 1024,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


@app.get("/", tags=["system"])
def read_root() -> dict[str, str]:
    return {"message": "Backend is running!"}


@app.get("/health/live", tags=["system"])
def liveness() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/ready", tags=["system"])
def readiness() -> dict[str, str]:
    try:
        check_database_connection()
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Database is unavailable") from exc
    return {"status": "ok"}


@app.get("/api/projects", response_model=list[ProjectSchema], tags=["portfolio"])
def get_projects(db: Session = Depends(get_db)) -> list[models.Project]:
    return db.query(models.Project).order_by(models.Project.id.asc()).all()


@app.get("/api/educations", response_model=list[EducationSchema], tags=["portfolio"])
def get_educations(db: Session = Depends(get_db)) -> list[models.Education]:
    return db.query(models.Education).order_by(
        models.Education.start_date.desc(),
        models.Education.id.asc(),
    ).all()


@app.get("/api/experiences", response_model=list[ExperienceSchema], tags=["portfolio"])
def get_experiences(db: Session = Depends(get_db)) -> list[models.Experience]:
    return db.query(models.Experience).order_by(
        models.Experience.start_date.desc(),
        models.Experience.id.asc(),
    ).all()


@app.get("/api/skills", response_model=list[SkillSchema], tags=["portfolio"])
def get_skills(db: Session = Depends(get_db)) -> list[models.Skill]:
    return db.query(models.Skill).order_by(models.Skill.id.asc()).all()


@app.post(
    "/api/contact",
    response_model=ContactResponse,
    status_code=status.HTTP_200_OK,
    tags=["contact"],
)
def send_contact_message(
    contact: ContactRequest,
    _: None = Depends(enforce_contact_rate_limit),
) -> ContactResponse:
    if contact.website:
        return ContactResponse(message="Message received")

    verify_turnstile_token(contact.turnstile_token)
    send_contact_email(contact)

    return ContactResponse(message="Message sent successfully")
