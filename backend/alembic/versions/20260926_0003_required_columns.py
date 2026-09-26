"""enforce required portfolio fields

Revision ID: 20260926_0003
Revises: 20260926_0002
"""

from alembic import op
import sqlalchemy as sa

revision = "20260926_0003"
down_revision = "20260926_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        UPDATE experience
        SET company_slug = CASE url
            WHEN 'https://www.cnr.it/' THEN 'cnr'
            WHEN 'https://zutre.com' THEN 'zutre'
            WHEN 'https://www.denxa.ca' THEN 'denxa'
            WHEN 'https://zincsulfate.co' THEN 'sulfate-shargh'
            ELSE company_slug
        END
        WHERE company_slug IS NULL
        """
    )

    op.execute("UPDATE projects SET skills = '{}' WHERE skills IS NULL")
    op.execute("UPDATE projects SET description = '{}' WHERE description IS NULL")
    op.execute("UPDATE experience SET skills = '{}' WHERE skills IS NULL")
    op.execute("UPDATE experience SET description = '{}' WHERE description IS NULL")
    op.execute("UPDATE skills SET skills = '{}' WHERE skills IS NULL")
    op.execute("UPDATE skills SET featured = FALSE WHERE featured IS NULL")

    required_columns = {
        "projects": {
            "name": sa.String(),
            "url": sa.String(),
            "skills": sa.ARRAY(sa.String()),
            "description": sa.ARRAY(sa.String()),
        },
        "experience": {
            "company": sa.String(),
            "company_slug": sa.String(),
            "role": sa.String(),
            "start_date": sa.Date(),
            "end_date": sa.Date(),
            "skills": sa.ARRAY(sa.String()),
            "url": sa.String(),
            "description": sa.ARRAY(sa.String()),
        },
        "education": {
            "institution": sa.String(),
            "degree": sa.String(),
            "grade": sa.String(),
            "start_date": sa.Date(),
            "end_date": sa.Date(),
            "country": sa.String(),
        },
        "skills": {
            "title": sa.String(),
            "skills": sa.ARRAY(sa.String()),
            "description": sa.String(),
            "featured": sa.Boolean(),
        },
    }
    for table, columns in required_columns.items():
        for column, column_type in columns.items():
            op.alter_column(
                table,
                column,
                existing_type=column_type,
                nullable=False,
            )


def downgrade() -> None:
    required_columns = {
        "projects": {
            "name": sa.String(),
            "url": sa.String(),
            "skills": sa.ARRAY(sa.String()),
            "description": sa.ARRAY(sa.String()),
        },
        "experience": {
            "company": sa.String(),
            "company_slug": sa.String(),
            "role": sa.String(),
            "start_date": sa.Date(),
            "end_date": sa.Date(),
            "skills": sa.ARRAY(sa.String()),
            "url": sa.String(),
            "description": sa.ARRAY(sa.String()),
        },
        "education": {
            "institution": sa.String(),
            "degree": sa.String(),
            "grade": sa.String(),
            "start_date": sa.Date(),
            "end_date": sa.Date(),
            "country": sa.String(),
        },
        "skills": {
            "title": sa.String(),
            "skills": sa.ARRAY(sa.String()),
            "description": sa.String(),
            "featured": sa.Boolean(),
        },
    }
    for table, columns in required_columns.items():
        for column, column_type in columns.items():
            op.alter_column(
                table,
                column,
                existing_type=column_type,
                nullable=True,
            )
