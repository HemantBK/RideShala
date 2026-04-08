# Changelog

All notable changes to RideShala are documented here.
Format based on [Keep a Changelog](https://keepachangelog.com/).

## [0.1.0] - 2026-04-08

### Added
- Multi-agent AI system with LangGraph (9 nodes: intent, clarify, research, comparison, safety, finance, ride plan, synthesize, guardrail)
- LLM provider routing with circuit breakers (vLLM primary, optional Claude/Groq fallback)
- Hybrid RAG pipeline (Qdrant dense + Meilisearch sparse + RRF + cross-encoder reranking)
- Streaming chat endpoint (SSE) with LangGraph integration
- Bike specs endpoint wired to 30-bike seed database
- AI comparison endpoint with real specs + LLM reasoning + fallback spec table
- TCO calculator using real RTO, IRDAI, and IOCL published rates
- Ride planner with OSRM routing, Open-Meteo weather, fuel stop calculator
- Review system with moderation pipeline (plagiarism, toxicity, spam, quality checks)
- Mileage tracking (community fill-up logs with real kpl calculation)
- Service cost tracking (dealer vs local breakdown)
- Community spec contribution workflow (Wikipedia-style with OEM source verification)
- Embedding pipeline (review → aspect chunking → nomic-embed-text → Qdrant)
- Self-hosted JWT authentication middleware
- Redis-backed rate limiting middleware
- Real health checks (PostgreSQL, Redis, Qdrant, LLM connectivity)
- SQLAlchemy models (bikes, reviews, usage_logs, consent_logs)
- Alembic initial migration
- Seed script for 30 Indian bikes with OEM specs
- Qdrant collection setup script
- Meilisearch index setup script
- RAGAS evaluation framework with 49 golden test cases
- Locust load testing configuration
- Next.js frontend with SSE streaming chat
- Docker Compose with 8 services (API, web, PostgreSQL, Qdrant, Redis, Meilisearch, vLLM, Grafana)
- Prometheus metrics + structured logging with request IDs
- CI/CD pipeline (ruff lint, pytest, security audit, secret detection)
- Full documentation (architecture, AI pipeline, API reference, setup, deployment, scaling, legal)
- MIT license (code) + CC BY-SA 4.0 (data) + third-party license tracking
- DPDP Act 2023 compliance (consent tracking, data retention, cross-border disclosure)
