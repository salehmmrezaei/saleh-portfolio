import os

from app.config import get_database_url, get_migration_database_url


def test_migration_database_url_falls_back_to_runtime_url(
    monkeypatch,
) -> None:
    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql://runtime:password@localhost/portfolio",
    )
    monkeypatch.delenv("MIGRATION_DATABASE_URL", raising=False)

    assert get_migration_database_url() == (
        "postgresql+psycopg2://runtime:password@localhost/portfolio"
    )


def test_migration_database_url_uses_separate_setting(
    monkeypatch,
) -> None:
    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql://runtime:password@localhost/portfolio",
    )
    monkeypatch.setenv(
        "MIGRATION_DATABASE_URL",
        "postgresql://migration:password@localhost/portfolio",
    )

    assert get_database_url() == (
        "postgresql+psycopg2://runtime:password@localhost/portfolio"
    )
    assert get_migration_database_url() == (
        "postgresql+psycopg2://migration:password@localhost/portfolio"
    )