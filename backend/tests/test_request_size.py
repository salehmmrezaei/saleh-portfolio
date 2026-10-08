from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from app.middleware.request_size import RequestSizeLimitMiddleware


app = FastAPI()
app.add_middleware(
    RequestSizeLimitMiddleware,
    max_body_size=16 * 1024,
    paths=("/api/contact", "/api/chat"),
)


@app.post("/api/contact")
async def contact(request: Request) -> dict[str, int]:
    body = await request.body()
    return {"size": len(body)}


@app.post("/api/chat")
async def chat(request: Request) -> dict[str, int]:
    body = await request.body()
    return {"size": len(body)}


client = TestClient(app)


def test_contact_allows_body_under_limit() -> None:
    response = client.post(
        "/api/contact",
        content=b"a" * 1024,
        headers={"Content-Type": "application/octet-stream"},
    )

    assert response.status_code == 200
    assert response.json() == {"size": 1024}


def test_contact_rejects_body_over_limit() -> None:
    response = client.post(
        "/api/contact",
        content=b"a" * (16 * 1024 + 1),
        headers={"Content-Type": "application/octet-stream"},
    )

    assert response.status_code == 413
    assert response.json() == {
        "detail": "Request body too large"
    }


def test_chat_rejects_body_over_limit() -> None:
    response = client.post(
        "/api/chat",
        content=b"a" * (16 * 1024 + 1),
        headers={"Content-Type": "application/octet-stream"},
    )

    assert response.status_code == 413
    assert response.json() == {
        "detail": "Request body too large"
    }
