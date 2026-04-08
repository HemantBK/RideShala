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


def _get_image_url(slug: str, brand: str, name: str) -> str:
    """Get bike image URL — real OEM images where available, placeholder otherwise.

    Real images are from OEM manufacturer websites (press/media images).
    These are publicly available and legal for editorial use.
    Community can contribute more real image URLs via spec contributions.
    """
    # Real OEM images from manufacturer media/product pages
    oem_images = {
        "royal-enfield-meteor-350": "https://www.royalenfield.com/content/dam/royal-enfield/india/motorcycles/meteor/colours/stellar/meteor-350-stellar-red-702x512.png",
        "royal-enfield-classic-350": "https://www.royalenfield.com/content/dam/royal-enfield/india/motorcycles/classic/colours/dark/classic-350-dark-gunmetal-grey-702x512.png",
        "royal-enfield-hunter-350": "https://www.royalenfield.com/content/dam/royal-enfield/india/motorcycles/hunter/colours/retro/hunter-350-retro-dapper-ash-702x512.png",
        "royal-enfield-guerrilla-450": "https://www.royalenfield.com/content/dam/royal-enfield/india/motorcycles/guerrilla/colours/guerrilla-playa-black-702x512.png",
        "royal-enfield-himalayan-450": "https://www.royalenfield.com/content/dam/royal-enfield/india/motorcycles/himalayan/colours/himalayan-kamet-white-702x512.png",
    }

    if slug in oem_images:
        return oem_images[slug]

    # Fallback: branded placeholder with bike name
    brand_colors = {
        "Royal Enfield": "8B0000",
        "Honda": "CC0000",
        "Hero": "004B87",
        "Bajaj": "1A1A6C",
        "TVS": "0047AB",
        "KTM": "FF6600",
        "Yamaha": "0033A0",
        "Triumph": "000000",
        "Jawa": "8B4513",
        "Suzuki": "003DA5",
        "Kawasaki": "28A745",
    }
    color = brand_colors.get(brand, "333333")
    text = f"{brand}+{name}".replace(" ", "+")
    return f"https://placehold.co/600x400/{color}/white?text={text}"


def _load_seed_data() -> list[dict]:
    """Load seed data from JSON file (fallback when DB not available)."""
    global _SEED_DATA
    if _SEED_DATA is not None:
        return _SEED_DATA

    seed_file = Path(__file__).parents[4] / "data" / "seeds" / "bikes_india_top30.json"
    if seed_file.exists():
        _SEED_DATA = json.loads(seed_file.read_text())
        # Add image URLs to each bike
        for bike in _SEED_DATA:
            if "image_url" not in bike:
                bike["image_url"] = _get_image_url(bike["slug"], bike["brand"], bike["name"])
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
