"""User review API endpoints.

All reviews are user-generated content with explicit consent.
Every review goes through moderation before being available.
"""

import bleach
from fastapi import APIRouter
from pydantic import BaseModel, Field, field_validator

router = APIRouter()


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
    """Submit a user review.

    Review goes through:
    1. Input validation (Pydantic)
    2. Plagiarism detection (reject copy-pasted reviews)
    3. Toxicity filtering
    4. Moderation queue (volunteer review)
    5. Embedding generation (batch pipeline)
    6. Published to platform
    """
    # TODO: Process through moderation pipeline
    return {"status": "pending_moderation", "message": "Thank you! Your review is being reviewed."}


@router.get("/{bike_model}")
async def get_reviews(
    bike_model: str,
    aspect: str | None = None,
    sort: str = "recent",
    limit: int = 20,
):
    """Get reviews for a bike model."""
    # TODO: Query from PostgreSQL + Qdrant
    return {"bike": bike_model, "reviews": [], "total": 0}
