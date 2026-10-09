from app.project_knowledge import PROJECT_KNOWLEDGE
from app.services.knowledge_builder import (
    build_knowledge_chunks,
)


def test_builds_unique_nonempty_chunks() -> None:
    chunks = build_knowledge_chunks()

    assert chunks

    identities = {
        (
            chunk.source_type,
            chunk.source_key,
            chunk.section,
            chunk.chunk_index,
        )
        for chunk in chunks
    }

    assert len(identities) == len(chunks)

    for chunk in chunks:
        assert chunk.title.strip()
        assert chunk.content.strip()
        assert len(chunk.content_hash) == 64


def test_contains_every_project() -> None:
    chunks = build_knowledge_chunks()

    project_keys = {
        chunk.source_key
        for chunk in chunks
        if chunk.source_type == "project"
    }

    assert project_keys == set(
        PROJECT_KNOWLEDGE
    )


def test_profile_has_precise_fact_chunks() -> None:
    chunks = build_knowledge_chunks()

    sections = {
        chunk.section
        for chunk in chunks
        if chunk.source_type == "profile"
    }

    assert "overview" in sections
    assert "experience" in sections
    assert "education" in sections
    assert "skills" in sections
    assert "availability" in sections
    assert "work_authorization" in sections
    assert "personal_interests" in sections
    assert "public_links" in sections


def test_repopilot_has_architecture_chunk() -> None:
    chunks = build_knowledge_chunks()

    matching = [
        chunk
        for chunk in chunks
        if (
            chunk.source_key == "repopilot-ai"
            and chunk.section == "architecture"
        )
    ]

    assert len(matching) == 1
    assert "PostgreSQL" in matching[0].content


def test_does_not_embed_raw_retrieval_term_lists() -> None:
    chunks = build_knowledge_chunks()

    assert all(
        chunk.section != "retrieval_terms"
        for chunk in chunks
    )
