import re
from datetime import date

from pydantic import AnyHttpUrl, BaseModel, ConfigDict, Field, field_validator


class ProjectSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    skills: list[str]
    url: AnyHttpUrl
    description: list[str]


class ExperienceSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company: str
    company_slug: str
    role: str
    start_date: date
    end_date: date
    skills: list[str]
    url: AnyHttpUrl
    description: list[str]


class EducationSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    institution: str
    degree: str
    grade: str
    start_date: date
    end_date: date
    country: str


class SkillSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    skills: list[str]
    description: str
    featured: bool


class ContactRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=3, max_length=254)
    subject: str = Field(min_length=1, max_length=160)
    message: str = Field(min_length=1, max_length=5000)
    website: str = Field(default="", max_length=200)
    turnstile_token: str = Field(min_length=1, max_length=2048)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", value):
            raise ValueError("Please enter a valid email address")
        return value


class ContactResponse(BaseModel):
    message: str
