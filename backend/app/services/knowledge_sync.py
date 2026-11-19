import argparse
import json
from collections import Counter
from dataclasses import asdict, dataclass

from sqlalchemy import create_engine, delete, select, func
from sqlalchemy.dialects.postgresql import insert

from ..config import get_migration_database_url
from .knowledge_builder import (
    KnowledgeChunkInput,
    build_knowledge_chunks,
)
from .knowledge_embeddings import (
    embed_chunks,
    get_embedding_model,
)


@dataclass(frozen=True)
class ExistingChunkState:
    id: int
    source_type: str
    source_key: str
    section: str
    chunk_index: int
    content_hash: str
    embedding_model: str | None
    has_embedding: bool


@dataclass(frozen=True)
class KnowledgeSyncResult:
    total: int
    embedded: int
    upserted: int
    deleted: int


def _identity(
    chunk: KnowledgeChunkInput,
) -> tuple[str, str, str, int]:
    return (
        chunk.source_type,
        chunk.source_key,
        chunk.section,
        chunk.chunk_index,
    )


def _existing_identity(
    chunk: ExistingChunkState,
) -> tuple[str, str, str, int]:
    return (
        chunk.source_type,
        chunk.source_key,
        chunk.section,
        chunk.chunk_index,
    )


def needs_embedding(
    *,
    chunk: KnowledgeChunkInput,
    existing: ExistingChunkState | None,
    embedding_model: str,
) -> bool:
    if existing is None:
        return True

    if existing.content_hash != chunk.content_hash:
        return True

    if existing.embedding_model != embedding_model:
        return True

    if not existing.has_embedding:
        return True

    return False


def sync_knowledge() -> KnowledgeSyncResult:
    from ..models import KnowledgeChunk

    chunks = build_knowledge_chunks()
    embedding_model = get_embedding_model()

    engine = create_engine(
        get_migration_database_url(),
        pool_pre_ping=True,
    )

    with engine.connect() as connection:
        rows = connection.execute(
            select(
                KnowledgeChunk.id,
                KnowledgeChunk.source_type,
                KnowledgeChunk.source_key,
                KnowledgeChunk.section,
                KnowledgeChunk.chunk_index,
                KnowledgeChunk.content_hash,
                KnowledgeChunk.embedding_model,
                KnowledgeChunk.embedding,
            )
        ).all()

    existing_chunks = [
        ExistingChunkState(
            id=row.id,
            source_type=row.source_type,
            source_key=row.source_key,
            section=row.section,
            chunk_index=row.chunk_index,
            content_hash=row.content_hash,
            embedding_model=row.embedding_model,
            has_embedding=row.embedding is not None,
        )
        for row in rows
    ]

    existing_by_identity = {
        _existing_identity(chunk): chunk
        for chunk in existing_chunks
    }

    changed_chunks = [
        chunk
        for chunk in chunks
        if needs_embedding(
            chunk=chunk,
            existing=existing_by_identity.get(
                _identity(chunk)
            ),
            embedding_model=embedding_model,
        )
    ]

    vectors = embed_chunks(changed_chunks)

    if len(vectors) != len(changed_chunks):
        raise RuntimeError(
            "Embedding count does not match "
            "changed chunk count."
        )

    desired_identities = {
        _identity(chunk)
        for chunk in chunks
    }

    stale_ids = [
        chunk.id
        for chunk in existing_chunks
        if _existing_identity(chunk)
        not in desired_identities
    ]

    with engine.begin() as connection:
        for chunk, vector in zip(
            changed_chunks,
            vectors,
            strict=True,
        ):
            statement = insert(
                KnowledgeChunk
            ).values(
                source_type=chunk.source_type,
                source_key=chunk.source_key,
                section=chunk.section,
                chunk_index=chunk.chunk_index,
                title=chunk.title,
                content=chunk.content,
                content_hash=chunk.content_hash,
                embedding_model=embedding_model,
                embedding=vector,
            )

            statement = (
                statement.on_conflict_do_update(
                    constraint=(
                        "uq_knowledge_chunk_identity"
                    ),
                    set_={
                        "title": statement.excluded.title,
                        "content": statement.excluded.content,
                        "content_hash": (
                            statement.excluded.content_hash
                        ),
                        "embedding_model": (
                            statement.excluded.embedding_model
                        ),
                        "embedding": (
                            statement.excluded.embedding
                        ),
                        "updated_at": func.now(),
                    },
                )
            )

            connection.execute(statement)

        if stale_ids:
            connection.execute(
                delete(KnowledgeChunk).where(
                    KnowledgeChunk.id.in_(
                        stale_ids
                    )
                )
            )

    engine.dispose()

    return KnowledgeSyncResult(
        total=len(chunks),
        embedded=len(changed_chunks),
        upserted=len(changed_chunks),
        deleted=len(stale_ids),
    )


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Validate or synchronize portfolio chatbot knowledge."
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--check",
        action="store_true",
        help="Build and validate source chunks without database or AI calls.",
    )
    mode.add_argument(
        "--sync",
        action="store_true",
        help="Embed changed chunks and update the configured knowledge database.",
    )
    args = parser.parse_args(argv)

    if args.check:
        chunks = build_knowledge_chunks()
        summary = {
            "total": len(chunks),
            "sources": dict(sorted(Counter(
                f"{chunk.source_type}/{chunk.source_key}"
                for chunk in chunks
            ).items())),
        }
    else:
        summary = asdict(sync_knowledge())

    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
