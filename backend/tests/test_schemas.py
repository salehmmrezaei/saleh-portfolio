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


def test_chat_request_accepts_bounded_history() -> None:
    from app.schemas import ChatRequest

    request = ChatRequest(
        message="  What projects has Saleh built?  ",
        history=[
            {
                "role": "user",
                "content": "Tell me about Saleh.",
            },
            {
                "role": "assistant",
                "content": "Saleh is an AI/ML engineer.",
            },
        ],
    )

    assert request.message == "What projects has Saleh built?"
    assert len(request.history) == 2


def test_chat_request_rejects_blank_message() -> None:
    from app.schemas import ChatRequest

    with pytest.raises(ValidationError):
        ChatRequest(message="   ")


def test_chat_request_rejects_too_many_history_turns() -> None:
    from app.schemas import ChatRequest

    history = [
        {
            "role": "user",
            "content": f"Message {index}",
        }
        for index in range(7)
    ]

    with pytest.raises(ValidationError):
        ChatRequest(
            message="Hello",
            history=history,
        )
