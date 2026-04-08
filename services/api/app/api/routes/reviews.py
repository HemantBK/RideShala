"""User review API endpoints.

All reviews are user-generated content with explicit consent.
MVP: stores reviews in-memory. Production: PostgreSQL + Qdrant.
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path

import bleach
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator

logger = logging.getLogger(__name__)

router = APIRouter()

# MVP in-memory store (replaced by PostgreSQL in production)
_REVIEWS_STORE: list[dict] = []
_REVIEWS_FILE = Path(__file__).parents[5] / "data" / "reviews.json"


def _load_reviews() -> list[dict]:
    """Load persisted reviews from disk (MVP fallback)."""
    global _REVIEWS_STORE
    if _REVIEWS_STORE:
        return _REVIEWS_STORE
    if _REVIEWS_FILE.exists():
        try:
            _REVIEWS_STORE = json.loads(_REVIEWS_FILE.read_text())
        except Exception:
            _REVIEWS_STORE = []
    return _REVIEWS_STORE


def _save_reviews() -> None:
    """Persist reviews to disk (MVP fallback)."""
    try:
        _REVIEWS_FILE.parent.mkdir(parents=True, exist_ok=True)
        _REVIEWS_FILE.write_text(json.dumps(_REVIEWS_STORE, indent=2, default=str))
    except Exception as e:
        logger.warning(f"Could not persist reviews: {e}")


class ReviewSubmission(BaseModel):
    """Review submission with consent and validation."""

    bike_model: str = Field(..., min_length=2, max_length=100)
    text: str = Field(..., min_length=50, max_length=5000)
    rating: float = Field(..., ge=1.0, le=5.0)
    mileage_kpl: float | None = Field(None, ge=0, le=100)
    ownership_months: int | None = Field(None, ge=0, le=240)
    consent_granted: bool = Field(
        ..., description="User must explicitly consent to CC BY-SA 4.0 licensing"
    )
    is_original: bool = Field(
        ..., description="User confirms this is their original content"
    )

    @field_validator("text")
    @classmethod
    def sanitize_text(cls, v: str) -> str:
        return bleach.clean(v, tags=[], strip=True)

    @field_validator("consent_granted")
    @classmethod
    def must_consent(cls, v: bool) -> bool:
        if not v:
            raise ValueError("You must consent to the CC BY-SA 4.0 license to submit a review")
        return v

    @field_validator("is_original")
    @classmethod
    def must_be_original(cls, v: bool) -> bool:
        if not v:
            raise ValueError("Reviews must be your original content")
        return v


@router.post("")
async def submit_review(review: ReviewSubmission):
    """Submit a user review with moderation and consent tracking."""
    from app.services.moderation import moderate_review

    reviews = _load_reviews()

    # Run moderation pipeline (plagiarism, toxicity, spam, quality)
    moderation = moderate_review(review.text, reviews)

    if not moderation["approved"]:
        raise HTTPException(
            status_code=400,
            detail={
                "message": moderation["reason"],
                "checks": moderation["checks"],
            },
        )

    new_review = {
        "id": len(reviews) + 1,
        "bike_model": review.bike_model,
        "text": review.text,
        "rating": review.rating,
        "mileage_kpl": review.mileage_kpl,
        "ownership_months": review.ownership_months,
        "consent_granted": review.consent_granted,
        "is_original": review.is_original,
        "consent_timestamp": datetime.now().isoformat(),
        "status": "approved",
        "moderation": moderation["checks"],
        "created_at": datetime.now().isoformat(),
    }

    _REVIEWS_STORE.append(new_review)
    _save_reviews()

    # Queue for embedding pipeline (async, non-blocking)
    try:
        import redis.asyncio as aioredis

        r = aioredis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))
        await r.rpush("embedding_queue", json.dumps(new_review))
        await r.aclose()
    except Exception as e:
        logger.debug(f"Embedding queue unavailable (will embed later): {e}")

    return {
        "status": "approved",
        "message": "Thank you! Your review has been published.",
        "review_id": new_review["id"],
    }


@router.get("/{bike_model}")
async def get_reviews(
    bike_model: str,
    aspect: str | None = None,
    sort: str = "recent",
    limit: int = 20,
):
    """Get reviews for a bike model."""
    reviews = _load_reviews()

    # Filter by bike model (fuzzy match)
    model_lower = bike_model.lower().replace("-", " ")
    filtered = [
        r for r in reviews
        if model_lower in r.get("bike_model", "").lower().replace("-", " ")
        and r.get("status") == "approved"
    ]

    # Sort
    if sort == "recent":
        filtered.sort(key=lambda r: r.get("created_at", ""), reverse=True)
    elif sort == "rating":
        filtered.sort(key=lambda r: r.get("rating", 0), reverse=True)

    # Aggregate stats
    ratings = [r["rating"] for r in filtered if "rating" in r]
    mileages = [r["mileage_kpl"] for r in filtered if r.get("mileage_kpl")]

    return {
        "bike": bike_model,
        "reviews": filtered[:limit],
        "total": len(filtered),
        "avg_rating": round(sum(ratings) / len(ratings), 1) if ratings else None,
        "avg_mileage_kpl": round(sum(mileages) / len(mileages), 1) if mileages else None,
    }
