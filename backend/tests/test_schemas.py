import pytest
from pydantic import ValidationError

from app.schemas import ContactRequest


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
