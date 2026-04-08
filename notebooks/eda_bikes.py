"""Data Exploration & Analysis — Bike Database Profiling.

Run this script to generate distribution analysis of the bike database.
No Jupyter required — outputs stats to console and can generate plots.

Usage:
    python notebooks/eda_bikes.py
"""

import json
from collections import Counter
from pathlib import Path

SEED_FILE = Path(__file__).parent.parent / "data" / "seeds" / "bikes_india_top30.json"


def load_data() -> list[dict]:
    return json.loads(SEED_FILE.read_text())


def analyze():
    bikes = load_data()
    print(f"\n{'='*60}")
    print(f"RIDESHALA DATA EXPLORATION — {len(bikes)} BIKES")
    print(f"{'='*60}")

    # Brand distribution
    brands = Counter(b["brand"] for b in bikes)
    print(f"\n--- Brand Distribution ---")
    for brand, count in brands.most_common():
        bar = "#" * (count * 4)
        print(f"  {brand:20s} {count:2d}  {bar}")

    # Category distribution
    categories = Counter(b["category"] for b in bikes)
    print(f"\n--- Category Distribution ---")
    for cat, count in categories.most_common():
        bar = "#" * (count * 4)
        print(f"  {cat:20s} {count:2d}  {bar}")

    # Price distribution
    prices = [b["price_ex_showroom_inr"] for b in bikes if b.get("price_ex_showroom_inr")]
    print(f"\n--- Price Distribution (Ex-Showroom INR) ---")
    print(f"  Min:    Rs {min(prices):>10,}")
    print(f"  Max:    Rs {max(prices):>10,}")
    print(f"  Mean:   Rs {sum(prices)//len(prices):>10,}")
    print(f"  Median: Rs {sorted(prices)[len(prices)//2]:>10,}")

    # Price buckets
    buckets = {"Under 1L": 0, "1L-1.5L": 0, "1.5L-2L": 0, "2L-2.5L": 0, "2.5L-3L": 0, "3L+": 0}
    for p in prices:
        if p < 100000:
            buckets["Under 1L"] += 1
        elif p < 150000:
            buckets["1L-1.5L"] += 1
        elif p < 200000:
            buckets["1.5L-2L"] += 1
        elif p < 250000:
            buckets["2L-2.5L"] += 1
        elif p < 300000:
            buckets["2.5L-3L"] += 1
        else:
            buckets["3L+"] += 1

    print(f"\n--- Price Buckets ---")
    for bucket, count in buckets.items():
        bar = "#" * (count * 4)
        print(f"  {bucket:12s} {count:2d}  {bar}")

    # Engine size distribution
    engines = [b["engine_cc"] for b in bikes if b.get("engine_cc")]
    print(f"\n--- Engine Size Distribution ---")
    print(f"  Min:  {min(engines):>6.0f}cc")
    print(f"  Max:  {max(engines):>6.0f}cc")
    print(f"  Mean: {sum(engines)/len(engines):>6.0f}cc")

    # Safety features
    abs_types = Counter(b.get("abs_type", "unknown") for b in bikes)
    tc_count = sum(1 for b in bikes if b.get("traction_control"))
    print(f"\n--- Safety Features ---")
    for abs_type, count in abs_types.most_common():
        print(f"  ABS {abs_type:20s}: {count} bikes")
    print(f"  Traction control:       {tc_count}/{len(bikes)} bikes")

    # Seat height (important for Indian riders)
    seats = [b["seat_height_mm"] for b in bikes if b.get("seat_height_mm")]
    print(f"\n--- Seat Height Distribution ---")
    print(f"  Min:    {min(seats)}mm (best for short riders)")
    print(f"  Max:    {max(seats)}mm")
    print(f"  Mean:   {sum(seats)//len(seats)}mm")
    low_seat = [b for b in bikes if b.get("seat_height_mm", 999) <= 790]
    print(f"  Under 790mm (5'5-friendly): {len(low_seat)} bikes")

    # Mileage
    mileages = [b["mileage_claimed_kpl"] for b in bikes if b.get("mileage_claimed_kpl")]
    print(f"\n--- Mileage Distribution (Claimed KPL) ---")
    print(f"  Min:  {min(mileages)} kpl")
    print(f"  Max:  {max(mileages)} kpl")
    print(f"  Mean: {sum(mileages)/len(mileages):.1f} kpl")

    # Weight
    weights = [b["weight_kg"] for b in bikes if b.get("weight_kg")]
    print(f"\n--- Weight Distribution ---")
    print(f"  Lightest: {min(weights)} kg ({[b['name'] for b in bikes if b.get('weight_kg')==min(weights)][0]})")
    print(f"  Heaviest: {max(weights)} kg ({[b['name'] for b in bikes if b.get('weight_kg')==max(weights)][0]})")

    # Golden test set coverage
    testset_file = Path(__file__).parent.parent / "packages" / "ai" / "evaluation" / "golden_testset.json"
    if testset_file.exists():
        testset = json.loads(testset_file.read_text())
        test_cats = Counter(t["category"] for t in testset)
        print(f"\n--- Golden Test Set ({len(testset)} Q&A pairs) ---")
        for cat, count in test_cats.most_common():
            print(f"  {cat:20s}: {count} questions")

    print(f"\n{'='*60}")
    print("EDA complete.")


if __name__ == "__main__":
    analyze()
