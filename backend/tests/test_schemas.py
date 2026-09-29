from datetime import date

import pytest
from pydantic import ValidationError

from app.schemas import ContactRequest, ExperienceSchema


def test_contact_request_validates_email_and_limits_fields() -> None:
    contact = ContactRequest(
        name="Saleh",
        email="saleh@example.com",
        subject="Hello",
        message="A message",
        turnstile_token="test-token",
    )

    assert contact.email == "saleh@example.com"


def test_contact_request_rejects_invalid_email() -> None:
    with pytest.raises(ValidationError):
        ContactRequest(
            name="Saleh",
            email="invalid",
            subject="Hello",
            message="A message",
            turnstile_token="test-token",
        )


def test_experience_schema_requires_typed_dates_and_http_url() -> None:
    experience = ExperienceSchema(
        id=1,
        company="CNR",
        company_slug="cnr",
        role="AI Engineer",
        start_date="2025-11-01",
        end_date="2026-08-31",
        skills=["Python"],
        url="https://example.com",
        description=["Built systems."],
    )

    assert experience.start_date == date(2025, 11, 1)
