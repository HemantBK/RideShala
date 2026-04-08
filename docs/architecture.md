# Architecture

## System Overview

RideShala is a multi-service application with an AI-powered backend that uses a multi-agent system to process user queries about motorcycles.

```
                    ┌─────────────┐  ┌─────────────┐
                    │  Next.js    │  │  Flutter     │
                    │  Web App    │  │  Mobile App  │
                    └──────┬──────┘  └──────┬───────┘
                           │                │
                           └────────┬───────┘
                                    │
                             ┌──────▼──────┐
                             │   FastAPI   │  Rate Limiting
                             │   Backend   │  Circuit Breakers
                             └──────┬──────┘  Auth + CORS
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
             ┌──────▼──────┐ ┌─────▼─────┐ ┌──────▼──────┐
             │  LangGraph  │ │ Specs API │ │ Reviews API │
             │  Agents     │ │           │ │             │
             └──────┬──────┘ └─────┬─────┘ └──────┬──────┘
                    │              │               │
        ┌───────┬──┘        ┌─────▼─────┐  ┌─────▼──────┐
        │       │           │PostgreSQL │  │  Qdrant    │
        │       │           │(specs,    │  │  (review   │
        ▼       ▼           │ users)    │  │  vectors)  │
    ┌───────┐ ┌───────┐    └───────────┘  └────────────┘
    │ vLLM  │ │Claude │
    │(self- │ │(opt.) │    ┌───────────┐  ┌────────────┐
    │hosted)│ │       │    │   Redis   │  │Meilisearch │
    └───────┘ └───────┘    │  (cache)  │  │  (search)  │
                           └───────────┘  └────────────┘
```

## Tech Stack

| Layer | Technology | License | Why chosen |
|-------|-----------|---------|------------|
| Frontend | Next.js 14 | MIT | SSR, SEO, App Router |
| Backend | FastAPI | MIT | Async, fast, Python-native for AI |
| Database | PostgreSQL 16 | PostgreSQL | Relational data, ACID, mature |
| Vector DB | Qdrant | Apache 2.0 | Named vectors, filtering, snapshots |
| Cache | Redis 7 | BSD | Sessions, rate limiting, message queues |
| Search | Meilisearch | MIT | BM25 sparse retrieval for hybrid RAG |
| LLM | vLLM + Mistral 7B | Apache 2.0 | Self-hosted, zero restrictions, continuous batching |
| Embeddings | nomic-embed-text v1.5 | Apache 2.0 | Strong quality, servable via vLLM |
| Re-ranker | ms-marco-MiniLM-L-6-v2 | Apache 2.0 | Cross-encoder for RAG precision |
| Agents | LangGraph | MIT | State machine, conditional routing, explicit control |
| Maps | OpenStreetMap + OSRM | ODbL / BSD | Free routing, no API key |
| Weather | Open-Meteo | Open Source | Free, no API key needed |
| Monitoring | Grafana + Prometheus | Apache 2.0 | Industry standard observability |

## Key Design Decisions

| Decision | Choice | Alternative considered | Why |
|----------|--------|----------------------|-----|
| Monorepo vs multi-repo | Monorepo | 6 separate repos | Simpler for small team, shared types, atomic PRs |
| vLLM vs Ollama | vLLM | Ollama | Continuous batching (20-30 concurrent vs 1), PagedAttention, OpenAI-compatible API |
| Qdrant vs ChromaDB | Qdrant | ChromaDB | Production-grade, named vectors, snapshot backups, better filtering |
| LangGraph vs CrewAI | LangGraph | CrewAI | Explicit state management, conditional routing, more control over flow |
| Mistral 7B vs Llama 3.1 | Mistral 7B | Llama 3.1 8B | Apache 2.0 (zero restrictions) vs Llama License (700M MAU limit) |
| Hybrid RAG vs dense-only | Hybrid | Dense-only (Qdrant) | Catches both semantic and keyword matches |
| Self-hosted JWT vs Supabase | Self-hosted JWT | Supabase Auth | Zero external dependency, free |
| OpenStreetMap vs Google Maps | OpenStreetMap | Google Maps API | 100% free, no API key |

## Database Schema

### PostgreSQL Tables

**bikes** — Motorcycle specifications (community-maintained, sourced from OEMs)
- Engine: cc, bhp, torque, cylinders, cooling
- Dimensions: weight, seat height, ground clearance, tank, wheelbase
- Safety: ABS type, traction control, riding modes
- Pricing: ex-showroom price, source URL
- Community: avg real mileage, avg service cost, total reviews, avg rating

