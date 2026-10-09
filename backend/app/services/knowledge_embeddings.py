import os
from collections.abc import Sequence
from functools import lru_cache

from openai import OpenAI

from ..config import get_required_setting
from .knowledge_builder import KnowledgeChunkInput


DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIMENSIONS = 1536
EMBEDDING_BATCH_SIZE = 64


@lru_cache
def _get_embedding_client() -> OpenAI:
    return OpenAI(
        api_key=get_required_setting("OPENAI_API_KEY"),
        timeout=20.0,
        max_retries=1,
    )


def get_embedding_model() -> str:
    return (
        os.getenv(
            "OPENAI_EMBEDDING_MODEL",
            DEFAULT_EMBEDDING_MODEL,
        ).strip()
        or DEFAULT_EMBEDDING_MODEL
    )


def build_embedding_text(
    chunk: KnowledgeChunkInput,
) -> str:
    return (
        f"{chunk.title.strip()}\n\n"
        f"{chunk.content.strip()}"
    )


def embed_texts(
    texts: Sequence[str],
) -> list[list[float]]:
    if not texts:
        return []

    cleaned = [
        text.strip()
        for text in texts
    ]

    if any(not text for text in cleaned):
        raise ValueError(
            "Embedding input cannot be empty."
        )

    client = _get_embedding_client()
    embeddings: list[list[float]] = []

    for start in range(
        0,
        len(cleaned),
        EMBEDDING_BATCH_SIZE,
    ):
        batch = cleaned[
            start : start + EMBEDDING_BATCH_SIZE
        ]

        response = client.embeddings.create(
            model=get_embedding_model(),
            input=batch,
            encoding_format="float",
            dimensions=EMBEDDING_DIMENSIONS,
        )

        ordered = sorted(
            response.data,
            key=lambda item: item.index,
        )

        if len(ordered) != len(batch):
            raise RuntimeError(
                "Embedding response count "
                "does not match request count."
            )

        for item in ordered:
            vector = list(item.embedding)

            if len(vector) != EMBEDDING_DIMENSIONS:
                raise RuntimeError(
                    "Unexpected embedding dimension."
                )

            embeddings.append(vector)

    if len(embeddings) != len(cleaned):
        raise RuntimeError(
            "Embedding result count mismatch."
        )

    return embeddings


def embed_chunks(
    chunks: Sequence[KnowledgeChunkInput],
) -> list[list[float]]:
    return embed_texts(
        [
            build_embedding_text(chunk)
            for chunk in chunks
        ]
    )
