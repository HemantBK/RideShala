"""Community spec contribution workflow.

Wikipedia-style spec editing: anyone can submit corrections,
they go through review before being applied.

All contributions must include an OEM source URL.
Licensed under CC BY-SA 4.0.
"""

import json
import logging
from datetime import datetime
from pathlib import Path

import bleach
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator

logger = logging.getLogger(__name__)

router = APIRouter()

_CONTRIBUTIONS_FILE = Path(__file__).parents[5] / "data" / "contributions.json"


def _load_contributions() -> list[dict]:
    if _CONTRIBUTIONS_FILE.exists():
        try:
            return json.loads(_CONTRIBUTIONS_FILE.read_text())
        except Exception:
            return []
    return []


def _save_contributions(data: list[dict]) -> None:
    try:
        _CONTRIBUTIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
        _CONTRIBUTIONS_FILE.write_text(json.dumps(data, indent=2, default=str))
    except Exception as e:
        logger.warning(f"Could not save contributions: {e}")


# Allowed fields that can be updated
EDITABLE_FIELDS = {
    "engine_cc", "power_bhp", "torque_nm", "cylinders", "cooling",
    "weight_kg", "seat_height_mm", "ground_clearance_mm", "fuel_tank_litres",
    "wheelbase_mm", "abs_type", "traction_control", "riding_modes",
    "price_ex_showroom_inr", "gears", "transmission_type", "top_speed_kmph",
    "mileage_claimed_kpl", "year",
}


class SpecContribution(BaseModel):
    """A spec edit suggestion with required source."""

    bike_slug: str = Field(..., min_length=2, max_length=100)
    field_name: str = Field(..., description="Which spec field to update")
    old_value: str | None = Field(None, description="Current value (for verification)")
    new_value: str = Field(..., min_length=1, max_length=200)
    source_url: str = Field(
        ...,
        min_length=10,
        max_length=500,
        description="OEM website URL where this data is published",
    )
    reason: str = Field(
        ...,
        min_length=5,
        max_length=500,
        description="Why this change is needed",
    )

    @field_validator("field_name")
    @classmethod
    def validate_field(cls, v: str) -> str:
        if v not in EDITABLE_FIELDS:
            raise ValueError(
                f"Field '{v}' is not editable. Allowed: {', '.join(sorted(EDITABLE_FIELDS))}"
            )
        return v

    @field_validator("reason")
    @classmethod
    def sanitize_reason(cls, v: str) -> str:
        return bleach.clean(v, tags=[], strip=True)


@router.post("")
async def submit_contribution(contribution: SpecContribution):
    """Submit a spec correction for review.

    All contributions require an OEM source URL.
    Contributions are reviewed before being applied.
    """
    contributions = _load_contributions()

    # Check for duplicate pending contribution
    for existing in contributions:
        if (
            existing.get("bike_slug") == contribution.bike_slug
            and existing.get("field_name") == contribution.field_name
            and existing.get("status") == "pending"
        ):
            raise HTTPException(
                status_code=409,
                detail="A pending contribution for this field already exists.",
            )

    new_contribution = {
        "id": len(contributions) + 1,
        "bike_slug": contribution.bike_slug,
        "field_name": contribution.field_name,
        "old_value": contribution.old_value,
        "new_value": contribution.new_value,
        "source_url": contribution.source_url,
        "reason": contribution.reason,
        "status": "pending",  # pending -> approved/rejected
        "created_at": datetime.now().isoformat(),
        "reviewed_at": None,
        "reviewed_by": None,
    }

    contributions.append(new_contribution)
    _save_contributions(contributions)

    return {
        "status": "pending_review",
        "contribution_id": new_contribution["id"],
        "message": "Thank you! A maintainer will review your contribution.",
    }


@router.get("")
async def list_contributions(
    status: str = "pending",
    bike_slug: str | None = None,
    limit: int = 20,
):
    """List spec contributions, filtered by status."""
    contributions = _load_contributions()

    filtered = [c for c in contributions if c.get("status") == status]
    if bike_slug:
        filtered = [c for c in filtered if c.get("bike_slug") == bike_slug]

    filtered.sort(key=lambda c: c.get("created_at", ""), reverse=True)

    return {
        "contributions": filtered[:limit],
        "total": len(filtered),
    }


@router.get("/{contribution_id}")
async def get_contribution(contribution_id: int):
    """Get a single contribution by ID."""
    contributions = _load_contributions()
    for c in contributions:
        if c.get("id") == contribution_id:
            return c
    raise HTTPException(status_code=404, detail="Contribution not found")
