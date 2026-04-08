"""Redis-backed rate limiting middleware.

Token bucket algorithm using Redis. Free — uses the Redis instance
already running in Docker Compose.

Limits:
    Anonymous:     10 requests/minute for chat, 60/minute for data APIs
    Authenticated: 30 requests/minute for chat, 120/minute for data APIs
"""

import logging
import os
import time

from fastapi import HTTPException, Request, status

logger = logging.getLogger(__name__)

LIMITS = {
    "anonymous": {"chat": 10, "data": 60},
    "authenticated": {"chat": 30, "data": 120},
}

# Endpoints that count as "chat" (LLM-intensive)
CHAT_ENDPOINTS = {"/api/v1/chat", "/api/v1/chat/stream", "/api/v1/compare"}


async def rate_limit_check(request: Request) -> None:
    """Check rate limit for the current request.

    Call this at the start of rate-limited endpoints.
    Raises 429 Too Many Requests if limit exceeded.
    """
    redis = getattr(request.app.state, "redis", None)
    if redis is None:
        return  # Skip rate limiting if Redis not available

    # Determine user identity
    user = getattr(request.state, "user", None) if hasattr(request.state, "user") else None
    user_id = user.get("sub") if user else request.client.host if request.client else "unknown"
    tier = "authenticated" if user else "anonymous"

    # Determine endpoint type
    path = request.url.path
    endpoint_type = "chat" if any(path.startswith(ep) for ep in CHAT_ENDPOINTS) else "data"

    limit = LIMITS[tier][endpoint_type]

    # Redis key: rate:{user_id}:{endpoint_type}:{minute_window}
    minute_window = int(time.time()) // 60
    key = f"rate:{user_id}:{endpoint_type}:{minute_window}"

    try:
        count = await redis.incr(key)
        if count == 1:
            await redis.expire(key, 60)

        if count > limit:
            retry_after = 60 - (int(time.time()) % 60)
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. {limit} requests/minute for {tier} users. Retry in {retry_after}s.",
                headers={"Retry-After": str(retry_after)},
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.warning(f"Rate limiter error (allowing request): {e}")
        # Fail open — if Redis is down, allow the request
