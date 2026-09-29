import os
from functools import lru_cache

from fastapi import HTTPException, Request, status
from redis import Redis
from redis.exceptions import RedisError


CONTACT_WINDOW_SECONDS = 60
CONTACT_REQUEST_LIMIT = 5

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


def enforce_contact_rate_limit(request: Request) -> None:
    client_ip = _get_client_ip(request)
    key = f"rate-limit:contact:{client_ip}"

    try:
        redis_client = _get_redis()

        count = int(
            redis_client.eval(
                RATE_LIMIT_SCRIPT,
                1,
                key,
                CONTACT_WINDOW_SECONDS,
            )
        )

        if count > CONTACT_REQUEST_LIMIT:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many contact requests. Please try again later.",
            )

    except HTTPException:
        raise

    except RedisError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Contact service is temporarily unavailable.",
        ) from exc