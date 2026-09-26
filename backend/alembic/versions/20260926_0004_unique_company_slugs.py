"""enforce unique experience company slugs

Revision ID: 20260926_0004
Revises: 20260926_0003
"""

from alembic import op

revision = "20260926_0004"
down_revision = "20260926_0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_unique_constraint(
        "uq_experience_company_slug",
        "experience",
        ["company_slug"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_experience_company_slug",
        "experience",
        type_="unique",
    )
