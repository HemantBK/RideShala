"""Setup Meilisearch index for review full-text search (BM25 sparse retrieval).

Usage:
    python data/migrations/002_setup_meilisearch.py

Creates the 'reviews' index with filterable and searchable fields.
Idempotent — safe to run multiple times.

Meilisearch is MIT licensed, free, self-hosted.
"""

import json
import os
from pathlib import Path

import httpx

MEILI_URL = os.getenv("MEILI_URL", "http://localhost:7700")
MEILI_KEY = os.getenv("MEILI_MASTER_KEY", "")
INDEX_NAME = "reviews"


def setup_index():
    """Create and configure the reviews index in Meilisearch."""
    headers = {}
    if MEILI_KEY:
        headers["Authorization"] = f"Bearer {MEILI_KEY}"

    # Create index
    print(f"Creating index '{INDEX_NAME}'...")
    resp = httpx.post(
        f"{MEILI_URL}/indexes",
        json={"uid": INDEX_NAME, "primaryKey": "id"},
        headers=headers,
    )
    if resp.status_code in (200, 201, 202):
        print("Index created.")
    elif resp.status_code == 409:
        print("Index already exists.")
    else:
        print(f"Create index response: {resp.status_code} {resp.text}")

    # Configure filterable attributes
    print("Setting filterable attributes...")
    resp = httpx.put(
        f"{MEILI_URL}/indexes/{INDEX_NAME}/settings/filterable-attributes",
        json=["bike_model", "aspect", "verified_owner", "rating", "status"],
        headers=headers,
    )
    print(f"  Filterable: {resp.status_code}")

    # Configure searchable attributes
    print("Setting searchable attributes...")
    resp = httpx.put(
        f"{MEILI_URL}/indexes/{INDEX_NAME}/settings/searchable-attributes",
        json=["text", "bike_model"],
        headers=headers,
    )
    print(f"  Searchable: {resp.status_code}")

    # Configure sortable attributes
    print("Setting sortable attributes...")
    resp = httpx.put(
        f"{MEILI_URL}/indexes/{INDEX_NAME}/settings/sortable-attributes",
        json=["rating", "created_at"],
        headers=headers,
    )
    print(f"  Sortable: {resp.status_code}")

    # Load existing reviews if any
    reviews_file = Path(__file__).parents[1] / "reviews.json"
    if reviews_file.exists():
        reviews = json.loads(reviews_file.read_text())
        approved = [r for r in reviews if r.get("status") == "approved"]
        if approved:
            print(f"Indexing {len(approved)} approved reviews...")
            resp = httpx.post(
                f"{MEILI_URL}/indexes/{INDEX_NAME}/documents",
                json=approved,
                headers=headers,
            )
            print(f"  Indexed: {resp.status_code}")
    else:
        print("No reviews file found. Index is empty (reviews will be added as users submit them).")

    print("Meilisearch setup complete.")


if __name__ == "__main__":
    setup_index()
