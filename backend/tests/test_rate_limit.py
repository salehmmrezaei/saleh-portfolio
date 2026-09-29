import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from app.services import rate_limit
from app.services.rate_limit import enforce_contact_rate_limit


class FakeRedis:
    def __init__(self) -> None:
        self.counts: dict[str, int] = {}

    def eval(
        self,
        script: str,
        number_of_keys: int,
        key: str,
        window_seconds: int,
    ) -> int:
        del script, number_of_keys, window_seconds

        self.counts[key] = self.counts.get(key, 0) + 1
        return self.counts[key]


def create_client(
    fake_redis: FakeRedis,
    monkeypatch: pytest.MonkeyPatch,
) -> TestClient:
    monkeypatch.setattr(
        rate_limit,
        "_get_redis",
        lambda: fake_redis,
    )

    app = FastAPI()

    @app.get("/test")
    def test_endpoint(
        _: None = Depends(enforce_contact_rate_limit),
    ) -> dict[str, str]:
        return {"status": "ok"}

    return TestClient(app)


def test_allows_five_requests_per_ip(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = create_client(FakeRedis(), monkeypatch)

    for _ in range(5):
        response = client.get(
            "/test",
            headers={"X-Real-IP": "203.0.113.10"},
        )
        assert response.status_code == 200


def test_rejects_sixth_request_per_ip(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = create_client(FakeRedis(), monkeypatch)

    for _ in range(5):
        client.get(
            "/test",
            headers={"X-Real-IP": "203.0.113.10"},
        )

    response = client.get(
        "/test",
        headers={"X-Real-IP": "203.0.113.10"},
    )

    assert response.status_code == 429
    assert response.json() == {
        "detail": "Too many contact requests. Please try again later."
    }


def test_limits_clients_independently(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = create_client(FakeRedis(), monkeypatch)

    for _ in range(5):
        client.get(
            "/test",
            headers={"X-Real-IP": "203.0.113.10"},
        )

    response = client.get(
        "/test",
        headers={"X-Real-IP": "203.0.113.20"},
    )

    assert response.status_code == 200