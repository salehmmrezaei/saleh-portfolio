import os
from functools import lru_cache

from fastapi import HTTPException, Request, status
from redis import Redis
from redis.exceptions import RedisError


CONTACT_WINDOW_SECONDS = 60
CONTACT_REQUEST_LIMIT = 5

CHAT_WINDOW_SECONDS = 60
CHAT_REQUEST_LIMIT = 6

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
        count = int(
            _get_redis().eval(
                RATE_LIMIT_SCRIPT,
                1,
                key,
                window_seconds,
            )
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


def enforce_contact_rate_limit(request: Request) -> None:
    _enforce_rate_limit(
        request,
        scope="contact",
        window_seconds=CONTACT_WINDOW_SECONDS,
        request_limit=CONTACT_REQUEST_LIMIT,
        limit_detail="Too many contact requests. Please try again later.",
        unavailable_detail="Contact service is temporarily unavailable.",
    )


def enforce_chat_rate_limit(request: Request) -> None:
    _enforce_rate_limit(
        request,
        scope="chat",
        window_seconds=CHAT_WINDOW_SECONDS,
        request_limit=CHAT_REQUEST_LIMIT,
        limit_detail="Too many chat requests. Please try again later.",
        unavailable_detail="Chat service is temporarily unavailable.",
    )
