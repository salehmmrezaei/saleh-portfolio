from types import SimpleNamespace

import pytest

from app.services import knowledge_embeddings
from app.services.knowledge_builder import (
    KnowledgeChunkInput,
)


class FakeEmbeddings:
    def __init__(self) -> None:
        self.calls: list[dict] = []

    def create(self, **kwargs):
        self.calls.append(kwargs)

        return SimpleNamespace(
            data=[
                SimpleNamespace(
                    index=index,
                    embedding=[0.1]
                    * knowledge_embeddings.EMBEDDING_DIMENSIONS,
                )
                for index, _ in enumerate(
                    kwargs["input"]
                )
            ]
        )


class FakeClient:
    def __init__(self) -> None:
        self.embeddings = FakeEmbeddings()


def test_build_embedding_text() -> None:
    chunk = KnowledgeChunkInput(
        source_type="project",
        source_key="repopilot-ai",
        section="architecture",
        chunk_index=0,
        title="RepoPilot AI — Architecture",
        content="Uses PostgreSQL and Redis.",
        content_hash="a" * 64,
    )

    assert (
        knowledge_embeddings.build_embedding_text(
            chunk
        )
        == (
            "RepoPilot AI — Architecture\n\n"
            "Uses PostgreSQL and Redis."
        )
    )


def test_embed_texts_uses_expected_model(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = FakeClient()

    monkeypatch.setattr(
        knowledge_embeddings,
        "_get_embedding_client",
        lambda: client,
    )

    monkeypatch.delenv(
        "OPENAI_EMBEDDING_MODEL",
        raising=False,
    )

    vectors = knowledge_embeddings.embed_texts(
        ["first", "second"]
    )

    assert len(vectors) == 2
    assert len(vectors[0]) == 1536

    call = client.embeddings.calls[0]

    assert (
        call["model"]
        == "text-embedding-3-small"
    )
    assert call["input"] == [
        "first",
        "second",
    ]
    assert call["encoding_format"] == "float"
    assert call["dimensions"] == 1536


def test_embed_texts_batches_requests(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = FakeClient()

    monkeypatch.setattr(
        knowledge_embeddings,
        "_get_embedding_client",
        lambda: client,
    )

    texts = [
        f"text-{index}"
        for index in range(
            knowledge_embeddings.EMBEDDING_BATCH_SIZE
            + 1
        )
    ]

    vectors = knowledge_embeddings.embed_texts(
        texts
    )

    assert len(vectors) == len(texts)
    assert len(client.embeddings.calls) == 2


def test_embed_texts_rejects_blank_input() -> None:
    with pytest.raises(
        ValueError,
        match="cannot be empty",
    ):
        knowledge_embeddings.embed_texts(
            ["valid", "   "]
        )


def test_embed_texts_handles_empty_list() -> None:
    assert (
        knowledge_embeddings.embed_texts([])
        == []
    )
