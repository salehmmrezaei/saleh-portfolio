"""create portfolio schema

Revision ID: 20260926_0001
Revises:
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "20260926_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "projects",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String()),
        sa.Column("skills", postgresql.ARRAY(sa.String()), server_default=sa.text("'{}'")),
        sa.Column("url", sa.String()),
        sa.Column("description", postgresql.ARRAY(sa.String()), server_default=sa.text("'{}'")),
    )
    op.create_index("ix_projects_id", "projects", ["id"])
    op.create_index("ix_projects_name", "projects", ["name"])

    op.create_table(
        "experience",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("company", sa.String()),
        sa.Column("company_slug", sa.String()),
        sa.Column("role", sa.String()),
        sa.Column("start_date", sa.String()),
        sa.Column("end_date", sa.String()),
        sa.Column("skills", postgresql.ARRAY(sa.String()), server_default=sa.text("'{}'")),
        sa.Column("url", sa.String()),
        sa.Column("description", postgresql.ARRAY(sa.String()), server_default=sa.text("'{}'")),
    )
    op.create_index("ix_experience_id", "experience", ["id"])
    op.create_index("ix_experience_company", "experience", ["company"])
    op.create_index("ix_experience_company_slug", "experience", ["company_slug"])

    op.create_table(
        "education",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("institution", sa.String()),
        sa.Column("degree", sa.String()),
        sa.Column("grade", sa.String()),
        sa.Column("start_date", sa.String()),
        sa.Column("end_date", sa.String()),
        sa.Column("country", sa.String()),
    )
    op.create_index("ix_education_id", "education", ["id"])
    op.create_index("ix_education_institution", "education", ["institution"])

    op.create_table(
        "skills",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String()),
        sa.Column("skills", postgresql.ARRAY(sa.String()), server_default=sa.text("'{}'")),
        sa.Column("description", sa.String()),
        sa.Column("featured", sa.Boolean(), server_default=sa.false()),
    )
    op.create_index("ix_skills_id", "skills", ["id"])
    op.create_index("ix_skills_title", "skills", ["title"])


def downgrade() -> None:
    op.drop_table("skills")
    op.drop_table("education")
    op.drop_table("experience")
    op.drop_table("projects")
