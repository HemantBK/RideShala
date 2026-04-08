"""Bike specifications API endpoints.

Returns real bike data from the seed database (MVP) or PostgreSQL (production).
All specs sourced from OEM manufacturer websites — facts are not copyrightable.
"""

from fastapi import APIRouter, HTTPException, Query

from packages.ai.agents.tools.search_specs import get_bike_by_slug, search_bike_specs

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
    results = await search_bike_specs(
        model_name=search,
        brand=brand,
        category=category,
        min_price=min_price,
        max_price=max_price,
    )

    total = len(results)
    paginated = results[offset : offset + limit]

    return {
        "bikes": paginated,
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@router.get("/{bike_slug}")
async def get_bike(bike_slug: str):
    """Get full specifications for a single bike."""
    bike = await get_bike_by_slug(bike_slug)
    if not bike:
        raise HTTPException(status_code=404, detail=f"Bike '{bike_slug}' not found")
    return bike


@router.get("/{bike_slug}/reviews/summary")
async def get_review_summary(bike_slug: str):
    """Get AI-generated review summary for a bike.

    Aggregates insights from user reviews on our platform.
    Returns placeholder until review data is populated.
    """
    bike = await get_bike_by_slug(bike_slug)
    if not bike:
        raise HTTPException(status_code=404, detail=f"Bike '{bike_slug}' not found")

    return {
        "bike": bike_slug,
        "bike_name": bike["name"],
        "brand": bike["brand"],
        "summary": "Review summaries will be available once the community contributes reviews.",
        "review_count": 0,
        "avg_rating": None,
    }
