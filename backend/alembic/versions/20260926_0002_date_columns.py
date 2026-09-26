"""convert portfolio dates to date columns

Revision ID: 20260926_0002
Revises: 20260926_0001
"""

from alembic import op
import sqlalchemy as sa

revision = "20260926_0002"
down_revision = "20260926_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    for table in ("experience", "education"):
        for column in ("start_date", "end_date"):
            op.alter_column(
                table,
                column,
                existing_type=sa.String(),
                type_=sa.Date(),
                postgresql_using=f"{column}::date",
            )


def downgrade() -> None:
    for table in ("experience", "education"):
        for column in ("start_date", "end_date"):
            op.alter_column(
                table,
                column,
                existing_type=sa.Date(),
                type_=sa.String(),
                postgresql_using=f"{column}::text",
            )
