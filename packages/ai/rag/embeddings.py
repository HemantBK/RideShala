"""Embedding ingestion worker — processes reviews into vectors.

Reads approved reviews, chunks them by aspect, embeds via vLLM,
and upserts to Qdrant. Can run as a one-shot script or as a
background worker listening to a Redis queue.

All components are free and open source:
- Embedding model: nomic-embed-text v1.5 (Apache 2.0) via vLLM
- Vector DB: Qdrant (Apache 2.0)
- Queue: Redis (BSD)

Usage:
    # One-shot: embed all reviews from JSON file
    python -m packages.ai.rag.embeddings

    # Or import and use in background worker
    from packages.ai.rag.embeddings import EmbeddingPipeline
"""

import asyncio
import json
import logging
import os
import uuid
from pathlib import Path

from openai import AsyncOpenAI
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import PointStruct

logger = logging.getLogger(__name__)

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
EMBEDDING_BASE_URL = os.getenv("EMBEDDING_BASE_URL", "http://localhost:8001/v1")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-ai/nomic-embed-text-v1.5")
COLLECTION_NAME = "user_reviews"
BATCH_SIZE = 32

# Aspect keywords for chunking reviews
ASPECT_KEYWORDS = {
    "comfort": ["comfort", "seat", "posture", "ergonomic", "back", "pillion", "long ride"],
    "mileage": ["mileage", "fuel", "kpl", "kmpl", "petrol", "tank", "range", "economy"],
    "performance": ["power", "speed", "acceleration", "torque", "bhp", "fast", "overtake", "highway"],
    "build_quality": ["build", "quality", "paint", "rust", "finish", "plastic", "vibration", "rattle"],
    "value": ["value", "price", "worth", "money", "expensive", "cheap", "budget", "cost"],
    "service": ["service", "maintenance", "dealer", "workshop", "spare", "warranty"],
}


def detect_aspects(text: str) -> list[str]:
    """Detect which aspects a review text covers."""
    text_lower = text.lower()
    found = []
    for aspect, keywords in ASPECT_KEYWORDS.items():
        if any(kw in text_lower for kw in keywords):
            found.append(aspect)
    return found or ["general"]


def chunk_review(review: dict) -> list[dict]:
    """Split a review into aspect-based chunks for better retrieval."""
    text = review.get("text", "")
    aspects = detect_aspects(text)

    chunks = []
    for aspect in aspects:
        chunks.append({
            "id": str(uuid.uuid4()),
            "text": text,
            "bike_model": review.get("bike_model", ""),
            "aspect": aspect,
            "rating": review.get("rating"),
            "user_id": review.get("user_id", "anonymous"),
            "date": review.get("created_at", ""),
            "verified_owner": review.get("is_verified_owner", False),
            "mileage_kpl": review.get("mileage_kpl"),
        })

    return chunks


class EmbeddingPipeline:
    """Process reviews into vector embeddings and store in Qdrant."""

    def __init__(self):
        self.qdrant = AsyncQdrantClient(url=QDRANT_URL)
        self.embedder = AsyncOpenAI(
            base_url=EMBEDDING_BASE_URL,
            api_key="dummy",
        )

    async def embed_reviews(self, reviews: list[dict]) -> int:
        """Embed a list of reviews and upsert to Qdrant.

        Args:
            reviews: List of review dicts with text, bike_model, etc.

        Returns:
            Number of vectors upserted.
        """
        # Chunk all reviews by aspect
        all_chunks = []
        for review in reviews:
            all_chunks.extend(chunk_review(review))

        if not all_chunks:
            return 0

        # Process in batches
        total_upserted = 0
        for i in range(0, len(all_chunks), BATCH_SIZE):
            batch = all_chunks[i : i + BATCH_SIZE]
            texts = [c["text"] for c in batch]

            # Embed via vLLM embedding server
            try:
                response = await self.embedder.embeddings.create(
                    model=EMBEDDING_MODEL,
                    input=texts,
                )
            except Exception as e:
                logger.error(f"Embedding batch failed: {e}")
                continue

            # Build Qdrant points
            points = [
                PointStruct(
                    id=chunk["id"],
                    vector=emb.embedding,
                    payload={
                        "text": chunk["text"],
                        "bike_model": chunk["bike_model"],
                        "aspect": chunk["aspect"],
                        "rating": chunk["rating"],
                        "user_id": chunk["user_id"],
                        "date": chunk["date"],
                        "verified_owner": chunk["verified_owner"],
                        "mileage_kpl": chunk["mileage_kpl"],
                    },
                )
                for chunk, emb in zip(batch, response.data, strict=False)
            ]

            # Upsert to Qdrant
            await self.qdrant.upsert(collection_name=COLLECTION_NAME, points=points)
            total_upserted += len(points)
            logger.info(f"Upserted {len(points)} vectors (batch {i // BATCH_SIZE + 1})")

        return total_upserted


async def embed_from_file(filepath: str | None = None):
    """One-shot: embed all reviews from a JSON file."""
    if filepath is None:
        filepath = str(Path(__file__).parents[3] / "data" / "reviews.json")

    path = Path(filepath)
    if not path.exists():
        print(f"No reviews file at {path}. Submit some reviews first.")
        return

    reviews = json.loads(path.read_text())
    approved = [r for r in reviews if r.get("status") == "approved"]

    if not approved:
        print("No approved reviews to embed.")
        return

    print(f"Embedding {len(approved)} reviews...")
    pipeline = EmbeddingPipeline()
    count = await pipeline.embed_reviews(approved)
    print(f"Done. {count} vectors upserted to Qdrant collection '{COLLECTION_NAME}'.")


if __name__ == "__main__":
    asyncio.run(embed_from_file())
