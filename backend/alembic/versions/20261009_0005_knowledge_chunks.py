"""add hybrid RAG knowledge chunks

Revision ID: 20261009_0005
Revises: 20260926_0004
"""

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import VECTOR
from sqlalchemy.dialects import postgresql


revision = "20261009_0005"
down_revision = "20260926_0004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    op.create_table(
        "knowledge_chunks",
        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
        ),
        sa.Column(
            "source_type",
            sa.String(length=32),
            nullable=False,
        ),
        sa.Column(
            "source_key",
            sa.String(length=128),
            nullable=False,
        ),
        sa.Column(
            "section",
            sa.String(length=64),
            nullable=False,
        ),
        sa.Column(
            "chunk_index",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "title",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "content",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "content_hash",
            sa.String(length=64),
            nullable=False,
        ),
        sa.Column(
            "embedding_model",
            sa.String(length=100),
            nullable=True,
        ),
        sa.Column(
            "embedding",
            VECTOR(1536),
            nullable=True,
        ),
        sa.Column(
            "search_document",
            postgresql.TSVECTOR(),
            sa.Computed(
                "to_tsvector("
                "'english'::regconfig, "
                "coalesce(title, '') || ' ' || content"
                ")",
                persisted=True,
            ),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.UniqueConstraint(
            "source_type",
            "source_key",
            "section",
            "chunk_index",
            name="uq_knowledge_chunk_identity",
        ),
    )

    op.create_index(
        "ix_knowledge_chunks_source_type",
        "knowledge_chunks",
        ["source_type"],
    )

    op.create_index(
        "ix_knowledge_chunks_source_key",
        "knowledge_chunks",
        ["source_key"],
    )

    op.create_index(
        "ix_knowledge_chunks_search_document",
        "knowledge_chunks",
        ["search_document"],
        postgresql_using="gin",
    )


    # Runtime role only needs retrieval access.
    # Knowledge synchronization uses MIGRATION_DATABASE_URL.
    op.execute(
        """
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1
                FROM pg_roles
                WHERE rolname = 'portfolio_app'
            ) THEN
                GRANT SELECT
                ON TABLE knowledge_chunks
                TO portfolio_app;
            END IF;
        END
        $$;
        """
    )


def downgrade() -> None:
    op.drop_index(
        "ix_knowledge_chunks_search_document",
        table_name="knowledge_chunks",
    )
    op.drop_index(
        "ix_knowledge_chunks_source_key",
        table_name="knowledge_chunks",
    )
    op.drop_index(
        "ix_knowledge_chunks_source_type",
        table_name="knowledge_chunks",
    )

    op.drop_table("knowledge_chunks")
