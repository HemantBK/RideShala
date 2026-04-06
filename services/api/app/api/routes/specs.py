"""Bike specifications API endpoints."""

from fastapi import APIRouter, Query

router = APIRouter()


@router.get("")
async def list_bikes(
    search: str | None = Query(None, max_length=100),
    brand: str | None = Query(None, max_length=50),
    min_price: int | None = Query(None, ge=0),
    max_price: int | None = Query(None, le=50_00_000),
    category: str | None = Query(None),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """List bikes with optional search and filters."""
    # TODO: Query PostgreSQL with filters
    return {"bikes": [], "total": 0, "limit": limit, "offset": offset}


@router.get("/{bike_slug}")
async def get_bike(bike_slug: str):
    """Get full specifications for a single bike."""
    # TODO: Fetch from PostgreSQL
    return {"error": "Not implemented", "bike_slug": bike_slug}


@router.get("/{bike_slug}/reviews/summary")
async def get_review_summary(bike_slug: str):
    """Get AI-generated review summary for a bike.

    Aggregates insights from user reviews on our platform using
    the review synthesis agent.
    """
    # TODO: Call review synthesis agent
    return {"bike": bike_slug, "summary": None, "review_count": 0}
