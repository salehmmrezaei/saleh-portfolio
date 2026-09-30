import re

from pydantic import BaseModel, Field, field_validator


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
