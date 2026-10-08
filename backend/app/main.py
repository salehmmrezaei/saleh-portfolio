from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from .config import get_allowed_origins
from .database import check_database_connection
from .middleware.request_size import RequestSizeLimitMiddleware
from .schemas import ContactRequest, ContactResponse
from .services.email import send_contact_email
from .services.rate_limit import enforce_contact_rate_limit
from .services.turnstile import verify_turnstile_token

app = FastAPI(
    title="Saleh Portfolio API",
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

app.add_middleware(
    RequestSizeLimitMiddleware,
    max_body_size=16 * 1024,
    paths=("/api/contact", "/api/chat"),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


@app.get("/", tags=["system"])
def read_root() -> dict[str, str]:
    return {"message": "Backend is running!"}


@app.get("/health/live", tags=["system"])
def liveness() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/ready", tags=["system"])
def readiness() -> dict[str, str]:
    try:
        check_database_connection()
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="Database is unavailable",
        ) from exc

    return {"status": "ok"}


@app.post(
    "/api/contact",
    response_model=ContactResponse,
    status_code=status.HTTP_200_OK,
    tags=["contact"],
)
def send_contact_message(
    contact: ContactRequest,
    _: None = Depends(enforce_contact_rate_limit),
) -> ContactResponse:
    if contact.website:
        return ContactResponse(message="Message received")

    verify_turnstile_token(contact.turnstile_token)
    send_contact_email(contact)

    return ContactResponse(message="Message sent successfully")
