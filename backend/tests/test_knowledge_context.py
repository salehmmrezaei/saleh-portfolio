import json

from app.schemas import (
    ChatRequest,
    ChatTurn,
)
from app.services import knowledge_context
from app.services.knowledge_retrieval import (
    RetrievalCandidate,
    RetrievedKnowledge,
)


def fake_result(
    *,
    source_key: str = "repopilot-ai",
    section: str = "architecture",
    content: str = "Hybrid retrieval architecture.",
) -> RetrievedKnowledge:
    return RetrievedKnowledge(
        candidate=RetrievalCandidate(
            id=1,
            source_type="project",
            source_key=source_key,
            section=section,
            chunk_index=0,
            title="RepoPilot AI — Architecture",
            content=content,
        ),
        score=1.0,
        matched_by=("vector",),
    )


def test_direct_question_uses_current_message() -> None:
    payload = ChatRequest(
        message="Tell me about RepoPilot."
    )

    assert (
        knowledge_context.build_retrieval_query(
            payload
        )
        == "Tell me about RepoPilot."
    )


def test_follow_up_includes_previous_user_context() -> None:
    payload = ChatRequest(
        message="What about security?",
        history=[
            ChatTurn(
                role="user",
                content="Tell me about RepoPilot.",
            ),
            ChatTurn(
                role="assistant",
                content="RepoPilot is...",
            ),
        ],
    )

    query = (
        knowledge_context.build_retrieval_query(
            payload
        )
    )

    assert "Tell me about RepoPilot." in query
    assert "What about security?" in query


def test_context_contains_ranked_rag_chunks(
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        knowledge_context,
        "retrieve_knowledge",
        lambda query, limit: [
            fake_result()
        ],
    )

    payload = ChatRequest(
        message="How does RepoPilot work?"
    )

    context = json.loads(
        knowledge_context
        .build_chat_knowledge_context(
            payload
        )
    )

    chunks = context[
        "retrieved_chunks"
    ]

    assert len(chunks) == 1
    assert chunks[0]["rank"] == 1
    assert (
        chunks[0]["source_key"]
        == "repopilot-ai"
    )
    assert (
        chunks[0]["section"]
        == "architecture"
    )


def test_work_authorization_keeps_exact_profile_fact(
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        knowledge_context,
        "retrieve_knowledge",
        lambda query, limit: [],
    )

    payload = ChatRequest(
        message="Can Saleh work in Italy?"
    )

    context = json.loads(
        knowledge_context
        .build_chat_knowledge_context(
            payload
        )
    )

    assert (
        "work_authorization"
        in context["profile_facts"]
    )


def test_chunk_content_is_bounded(
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        knowledge_context,
        "retrieve_knowledge",
        lambda query, limit: [
            fake_result(
                content="x" * 5000
            )
        ],
    )

    payload = ChatRequest(
        message="Tell me about RepoPilot."
    )

    context = json.loads(
        knowledge_context
        .build_chat_knowledge_context(
            payload
        )
    )

    content = context[
        "retrieved_chunks"
    ][0]["content"]

    assert (
        len(content)
        == knowledge_context
        .MAX_CHUNK_CONTEXT_CHARS
    )
