"""User feedback endpoint — thumbs up/down on AI responses.

This data powers the feedback loop for model improvement.
After 10K+ rated interactions, QLoRA fine-tuning can begin.
"""

import json
import logging
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

router = APIRouter()

_FEEDBACK_FILE = Path(__file__).parents[5] / "data" / "feedback.json"


def _load_feedback() -> list[dict]:
    if _FEEDBACK_FILE.exists():
        try:
            return json.loads(_FEEDBACK_FILE.read_text())
        except Exception:
            return []
    return []


def _save_feedback(data: list[dict]) -> None:
    try:
        _FEEDBACK_FILE.parent.mkdir(parents=True, exist_ok=True)
        _FEEDBACK_FILE.write_text(json.dumps(data, indent=2, default=str))
    except Exception as e:
        logger.warning(f"Could not save feedback: {e}")


class FeedbackSubmission(BaseModel):
    """User feedback on an AI response."""

    query: str = Field(..., min_length=1, max_length=2000)
    response: str = Field(..., min_length=1, max_length=10000)
    rating: str = Field(..., description="'thumbs_up' or 'thumbs_down'")
    intent: str | None = Field(None, description="Detected intent of the query")
    provider: str | None = Field(None, description="LLM provider used")
    comment: str | None = Field(None, max_length=500, description="Optional user comment")


@router.post("")
async def submit_feedback(feedback: FeedbackSubmission):
    """Submit thumbs up/down feedback on an AI response.

    This data is used to:
    1. Track user satisfaction per intent/provider
    2. Identify low-quality responses for improvement
    3. Build fine-tuning dataset (after 10K+ rated interactions)
    """
    data = _load_feedback()

    entry = {
        "id": len(data) + 1,
        "query": feedback.query,
        "response": feedback.response,
        "rating": feedback.rating,
        "intent": feedback.intent,
        "provider": feedback.provider,
        "comment": feedback.comment,
        "created_at": datetime.now().isoformat(),
    }

    data.append(entry)
    _save_feedback(data)

    return {
        "status": "recorded",
        "feedback_id": entry["id"],
        "message": "Thank you for your feedback!",
    }


@router.get("/stats")
async def feedback_stats():
    """Get aggregated feedback statistics."""
    data = _load_feedback()

    if not data:
        return {"total": 0, "thumbs_up": 0, "thumbs_down": 0, "satisfaction_pct": None}

    thumbs_up = sum(1 for d in data if d.get("rating") == "thumbs_up")
    thumbs_down = sum(1 for d in data if d.get("rating") == "thumbs_down")
    total = len(data)

    # Per-intent breakdown
    by_intent = {}
    for d in data:
        intent = d.get("intent", "unknown")
        by_intent.setdefault(intent, {"up": 0, "down": 0})
        if d.get("rating") == "thumbs_up":
            by_intent[intent]["up"] += 1
        else:
            by_intent[intent]["down"] += 1

    # Per-provider breakdown
    by_provider = {}
    for d in data:
        provider = d.get("provider", "unknown")
        by_provider.setdefault(provider, {"up": 0, "down": 0})
        if d.get("rating") == "thumbs_up":
            by_provider[provider]["up"] += 1
        else:
            by_provider[provider]["down"] += 1

    return {
        "total": total,
        "thumbs_up": thumbs_up,
        "thumbs_down": thumbs_down,
        "satisfaction_pct": round(thumbs_up / total * 100, 1) if total > 0 else None,
        "by_intent": by_intent,
        "by_provider": by_provider,
        "fine_tuning_ready": total >= 10000,
        "fine_tuning_progress": f"{total}/10000 ({round(total/100, 1)}%)",
    }
