import json
from urllib import error as urllib_error
from urllib import parse as urllib_parse
from urllib import request as urllib_request

from fastapi import HTTPException

from ..config import get_required_setting


TURNSTILE_VERIFY_URL = "https://challenges.cloudflare.com/turnstile/v0/siteverify"


def verify_turnstile_token(token: str) -> None:
    secret_key = get_required_setting("TURNSTILE_SECRET_KEY")

    payload = urllib_parse.urlencode(
        {
            "secret": secret_key,
            "response": token,
        }
    ).encode("utf-8")

    request = urllib_request.Request(
        TURNSTILE_VERIFY_URL,
        data=payload,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "saleh-portfolio/1.0",
        },
        method="POST",
    )

    try:
        with urllib_request.urlopen(request, timeout=5) as response:
            result = json.loads(response.read().decode("utf-8"))
    except (urllib_error.HTTPError, urllib_error.URLError, json.JSONDecodeError) as exc:
        raise HTTPException(
            status_code=502,
            detail="Unable to verify human challenge",
        ) from exc

    if not result.get("success"):
        raise HTTPException(
            status_code=400,
            detail="Human verification failed. Please try again.",
        )