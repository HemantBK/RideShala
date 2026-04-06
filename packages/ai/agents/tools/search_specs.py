"""Tool: Search bike specifications database.

Queries PostgreSQL for motorcycle specs. All data is community-maintained
and sourced from OEM websites (facts are not copyrightable).
"""

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# For MVP without database: load from seed JSON
_SEED_DATA: list[dict] | None = None


def _load_seed_data() -> list[dict]:
    """Load seed data from JSON file (fallback when DB not available)."""
    global _SEED_DATA
    if _SEED_DATA is not None:
        return _SEED_DATA

    seed_file = Path(__file__).parents[4] / "data" / "seeds" / "bikes_india_top30.json"
    if seed_file.exists():
        _SEED_DATA = json.loads(seed_file.read_text())
        logger.info(f"Loaded {len(_SEED_DATA)} bikes from seed data")
    else:
        _SEED_DATA = []
        logger.warning("No seed data found")

    return _SEED_DATA


async def search_bike_specs(
    model_name: str | None = None,
    brand: str | None = None,
    category: str | None = None,
    max_price: int | None = None,
    min_price: int | None = None,
) -> list[dict]:
    """Search motorcycle specifications.

    Args:
        model_name: Bike model name (fuzzy match).
        brand: Filter by brand (exact).
        category: Filter by category (cruiser, sport, adventure, etc.).
        max_price: Maximum ex-showroom price in INR.
        min_price: Minimum ex-showroom price in INR.

    Returns:
        List of matching bike spec dicts.
    """
    # TODO: Replace with actual PostgreSQL query in production
    bikes = _load_seed_data()

    results = bikes
    if model_name:
        model_lower = model_name.lower()
        results = [b for b in results if model_lower in b["name"].lower() or model_lower in b["slug"]]
    if brand:
        results = [b for b in results if b["brand"].lower() == brand.lower()]
    if category:
        results = [b for b in results if b["category"].lower() == category.lower()]
    if max_price:
        results = [b for b in results if b.get("price_ex_showroom_inr", 0) <= max_price]
    if min_price:
        results = [b for b in results if b.get("price_ex_showroom_inr", 0) >= min_price]

    return results


async def get_bike_by_slug(slug: str) -> dict | None:
    """Get a single bike by its URL slug."""
    bikes = _load_seed_data()
    for bike in bikes:
        if bike["slug"] == slug:
            return bike
    return None
