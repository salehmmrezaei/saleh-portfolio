from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from app.schemas import ChatRequest
from app.services import chat


class FakeResponses:
    def __init__(self, output_text: str) -> None:
        self.output_text = output_text
        self.kwargs: dict[str, object] = {}

    def create(self, **kwargs: object) -> SimpleNamespace:
        self.kwargs = kwargs
        return SimpleNamespace(
            output_text=self.output_text,
        )


class FakeClient:
    def __init__(self, output_text: str) -> None:
        self.responses = FakeResponses(output_text)


def test_generate_chat_answer_uses_bounded_request(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = FakeClient("Saleh has worked on RAG systems.")

    monkeypatch.setattr(
        chat,
        "_get_openai_client",
        lambda: client,
    )
    monkeypatch.delenv(
        "OPENAI_CHAT_MODEL",
        raising=False,
    )

    payload = ChatRequest(
        message="What has Saleh done with RAG?",
        history=[
            {
                "role": "user",
                "content": "Tell me about his AI experience.",
            },
            {
                "role": "assistant",
                "content": "He has worked on AI systems.",
            },
        ],
    )

    answer = chat.generate_chat_answer(payload)

    assert answer == "Saleh has worked on RAG systems."

    kwargs = client.responses.kwargs

    assert kwargs["model"] == "gpt-6-luna"
    assert kwargs["max_output_tokens"] == 240
    assert kwargs["store"] is False

    assert kwargs["input"] == [
        {
            "role": "user",
            "content": "Tell me about his AI experience.",
        },
        {
            "role": "assistant",
            "content": "He has worked on AI systems.",
        },
        {
            "role": "user",
            "content": "What has Saleh done with RAG?",
        },
    ]

    instructions = str(kwargs["instructions"])

    assert "<portfolio_reference>" in instructions
    assert "RepoPilot AI" in instructions
    assert "API keys" in instructions


def test_generate_chat_answer_rejects_empty_output(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        chat,
        "_get_openai_client",
        lambda: FakeClient("   "),
    )

    with pytest.raises(HTTPException) as exc_info:
        chat.generate_chat_answer(
            ChatRequest(message="Tell me about Saleh.")
        )

    assert exc_info.value.status_code == 502
