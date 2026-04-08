"""RideShala Error Codes — unique identifiers for every error type.

Every error in the system has a code like RS-1001.
When something breaks in production, search logs for the code
to instantly find the root cause.

Error code ranges:
    RS-1xxx  →  Authentication & authorization errors
    RS-2xxx  →  Input validation errors
    RS-3xxx  →  LLM & AI pipeline errors
    RS-4xxx  →  Database & storage errors
    RS-5xxx  →  External service errors (Groq, HuggingFace, weather, maps)
    RS-6xxx  →  Rate limiting & abuse prevention
    RS-7xxx  →  Data privacy & compliance errors
    RS-9xxx  →  Internal server errors
"""

import logging

from fastapi import HTTPException

logger = logging.getLogger(__name__)


class RideShalaError(HTTPException):
    """Base error with error code for traceability."""

    def __init__(self, code: str, message: str, status_code: int = 400):
        self.error_code = code
        logger.error(f"[{code}] {message}")
        super().__init__(
            status_code=status_code,
            detail={"error_code": code, "message": message},
        )


# ─── Authentication (RS-1xxx) ──────────────────────────
class AuthRequired(RideShalaError):
    def __init__(self):
        super().__init__("RS-1001", "Authentication required", 401)


class TokenExpired(RideShalaError):
    def __init__(self):
        super().__init__("RS-1002", "Token has expired", 401)


class TokenInvalid(RideShalaError):
    def __init__(self):
        super().__init__("RS-1003", "Invalid token", 401)


# ─── Input Validation (RS-2xxx) ────────────────────────
class BikeNotFound(RideShalaError):
    def __init__(self, slug: str):
        super().__init__("RS-2001", f"Bike '{slug}' not found in database", 404)


class ReviewTooShort(RideShalaError):
    def __init__(self):
        super().__init__("RS-2002", "Review must be at least 50 characters", 400)


class ConsentRequired(RideShalaError):
    def __init__(self):
        super().__init__("RS-2003", "Consent is required to submit content (CC BY-SA 4.0)", 400)


class DuplicateContent(RideShalaError):
    def __init__(self):
        super().__init__("RS-2004", "This content appears to be a duplicate", 409)


class ModerationRejected(RideShalaError):
    def __init__(self, reason: str):
        super().__init__("RS-2005", f"Content rejected by moderation: {reason}", 400)


class InvalidBikeCount(RideShalaError):
    def __init__(self):
        super().__init__("RS-2006", "Comparison requires 2-4 bikes", 400)


# ─── LLM & AI Pipeline (RS-3xxx) ──────────────────────
class LLMUnavailable(RideShalaError):
    def __init__(self):
        super().__init__("RS-3001", "AI service temporarily unavailable. Please try again.", 503)


class LLMTimeout(RideShalaError):
    def __init__(self):
        super().__init__("RS-3002", "AI response timed out. Please try a simpler question.", 504)


class IntentClassificationFailed(RideShalaError):
    def __init__(self):
        super().__init__("RS-3003", "Could not understand the question. Please rephrase.", 400)


class GraphExecutionFailed(RideShalaError):
    def __init__(self):
        super().__init__("RS-3004", "AI pipeline error. Please try again.", 500)


# ─── Database & Storage (RS-4xxx) ──────────────────────
class DatabaseConnectionFailed(RideShalaError):
    def __init__(self):
        super().__init__("RS-4001", "Database connection failed", 503)


class DataWriteFailed(RideShalaError):
    def __init__(self, resource: str):
        super().__init__("RS-4002", f"Failed to save {resource}", 500)


# ─── External Services (RS-5xxx) ───────────────────────
class WeatherServiceFailed(RideShalaError):
    def __init__(self):
        super().__init__("RS-5001", "Weather data unavailable", 502)


class RoutingServiceFailed(RideShalaError):
    def __init__(self):
        super().__init__("RS-5002", "Route planning service unavailable", 502)


class EmbeddingServiceFailed(RideShalaError):
    def __init__(self):
        super().__init__("RS-5003", "Embedding service unavailable", 502)


# ─── Rate Limiting (RS-6xxx) ──────────────────────────
class RateLimitExceeded(RideShalaError):
    def __init__(self, limit: int, tier: str):
        super().__init__(
            "RS-6001",
            f"Rate limit exceeded. {limit} requests/minute for {tier} users.",
            429,
        )


# ─── Data Privacy (RS-7xxx) ───────────────────────────
class UserDataNotFound(RideShalaError):
    def __init__(self, user_id: str):
        super().__init__("RS-7001", f"No data found for user '{user_id}'", 404)


class DataDeletionFailed(RideShalaError):
    def __init__(self):
        super().__init__("RS-7002", "Failed to delete user data. Contact support.", 500)


# ─── Internal (RS-9xxx) ──────────────────────────────
class InternalError(RideShalaError):
    def __init__(self):
        super().__init__("RS-9001", "Something went wrong. Please try again.", 500)
