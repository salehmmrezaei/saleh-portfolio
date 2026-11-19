import os
from types import SimpleNamespace

import pytest
from fastapi import HTTPException

os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite:///:memory:")

from app.schemas import ChatRequest
from app.services import chat
from app.services import knowledge_context
from app.services.knowledge_builder import build_knowledge_chunks
from app.services.knowledge_retrieval import RetrievalCandidate, RetrievedKnowledge


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
    monkeypatch.setattr(
        chat,
        "build_chat_knowledge_context",
        lambda payload: (
            '{"profile_facts":{},'
            '"retrieved_chunks":['
            '{"rank":1,'
            '"source_type":"project",'
            '"source_key":"repopilot-ai",'
            '"section":"overview",'
            '"title":"RepoPilot AI — Overview",'
            '"content":"RepoPilot AI uses hybrid retrieval."}'
            ']}'
        ),
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

    assert "<portfolio_knowledge>" in instructions
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
    monkeypatch.setattr(
        chat,
        "build_chat_knowledge_context",
        lambda payload: (
            '{"profile_facts":{},'
            '"retrieved_chunks":[]}'
        ),
    )

    with pytest.raises(HTTPException) as exc_info:
        chat.generate_chat_answer(
            ChatRequest(message="Tell me about Saleh.")
        )

    assert exc_info.value.status_code == 502


def test_system_instructions_strictly_reject_unrelated_questions() -> None:
    instructions = chat.SYSTEM_INSTRUCTIONS

    assert (
        "do not answer the unrelated question at all"
        in instructions
    )
    assert "celebrities, sports, politics" in instructions
    assert (
        "I can help with Saleh's portfolio"
        in instructions
    )


@pytest.mark.parametrize("project_key, demo_url", [
    ("mediflow-ai", "https://mediflow.salehmmrezaei.com/demo"),
    ("ai-rental-agent", "https://casa.salehmmrezaei.com"),
])
def test_project_demo_evidence_reaches_chat_model(
    monkeypatch: pytest.MonkeyPatch,
    project_key: str,
    demo_url: str,
) -> None:
    client = FakeClient("The public demo uses fictional data and simulated responses.")
    chunks = [
        chunk for chunk in build_knowledge_chunks()
        if chunk.source_key == project_key
        and chunk.section in {"public_demo", "public_links"}
    ]
    results = [
        RetrievedKnowledge(
            candidate=RetrievalCandidate(
                id=index, source_type=chunk.source_type,
                source_key=chunk.source_key, section=chunk.section,
                chunk_index=chunk.chunk_index, title=chunk.title,
                content=chunk.content,
            ),
            score=1.0, matched_by=("vector",),
        )
        for index, chunk in enumerate(chunks)
    ]
    monkeypatch.setattr(knowledge_context, "retrieve_knowledge", lambda *args, **kwargs: results)
    monkeypatch.setattr(chat, "_get_openai_client", lambda: client)

    chat.generate_chat_answer(ChatRequest(message=f"Can I try the {project_key} demo?"))

    instructions = str(client.responses.kwargs["instructions"])
    assert demo_url in instructions
    assert f"https://github.com/salehmmrezaei/{project_key}" in instructions
    assert "simulat" in instructions.lower()
    assert "A simulated demo is not a live model call" in instructions
    assert "copy\n  supplied public URLs exactly" in instructions
