"""Create Qdrant vector collection for user reviews.

Usage:
    python data/migrations/001_create_qdrant_collection.py

Creates the 'user_reviews' collection with nomic-embed-text dimensions (768).
Idempotent — safe to run multiple times.
"""

import asyncio
import os

from qdrant_client import AsyncQdrantClient
from qdrant_client.models import Distance, VectorParams

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = "user_reviews"
VECTOR_SIZE = 768  # nomic-embed-text v1.5 output dimensions


async def create_collection():
    """Create the user_reviews collection in Qdrant."""
    client = AsyncQdrantClient(url=QDRANT_URL)

    collections = await client.get_collections()
    existing = [c.name for c in collections.collections]

    if COLLECTION_NAME in existing:
        print(f"Collection '{COLLECTION_NAME}' already exists. Skipping.")
        return

    await client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=VECTOR_SIZE,
            distance=Distance.COSINE,
        ),
    )

    # Create payload indexes for filtering
    await client.create_payload_index(
        collection_name=COLLECTION_NAME,
        field_name="bike_model",
        field_schema="keyword",
    )
    await client.create_payload_index(
        collection_name=COLLECTION_NAME,
        field_name="aspect",
        field_schema="keyword",
    )
    await client.create_payload_index(
        collection_name=COLLECTION_NAME,
        field_name="verified_owner",
        field_schema="bool",
    )

    print(f"Collection '{COLLECTION_NAME}' created with {VECTOR_SIZE}D vectors.")
    print("Payload indexes: bike_model, aspect, verified_owner")


if __name__ == "__main__":
    asyncio.run(create_collection())
