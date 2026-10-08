import os

import pytest
from fastapi.testclient import TestClient

os.environ.setdefault(
    "DATABASE_URL",
    "sqlite+pysqlite:///:memory:",
)

import app.main as main


@pytest.fixture
def client() -> TestClient:
    main.app.dependency_overrides[
        main.enforce_chat_rate_limit
    ] = lambda: None

    try:
        yield TestClient(main.app)
    finally:
        main.app.dependency_overrides.clear()


def test_chat_endpoint_returns_answer(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        main,
        "generate_chat_answer",
        lambda request: "Saleh builds practical AI systems.",
    )

    response = client.post(
        "/api/chat",
        json={
            "message": "What does Saleh work on?",
            "history": [],
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "answer": "Saleh builds practical AI systems."
    }


def test_chat_endpoint_validates_input(
    client: TestClient,
) -> None:
    response = client.post(
        "/api/chat",
        json={
            "message": "   ",
            "history": [],
        },
    )

    assert response.status_code == 422