**reviews** — User-submitted reviews (with consent, CC BY-SA 4.0)
- Content: text, rating, aspect ratings (JSON)
- Ownership: months owned, total km, mileage, service cost
- Moderation: status (pending/approved/rejected), verified owner flag
- Legal: consent granted, consent timestamp, is_original_content

**usage_logs** — LLM API usage tracking
- Provider, model, input/output tokens, cost, feature, timestamp

**consent_logs** — DPDP Act 2023 compliance
- User ID, purpose, granted/withdrawn, timestamp

### Qdrant Collections

**user_reviews** — Review embeddings for semantic search
- Vector: nomic-embed-text (768 dimensions)
- Payload: text, bike_model, aspect, user_id, date, verified_owner

### Meilisearch Indexes

**reviews** — Full-text search for BM25 sparse retrieval
- Filterable: bike_model, aspect, verified_owner
- Searchable: text

## Project Structure

```
rideshala/
├── apps/web/                         Next.js 14 frontend
│   ├── app/page.tsx                  Home page with SSE streaming chat
│   └── app/layout.tsx                Root layout with navigation
│
├── services/api/                     FastAPI backend
│   ├── app/main.py                   Entry point (lifespan, CORS, metrics)
│   ├── app/api/routes/
│   │   ├── chat.py                   AI chat (streaming + sync)
│   │   ├── compare.py                Comparison + TCO calculator
│   │   ├── specs.py                  Bike specs (wired to seed data)
│   │   ├── reviews.py                Reviews with moderation pipeline
│   │   ├── tracking.py               Mileage + service cost tracking
│   │   ├── contributions.py          Community spec corrections
│   │   ├── feedback.py               Thumbs up/down + satisfaction stats
│   │   └── health.py                 Real connectivity probes
│   ├── app/middleware/
│   │   ├── auth.py                   Self-hosted JWT authentication
│   │   └── rate_limiter.py           Redis-backed rate limiting
│   ├── app/services/
│   │   └── moderation.py             Plagiarism + toxicity + spam + quality
│   ├── app/models/bike.py            SQLAlchemy models (4 tables)
│   ├── alembic/versions/             Database migrations
│   └── tests/                        16 tests across 5 files
│
├── packages/ai/                      AI/ML engine
│   ├── agents/
│   │   ├── graph.py                  LangGraph orchestration (9 nodes)
│   │   ├── state.py                  State schema
│   │   ├── nodes/
│   │   │   ├── classify_intent.py    Intent detection (vLLM)
│   │   │   ├── clarify.py            Asks user for more info (inline in graph.py)
│   │   │   ├── research.py           Queries real DB + RAG
│   │   │   ├── comparison.py         Real specs + RAG + LLM reasoning
│   │   │   ├── safety.py             LLM + hardcoded safety rules
│   │   │   ├── finance.py            Real EMI/RTO/insurance calculators
│   │   │   ├── ride_plan.py          OSRM routing + Open-Meteo weather
│   │   │   ├── synthesize.py         Combines outputs + LLM for general chat
│   │   │   └── guardrail.py          Blocks unsafe responses
│   │   └── tools/
│   │       ├── search_specs.py       Queries bike database (seed/PostgreSQL)
│   │       └── calculators.py        EMI, RTO, insurance formulas
│   ├── llm/
│   │   ├── router.py                 vLLM primary + optional Claude/Groq fallback
│   │   ├── cost_tracker.py           Token usage logging
│   │   └── providers/                vLLM, Claude, Groq provider classes
│   ├── rag/
│   │   ├── hybrid_search.py          Dense + sparse + RRF + cross-encoder
│   │   └── embeddings.py             Batch embedding worker (review → Qdrant)
│   ├── prompts/system_base.py        6 versioned system prompts
│   └── evaluation/
│       ├── ragas_eval.py             RAGAS evaluation framework
│       └── golden_testset.json       49 curated Q&A test cases
│
├── infra/
│   ├── docker-compose.yml            8 services (API, web, PG, Qdrant, Redis, Meili, vLLM, Grafana)
│   └── docker/                       Dockerfile.api, Dockerfile.web
│
├── data/
│   ├── seeds/
│   │   ├── bikes_india_top30.json    30 Indian bikes with OEM specs
│   │   └── seed_db.py                Load seed data into PostgreSQL
│   └── migrations/
│       ├── 001_create_qdrant_collection.py
│       └── 002_setup_meilisearch.py
│
├── tests/load/locustfile.py          Load testing (100 concurrent users)
├── notebooks/eda_bikes.py            Data exploration & distribution analysis
└── docs/                             This documentation (9 guides)
```
