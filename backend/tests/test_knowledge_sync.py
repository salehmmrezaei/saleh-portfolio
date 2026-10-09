from app.services.knowledge_builder import (
    KnowledgeChunkInput,
)
from app.services.knowledge_sync import (
    ExistingChunkState,
    needs_embedding,
)


def make_chunk() -> KnowledgeChunkInput:
    return KnowledgeChunkInput(
        source_type="project",
        source_key="repopilot-ai",
        section="architecture",
        chunk_index=0,
        title="RepoPilot AI — Architecture",
        content="Hybrid retrieval architecture.",
        content_hash="a" * 64,
    )


def make_existing(
    *,
    content_hash: str = "a" * 64,
    embedding_model: str | None = (
        "text-embedding-3-small"
    ),
    has_embedding: bool = True,
) -> ExistingChunkState:
    return ExistingChunkState(
        id=1,
        source_type="project",
        source_key="repopilot-ai",
        section="architecture",
        chunk_index=0,
        content_hash=content_hash,
        embedding_model=embedding_model,
        has_embedding=has_embedding,
    )


def test_new_chunk_needs_embedding() -> None:
    assert needs_embedding(
        chunk=make_chunk(),
        existing=None,
        embedding_model="text-embedding-3-small",
    )


def test_unchanged_chunk_skips_embedding() -> None:
    assert not needs_embedding(
        chunk=make_chunk(),
        existing=make_existing(),
        embedding_model="text-embedding-3-small",
    )


def test_changed_content_needs_embedding() -> None:
    assert needs_embedding(
        chunk=make_chunk(),
        existing=make_existing(
            content_hash="b" * 64
        ),
        embedding_model="text-embedding-3-small",
    )


def test_changed_model_needs_embedding() -> None:
    assert needs_embedding(
        chunk=make_chunk(),
        existing=make_existing(
            embedding_model="old-model"
        ),
        embedding_model="text-embedding-3-small",
    )


def test_missing_embedding_needs_embedding() -> None:
    assert needs_embedding(
        chunk=make_chunk(),
        existing=make_existing(
            has_embedding=False
        ),
        embedding_model="text-embedding-3-small",
    )
