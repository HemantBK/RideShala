"""Bike comparison API endpoints."""

from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter()


class CompareRequest(BaseModel):
    bikes: list[str] = Field(..., min_length=2, max_length=4)
    user_height_cm: int | None = Field(None, ge=100, le=220)
    user_city: str | None = None
    user_budget: int | None = Field(None, ge=0)


@router.post("")
async def compare_bikes(request: CompareRequest):
    """AI-powered bike comparison with reasoning.

    Uses the comparison agent (Claude for complex, vLLM for simple)
    to provide personalized trade-off analysis instead of just spec tables.
    """
    # TODO: Route through LangGraph comparison agent
    return {
        "bikes": request.bikes,
        "comparison": None,
        "sources": [],
        "provider": "none",
    }


@router.post("/tco")
async def compare_tco(request: CompareRequest):
    """Total Cost of Ownership comparison.

    Calculates 5-year ownership costs using legal data sources:
    OEM prices, government RTO rates, IRDAI insurance rates,
    user-reported fuel/service costs.
    """
    # TODO: Route through finance agent
    return {
        "bikes": request.bikes,
        "tco": None,
        "sources": [],
    }
