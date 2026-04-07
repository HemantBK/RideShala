"""Hybrid RAG pipeline — dense + sparse search with re-ranking.

Combines Qdrant (dense/semantic) and Meilisearch (sparse/BM25) search
results using Reciprocal Rank Fusion, then re-ranks with a cross-encoder
for maximum retrieval quality.

Architecture:
    Query -> [Dense Search (Qdrant)] + [Sparse Search (Meilisearch)]
          -> Reciprocal Rank Fusion (k=60)
          -> Cross-Encoder Re-ranking (ms-marco-MiniLM-L-6-v2)
          -> Top-K results with source citations
"""

import asyncio
import logging
import os

from openai import AsyncOpenAI
from qdrant_client import AsyncQdrantClient
from sentence_transformers import CrossEncoder

logger = logging.getLogger(__name__)


class HybridRAG:
    """Hybrid retrieval pipeline combining dense and sparse search."""

    RRF_K = 60  # Reciprocal Rank Fusion constant

    def __init__(self):
        self.qdrant = AsyncQdrantClient(
            url=os.getenv("QDRANT_URL", "http://localhost:6333")
        )
        self.embedder = AsyncOpenAI(
            base_url=os.getenv("EMBEDDING_BASE_URL", "http://localhost:8001/v1"),
            api_key="dummy",
        )
        self.reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
        self.meili_url = os.getenv("MEILI_URL", "http://localhost:7700")
        self.meili_key = os.getenv("MEILI_MASTER_KEY", "")
        self.embedding_model = os.getenv("EMBEDDING_MODEL", "nomic-ai/nomic-embed-text-v1.5")

    async def search(
        self,
        query: str,
        bike_model: str | None = None,
        aspect: str | None = None,
        top_k: int = 10,
    ) -> list[dict]:
        """Search user reviews using hybrid dense + sparse retrieval.

        Args:
            query: Natural language search query.
            bike_model: Filter by bike model (optional).
            aspect: Filter by review aspect — comfort, mileage, etc. (optional).
            top_k: Number of results to return.

        Returns:
            List of search results with text, score, source citation, and metadata.
        """
        # 1. Run dense and sparse search in parallel
        dense_task = self._dense_search(query, bike_model, aspect, top_k=20)
        sparse_task = self._sparse_search(query, bike_model, top_k=20)
        dense_results, sparse_results = await asyncio.gather(dense_task, sparse_task)

        # 2. Merge with Reciprocal Rank Fusion
        fused = self._rrf_merge(dense_results, sparse_results)[:15]

        if not fused:
            return []

        # 3. Re-rank with cross-encoder
        pairs = [(query, doc["text"]) for doc in fused]
        scores = self.reranker.predict(pairs)
        reranked = sorted(zip(fused, scores, strict=False), key=lambda x: x[1], reverse=True)

        # 4. Return top-k with source citations
        return [
            {
                "text": doc["text"],
                "score": float(score),
                "source": f"User review on RideShala ({doc.get('date', 'unknown date')})",
                "bike_model": doc.get("bike_model", ""),
                "aspect": doc.get("aspect", ""),
                "verified_owner": doc.get("verified_owner", False),
            }
            for doc, score in reranked[:top_k]
        ]

    async def _dense_search(
        self, query: str, bike_model: str | None, aspect: str | None, top_k: int
    ) -> list[dict]:
        """Semantic search using Qdrant vector similarity."""
        # Generate query embedding via vLLM embedding server
        embedding_response = await self.embedder.embeddings.create(
            model=self.embedding_model,
            input=[query],
        )
        query_vector = embedding_response.data[0].embedding

        # Build Qdrant filter
        must_conditions = []
        if bike_model:
            must_conditions.append({"key": "bike_model", "match": {"value": bike_model}})
        if aspect:
            must_conditions.append({"key": "aspect", "match": {"value": aspect}})

        query_filter = {"must": must_conditions} if must_conditions else None

        # Search Qdrant
        results = await self.qdrant.search(
            collection_name="user_reviews",
            query_vector=query_vector,
            query_filter=query_filter,
            limit=top_k,
            with_payload=True,
        )

        return [
            {
                "id": str(r.id),
                "text": r.payload.get("text", ""),
                "score": r.score,
                "bike_model": r.payload.get("bike_model", ""),
                "aspect": r.payload.get("aspect", ""),
                "date": r.payload.get("date", ""),
                "verified_owner": r.payload.get("verified_owner", False),
            }
            for r in results
        ]

    async def _sparse_search(
        self, query: str, bike_model: str | None, top_k: int
    ) -> list[dict]:
        """Keyword search using Meilisearch BM25."""
        import httpx

        params = {"q": query, "limit": top_k}
        if bike_model:
            params["filter"] = f'bike_model = "{bike_model}"'

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.meili_url}/indexes/reviews/search",
                json=params,
                headers={"Authorization": f"Bearer {self.meili_key}"},
            )

        if response.status_code != 200:
            logger.warning(f"Meilisearch error: {response.status_code}")
            return []

        hits = response.json().get("hits", [])
        return [
            {
                "id": str(hit.get("id", "")),
                "text": hit.get("text", ""),
                "score": 1.0 / (i + 1),  # BM25 rank-based score
                "bike_model": hit.get("bike_model", ""),
                "aspect": hit.get("aspect", ""),
                "date": hit.get("date", ""),
                "verified_owner": hit.get("verified_owner", False),
            }
            for i, hit in enumerate(hits)
        ]

    def _rrf_merge(self, dense: list[dict], sparse: list[dict]) -> list[dict]:
        """Merge two ranked lists using Reciprocal Rank Fusion.

        RRF score = sum(1 / (k + rank)) across all lists where the doc appears.
        This gives a balanced combination regardless of score scale differences.
        """
        scores: dict[str, float] = {}
        docs: dict[str, dict] = {}

        for rank, doc in enumerate(dense):
            doc_id = doc["id"]
            scores[doc_id] = scores.get(doc_id, 0) + 1.0 / (self.RRF_K + rank + 1)
            docs[doc_id] = doc

        for rank, doc in enumerate(sparse):
            doc_id = doc["id"]
            scores[doc_id] = scores.get(doc_id, 0) + 1.0 / (self.RRF_K + rank + 1)
            if doc_id not in docs:
                docs[doc_id] = doc

        # Sort by fused score descending
        ranked_ids = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)
        return [docs[doc_id] for doc_id in ranked_ids if doc_id in docs]
