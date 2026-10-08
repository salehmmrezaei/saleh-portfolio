import os
from datetime import datetime, timezone
from functools import lru_cache

from fastapi import HTTPException, Request, status
from redis import Redis
from redis.exceptions import RedisError


CONTACT_WINDOW_SECONDS = 60
CONTACT_REQUEST_LIMIT = 5

CHAT_WINDOW_SECONDS = 60
CHAT_REQUEST_LIMIT = 6
CHAT_DAILY_REQUEST_LIMIT = 250

RATE_LIMIT_SCRIPT = """
local current = redis.call("INCR", KEYS[1])

if current == 1 then
    redis.call("EXPIRE", KEYS[1], ARGV[1])
end

return current
"""


@lru_cache
def _get_redis() -> Redis:
    redis_url = os.getenv("REDIS_URL")

    if not redis_url:
        raise RuntimeError("REDIS_URL is not configured")

    return Redis.from_url(
        redis_url,
        decode_responses=True,
        socket_connect_timeout=2,
        socket_timeout=2,
    )


def _get_client_ip(request: Request) -> str:
    real_ip = request.headers.get("x-real-ip")

    if real_ip:
        return real_ip.strip()

    if request.client:
        return request.client.host

    return "unknown"


def _get_daily_chat_request_limit() -> int:
    raw_value = os.getenv(
        "CHAT_DAILY_REQUEST_LIMIT",
        str(CHAT_DAILY_REQUEST_LIMIT),
    )

    try:
        value = int(raw_value)
    except ValueError as exc:
        raise RuntimeError(
            "CHAT_DAILY_REQUEST_LIMIT must be an integer"
        ) from exc

    if value < 1:
        raise RuntimeError(
            "CHAT_DAILY_REQUEST_LIMIT must be positive"
        )

    return value


def _increment_counter(
    *,
    key: str,
    window_seconds: int,
) -> int:
    return int(
        _get_redis().eval(
            RATE_LIMIT_SCRIPT,
            1,
            key,
            window_seconds,
        )
    )


def _enforce_rate_limit(
    request: Request,
    *,
    scope: str,
    window_seconds: int,
    request_limit: int,
    limit_detail: str,
    unavailable_detail: str,
) -> None:
    client_ip = _get_client_ip(request)
    key = f"rate-limit:{scope}:{client_ip}"

    try:
        count = _increment_counter(
            key=key,
            window_seconds=window_seconds,
        )

        if count > request_limit:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=limit_detail,
            )

    except HTTPException:
        raise

    except (RedisError, RuntimeError) as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=unavailable_detail,
        ) from exc


def _enforce_daily_chat_limit() -> None:
    now = datetime.now(timezone.utc)

    seconds_since_midnight = (
        now.hour * 3600
        + now.minute * 60
        + now.second
    )

    seconds_until_midnight = max(
        1,
        24 * 60 * 60 - seconds_since_midnight,
    )

    key = f"budget:chat:{now.date().isoformat()}"

    try:
        count = _increment_counter(
            key=key,
            window_seconds=seconds_until_midnight,
        )

        if count > _get_daily_chat_request_limit():
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=(
                    "Daily chat capacity has been reached. "
                    "Please try again tomorrow."
                ),
            )

    except HTTPException:
        raise

    except (RedisError, RuntimeError) as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Chat service is temporarily unavailable.",
        ) from exc


def enforce_contact_rate_limit(request: Request) -> None:
    _enforce_rate_limit(
        request,
        scope="contact",
        window_seconds=CONTACT_WINDOW_SECONDS,
        request_limit=CONTACT_REQUEST_LIMIT,
        limit_detail=(
            "Too many contact requests. "
            "Please try again later."
        ),
        unavailable_detail=(
            "Contact service is temporarily unavailable."
        ),
    )


def enforce_chat_rate_limit(request: Request) -> None:
    _enforce_rate_limit(
        request,
        scope="chat",
        window_seconds=CHAT_WINDOW_SECONDS,
        request_limit=CHAT_REQUEST_LIMIT,
        limit_detail=(
            "Too many chat requests. "
            "Please try again later."
        ),
        unavailable_detail=(
            "Chat service is temporarily unavailable."
        ),
    )

    _enforce_daily_chat_limit()
