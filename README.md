# RideShala

**Open-source AI-powered motorcycle comparison for Indian riders.**

Built with Mistral 7B | vLLM | LangGraph | FastAPI | Next.js | 100% Free & Open Source

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Data: CC BY-SA 4.0](https://img.shields.io/badge/Data-CC%20BY--SA%204.0-blue.svg)](DATA_LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

---

## What is RideShala?

RideShala is a free, open-source AI motorcycle advisor built for Indian riders. Instead of dropping you into a spec table and leaving you to figure things out, RideShala understands **you** — your height, budget, commute, city, and riding style — and tells you exactly which bike fits your life, and **why**.

```
You:  "5'7, back pain, Bangalore commute 25km, weekend Coorg trips, budget 2.5L"

RideShala: "I recommend the Meteor 350 because:
           - 765mm seat = your feet flat on ground at 5'7
           - Cruiser posture = less back strain than a roadster
           - 15L tank = Bangalore to Coorg without refueling
           - Rs 2.19L = Rs 31K under budget for accessories

           But: 20 bhp may feel slow on Shiradi Ghat inclines.
           Alternative: Hero Mavrick 440 (27 bhp) at Rs 2.15L

           [Sources: royalenfield.com specs, 847 user reviews on RideShala]"
```

Every claim has a source. Every recommendation has reasoning. If the AI doesn't have enough data, it says so.

---

## What Makes RideShala Different

### It understands YOU, not just bikes
Most tools show the same spec table to everyone. RideShala factors in your height (seat height matching), your city (pricing, dealer info, road conditions), your commute (fuel cost, comfort), your budget (total cost of ownership, not just sticker price), and your riding style. Two people asking about the same bike get different answers based on their situation.

### Every answer comes with a reason and a source
RideShala never says "this bike is good" without explaining why and linking where that data came from — whether it's the manufacturer's published specs, government RTO rates, or aggregated data from real owners on the platform. No black-box recommendations.

### Real-world data from real owners
Claimed mileage is a marketing number. RideShala tracks **actual mileage** from user-logged fill-ups, **actual service costs** from user-logged visits, and **actual ownership experiences** from verified reviews. The community builds the data together.

### It warns you, not just sells to you
RideShala has hardcoded safety rules the AI cannot override — it will always recommend dual-channel ABS, always suggest proper riding gear, and always flag known issues reported by owners. No hidden sponsorships. No brand deals. The AI works for the rider, not the manufacturer.

### AI that thinks, not just filters
Six specialized AI agents work together behind every answer:
- **Research Agent** finds bikes matching your criteria
- **Comparison Agent** reasons through real trade-offs between models
- **Safety Agent** checks safety features and known issues
- **Finance Agent** calculates 5-year ownership cost using government data
- **Ride Plan Agent** plans routes with fuel stops and weather
- **Guardrail** blocks unsafe or misleading responses

### 100% open source, community-owned
The code is MIT licensed. The bike database is CC BY-SA 4.0. Anyone can audit the recommendation logic, download the data, host their own instance, or contribute improvements. No corporation controls it. No ads fund it. The community owns it.

### 100% legally clean data
Every data point has a documented legal source — manufacturer-published specs (facts are not copyrightable), government data (RTO, insurance, fuel prices), free APIs, and original user contributions with explicit consent. Nothing scraped. Nothing grey-area.

### 100% free to run
Self-hosted Mistral 7B (Apache 2.0) on your own GPU. PostgreSQL, Qdrant, Redis, Meilisearch — all open source. OpenStreetMap for maps, Open-Meteo for weather. No paid API keys required. Zero monthly cost beyond your own hardware.

---

## AI Skills Demonstrated

This project showcases **15 production AI/ML skills**:

| Skill | Technology | Status |
|-------|-----------|--------|
| Self-hosted LLM serving | vLLM + Llama 3.1 8B (AWQ quantized) | Scaffolded |
| Cloud LLM API | Claude Sonnet (Anthropic SDK) | Scaffolded |
| Multi-agent orchestration | LangGraph (state machine, conditional routing) | Scaffolded |
| RAG pipeline | Hybrid search (dense + sparse + re-ranking) | Scaffolded |
| Vector database | Qdrant (embeddings, filtering, snapshots) | Scaffolded |
| Embeddings | nomic-embed-text via vLLM serving | Scaffolded |
| Streaming responses | SSE via FastAPI + vLLM/Claude native streaming | Scaffolded |
| Prompt engineering | Versioned prompts, few-shot, chain-of-thought | Scaffolded |
| Evaluation | RAGAS framework (faithfulness, relevancy) | Planned |
| Fine-tuning | QLoRA on Llama 3.1 8B (Phase 4) | Planned |
| MLOps | MLflow, A/B testing, drift monitoring | Planned |
| NLP | Intent classification, sentiment, entity extraction | Scaffolded |
| Content generation | Comparison reports, social cards, ride plans | Planned |
| Responsible AI | Bias audits, guardrails, citations, confidence | Scaffolded |
| Cost optimization | Budget guardrails, tiered routing, AWQ quantization | Scaffolded |

---

## Architecture

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
    │(self- │ │Sonnet │    ┌───────────┐  ┌────────────┐
    │hosted)│ │(API)  │    │   Redis   │  │Meilisearch │
    └───────┘ └───────┘    │  (cache)  │  │  (search)  │
                           └───────────┘  └────────────┘
```

### LangGraph Agent Flow

```
User Message
     │
     ▼
classify_intent (vLLM — fast, free)
     │
     ├── bike_search ──── research agent ────┐
     ├── compare ──────── comparison agent ──┤
     ├── safety ───────── safety agent ──────┤──► synthesize ──► guardrail ──► Response
     ├── tco ──────────── finance agent ─────┤
     ├── ride_plan ────── ride plan agent ───┘
     ├── general_chat ──► synthesize directly
     └── unclear ───────► ask for clarification
```

### LLM Provider Routing

| Task Complexity | Primary | Fallback 1 | Fallback 2 |
|----------------|---------|------------|------------|
| Simple (chat, greetings) | vLLM (free) | Groq (free tier) | Claude |
| Complex (comparison, safety, TCO) | Claude Sonnet | Groq 70B | vLLM (degraded) |
| Budget exceeded | vLLM (forced) | Groq | — |

---

## Project Structure

```
rideshala/
├── apps/
│   ├── web/                          Next.js 14 frontend
│   │   ├── app/                      App router pages
│   │   ├── components/               UI components
│   │   └── lib/                      API client, utilities
│   └── mobile/                       Flutter app (Phase 3)
│
├── services/
│   └── api/                          FastAPI backend
│       ├── app/
│       │   ├── main.py               App entry point (CORS, metrics, logging)
│       │   ├── api/routes/
│       │   │   ├── chat.py           SSE streaming chat endpoint
│       │   │   ├── compare.py        AI comparison endpoint
│       │   │   ├── specs.py          Bike specs CRUD
│       │   │   ├── reviews.py        Review submission + retrieval
│       │   │   └── health.py         Liveness/readiness probes
│       │   ├── middleware/            Rate limiter, circuit breaker, auth
│       │   ├── models/               SQLAlchemy ORM models
│       │   └── services/             Business logic
│       ├── alembic/                  Database migrations
│       ├── tests/
│       └── requirements.txt
│
├── packages/
│   └── ai/                           AI/ML engine
│       ├── agents/
│       │   ├── graph.py              LangGraph orchestration graph
│       │   ├── state.py              State schema (RideShalaState)
│       │   └── nodes/
│       │       ├── classify_intent.py  Intent detection (vLLM)
│       │       ├── comparison.py       Bike comparison (Claude)
│       │       ├── safety.py           Safety assessment (Claude)
│       │       ├── finance.py          TCO calculator
│       │       ├── research.py         Bike search agent
│       │       ├── ride_plan.py        Route planner
│       │       ├── synthesize.py       Response assembly
│       │       └── guardrail.py        Safety guardrails
│       ├── llm/
│       │   ├── router.py              Provider routing + fallback chain
│       │   ├── cost_tracker.py         Token usage + budget enforcement
│       │   └── providers/
│       │       ├── vllm_provider.py    Self-hosted (OpenAI-compatible)
│       │       ├── claude_provider.py  Anthropic SDK
│       │       └── groq_provider.py    Groq free tier
│       ├── rag/
│       │   └── hybrid_search.py        Dense + sparse + RRF + reranker
│       ├── prompts/
│       │   └── system_base.py          Versioned system prompts
│       └── evaluation/                 RAGAS eval + golden test set
│
├── infra/
│   ├── docker-compose.yml             Dev environment (all services)
│   ├── docker/                        Dockerfiles
│   └── k8s/                           Kubernetes manifests (Phase 2)
│
├── data/
│   ├── seeds/                         Initial 30 bikes (JSON)
│   └── migrations/                    Vector DB migrations
│
├── .env.example                       Environment template (SAFE to push)
├── .gitignore                         Excludes secrets, models, volumes
├── LICENSE                            MIT License
├── DATA_LICENSE                       Dual: CC BY-SA (bulk) + CC BY (API)
├── THIRD_PARTY_LICENSES               All model & library licenses
└── README.md                          This file
```

---

## Tech Stack — 100% Free & Open Source

```
╔═══════════════════════════════════════════════════════════════╗
║  RideShala runs entirely on FREE, OPEN-SOURCE software.       ║
║  No paid API keys. No SaaS dependencies. No vendor lock-in. ║
║  Everything self-hosted on your own hardware.                ║
╚═══════════════════════════════════════════════════════════════╝
```

### Default Stack (FREE — zero cost)

| Layer | Technology | License | Cost |
|-------|-----------|---------|------|
| Frontend (Web) | Next.js 14 | MIT | FREE |
| Frontend (Mobile) | Flutter | BSD | FREE |
| Backend API | FastAPI | MIT | FREE |
| Database | PostgreSQL 16 | PostgreSQL License | FREE |
| Vector DB | Qdrant | Apache 2.0 | FREE (self-hosted) |
| Cache | Redis 7 | BSD 3-Clause | FREE |
| Search | Meilisearch | MIT | FREE |
| **LLM** | **vLLM + Mistral 7B** | **Apache 2.0** | **FREE (self-hosted, zero restrictions)** |
| Embeddings | nomic-embed-text v1.5 | Apache 2.0 | FREE |
| Re-ranker | ms-marco-MiniLM-L-6-v2 | Apache 2.0 | FREE |
| Agent Framework | LangGraph | MIT | FREE |
| Auth | Self-hosted JWT | MIT | FREE |
| Maps | OpenStreetMap + Nominatim | ODbL | FREE |
| Weather | Open-Meteo | Open Source | FREE (no API key needed) |
| Routing | OSRM | BSD 2-Clause | FREE |
| Monitoring | Grafana + Prometheus | Apache 2.0 / AGPL | FREE |
| CI/CD | GitHub Actions | Free for OSS | FREE |

### Optional Paid Enhancements (NOT required)

| Enhancement | What it adds | Cost |
|---|---|---|
| Claude API (Anthropic) | Better reasoning for complex comparisons | ~$3-15 per 1M tokens |
| Groq API | Faster fallback inference | Free tier (30 req/min) |
| Llama 3.1 8B (instead of Mistral) | Slightly better quality | Free, but 700M MAU limit |
| Google Maps API | Premium maps/routing | $200 free credit/month |
| Supabase Auth | Social login (Google, GitHub) | Free tier (50K MAU) |

**None of the above are required.** The system works 100% on the free stack.

---

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- NVIDIA GPU (for self-hosted vLLM — RTX 3060+ or equivalent)

### 1. Clone the repository

```bash
git clone https://github.com/HemantBK/RideShala.git
cd RideShala
```

### 2. Set up environment variables

```bash
cp .env.example .env
```

The defaults work out of the box — no API keys needed:

```env
# Everything is pre-configured for FREE self-hosted operation.
# Default LLM: Mistral 7B via vLLM (Apache 2.0, zero cost)
# Default maps: OpenStreetMap (free)
# Default weather: Open-Meteo (free, no API key)
# Default auth: Self-hosted JWT (free)

# Only change the database password:
DATABASE_URL=postgresql://rideshala:your-secure-password@localhost:5432/rideshala
```

### 3. Start all services with Docker Compose

```bash
cd infra

# Start with GPU (recommended — runs free self-hosted AI):
docker compose --profile gpu up -d

# With monitoring dashboards:
docker compose --profile monitoring up -d
```

### 4. Verify services are running

```bash
# API health check
curl http://localhost:8080/health/ready

# Expected: {"status": "ready", "checks": {...}}
```

### 5. Access the app

| Service | URL |
|---------|-----|
| Web App | http://localhost:3000 |
| API Docs (Swagger) | http://localhost:8080/docs |
| API Health | http://localhost:8080/health/ready |
| Qdrant Dashboard | http://localhost:6333/dashboard |
| Meilisearch | http://localhost:7700 |
| Grafana | http://localhost:3001 (admin/admin) |
| Prometheus | http://localhost:9090 |

### Development without Docker

```bash
# Backend
cd services/api
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8080

# Frontend
cd apps/web
npm install
npm run dev
```

---

## API Endpoints

### Chat (AI Advisor)

```bash
# Streaming chat (Server-Sent Events)
curl -N -X POST http://localhost:8080/api/v1/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"message": "Best bike for Bangalore commute under 2L?"}'

# Non-streaming chat
curl -X POST http://localhost:8080/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Compare Meteor 350 vs CB350"}'
```

### Bike Specs

```bash
# List bikes with filters
curl "http://localhost:8080/api/v1/specs?brand=royal_enfield&max_price=300000"

# Get single bike
curl http://localhost:8080/api/v1/specs/meteor-350
```

### Comparison

```bash
# AI-powered comparison with reasoning
curl -X POST http://localhost:8080/api/v1/compare \
  -H "Content-Type: application/json" \
  -d '{"bikes": ["Meteor 350", "CB350"], "user_height_cm": 170, "user_city": "Bangalore"}'

# Total Cost of Ownership
curl -X POST http://localhost:8080/api/v1/compare/tco \
  -H "Content-Type: application/json" \
  -d '{"bikes": ["Meteor 350", "CB350"], "user_city": "Bangalore"}'
```

### Reviews

```bash
# Submit a review (requires consent)
curl -X POST http://localhost:8080/api/v1/reviews \
  -H "Content-Type: application/json" \
  -d '{
    "bike_model": "Meteor 350",
    "text": "Owned for 18 months, 12000 km. Incredibly comfortable for city riding...",
    "rating": 4.2,
    "mileage_kpl": 33.5,
    "ownership_months": 18,
    "consent_granted": true,
    "is_original": true
  }'

# Get reviews for a bike
curl "http://localhost:8080/api/v1/reviews/meteor-350?sort=recent&limit=20"
```

### Health Checks

```bash
curl http://localhost:8080/health/live     # Process alive?
curl http://localhost:8080/health/ready    # Can serve traffic?
curl http://localhost:8080/health/startup  # Initialization done?
```

---

## Legal Compliance

RideShala is built with a **legal-first** approach. Every data point has a documented legal source.

### What we DO (100% legal)

- Use OEM-published specs (facts are not copyrightable)
- Display manufacturer prices (publicly advertised)
- Use OEM press images (released for editorial use)
- Collect original user reviews (with explicit consent + CC BY-SA license)
- Use government data (RTO rates, fuel prices, insurance tariffs)
- Use free APIs within their terms (OpenWeather, Google Maps, API Ninjas)

### What we NEVER do

- Scrape BikeWale, BikeDekho, ZigWheels, or any competitor
- Copy reviews, images, or content from other platforms
- Collect personal data without explicit consent
- Use copyrighted content without permission
- Track users or sell data to third parties

### Compliance

| Law | Status |
|-----|--------|
| Copyright Act 1957 (India) | Compliant — only facts + user-contributed content |
| IT Act 2000 (India) | Compliant — no unauthorized access, no scraping |
| DPDP Act 2023 (India) | Compliant — consent-first, purpose limitation, right to delete |
| Consumer Protection Act 2019 | Compliant — no misleading claims, clear disclaimers |
| GDPR (if EU users access) | Compliant — same protections as DPDP |

### Cross-Border Data Disclosure

When using Claude API, user query text (not personal data) is sent to Anthropic's US servers. Users can opt out via "Local AI Only" mode, which routes all queries through self-hosted vLLM. Full details in the Privacy Policy.

See [RideShala_Legal_OpenSource_Plan_v2.md](RideShala_Legal_OpenSource_Plan_v2.md) for the complete legal analysis.

---

## Licensing

| Component | License | What it means |
|-----------|---------|--------------|
| **Source code** | [MIT License](LICENSE) | Free to use, modify, distribute — no restrictions |
| **Data (bulk download)** | [CC BY-SA 4.0](DATA_LICENSE) | Free to use with attribution, derivatives must be open |
| **Data (API responses)** | [CC BY 4.0](DATA_LICENSE) | Free to use in proprietary apps with attribution |
| **Third-party models** | [See THIRD_PARTY_LICENSES](THIRD_PARTY_LICENSES) | Llama 3.1 (Meta License), vLLM (Apache 2.0), etc. |

Attribution for API usage: `Data from RideShala (rideshala.in)`

---

## Security

### Reporting Vulnerabilities

If you discover a security vulnerability, please email **security@rideshala.in** instead of opening a public issue. We will respond within 48 hours.

### What we protect

- API keys are **never** committed to git (see `.env.example`)
- All user inputs are validated and sanitized (Pydantic + bleach)
- CORS whitelist (no wildcards in production)
- Rate limiting on all endpoints (Redis-backed)
- Circuit breakers on external services
- LLM prompt injection defense (system/user message separation)
- Dependency scanning in CI (`pip-audit` + `npm audit`)
- User passwords hashed via Supabase (bcrypt)
- Data encrypted at rest (AES-256) and in transit (TLS 1.3)

### Files that should NEVER be in git

| File/Pattern | Why |
|---|---|
| `.env`, `.env.local`, `.env.production` | Contains API keys and database passwords |
| `*.pem`, `*.key`, `*.cert` | SSL/TLS certificates and private keys |
| `credentials.json`, `service-account.json` | Cloud provider credentials |
| `models/*.safetensors`, `*.gguf` | Large ML model files (downloaded at runtime) |
| `pgdata/`, `qdrant_data/`, `redis_data/` | Local database volumes |
| `node_modules/`, `__pycache__/`, `.venv/` | Dependencies (installed from lockfiles) |
| `.claude/` | Claude Code session files |

All of these are covered by our `.gitignore`. The only env file in git is `.env.example` with dummy placeholder values.

---

## Roadmap

| Phase | Timeline | Key Deliverables | Status |
|-------|----------|-----------------|--------|
| **1 — Foundation** | Weeks 1-6 | Monorepo, PostgreSQL, FastAPI, 30 bikes seeded, Next.js UI, auth, Docker, CI/CD | In Progress |
| **2 — AI Layer** | Weeks 7-12 | vLLM server, Qdrant, hybrid RAG, LangGraph agents, Claude integration, streaming chat | Planned |
| **3 — Full Agents** | Weeks 13-18 | Comparison/safety/finance agents, user reviews, moderation, mileage tracking, load testing | Planned |
| **4 — Scale** | Weeks 19-24 | Flutter app, ride planner, fine-tuning, A/B testing, Hindi support, K8s, public API | Planned |

---

## Contributing

We welcome contributions of all kinds:

| Type | How |
|------|-----|
| Add bike specs | Submit a PR with OEM source link |
| Write reviews | Use the in-app review form (coming soon) |
| Code | Fork, branch, PR (see below) |
| Bug reports | Open a GitHub Issue |
| Translations | Help us support Hindi, Kannada, Tamil |
| Spec verification | Cross-check existing data against OEM sites |

### Development workflow

```bash
# 1. Fork and clone
git clone https://github.com/HemantBK/RideShala.git
cd RideShala

# 2. Create a feature branch
git checkout -b feature/your-feature-name

# 3. Set up environment
cp .env.example .env
cd infra && docker compose up -d

# 4. Make your changes and test
cd services/api
pip install -r requirements.txt
pytest

# 5. Commit and push
git add -A
git commit -m "feat: add your feature description"
git push origin feature/your-feature-name

# 6. Open a Pull Request on GitHub
```

### Code standards

- Python: Formatted with `ruff`, type hints required
- TypeScript: ESLint + Prettier
- Commits: Conventional commits (`feat:`, `fix:`, `docs:`, `refactor:`)
- PRs: Must include description, test plan, and pass CI

---

## Community

- **GitHub Discussions**: Questions, ideas, show-and-tell
- **GitHub Issues**: Bug reports, feature requests
- **Contributing Guide**: [CONTRIBUTING.md](.github/CONTRIBUTING.md)
- **Code of Conduct**: [CODE_OF_CONDUCT.md](.github/CODE_OF_CONDUCT.md)

### Governance

Inspired by the Apache Foundation model:

```
Users → Contributors → Committers → PMC (Project Management Committee)
```

All decisions are made transparently via GitHub Discussions. No single person or company controls RideShala.

---

## Acknowledgements

Built with Meta Llama 3.1, vLLM, Claude by Anthropic, LangGraph by LangChain, Qdrant, and many other open-source projects. See [THIRD_PARTY_LICENSES](THIRD_PARTY_LICENSES) for full attribution.

---

## FAQ

**Q: Is this really free?**
Yes. 100% free. MIT licensed code, Apache 2.0 licensed default model (Mistral 7B), CC BY-SA data. Self-hosted on your own hardware with zero API costs, zero SaaS dependencies, zero vendor lock-in. Optional paid enhancements (Claude API, Groq) exist but are never required.

**Q: Do you scrape BikeWale or BikeDekho?**
Never. Every data point comes from OEM websites (manual entry), government sources, free APIs, or our own users. See the legal compliance section.

**Q: Can I use this for my own project?**
Yes. The code is MIT licensed (do anything). The data API is CC BY 4.0 (use freely, just credit us). Bulk data downloads are CC BY-SA 4.0 (derivatives must be open).

**Q: Why not just use ChatGPT/Gemini for bike advice?**
ChatGPT/Gemini hallucinate specs, use outdated training data, and can't cite sources. RideShala is grounded in real, verified data from our own database — every claim has a source citation.

**Q: Do I need a GPU to run this?**
Yes, for the default free setup — an NVIDIA GPU (RTX 3060+ / 8GB+ VRAM) runs Mistral 7B via vLLM at zero cost. If you don't have a GPU, you can optionally use Groq's free tier (30 req/min, no cost) or Claude API (paid) as cloud alternatives.

**Q: What about my privacy?**
No tracking, no ads, no data selling. Anonymous mode available. You can delete all your data with one click. DPDP Act 2023 compliant. Code is open source — audit it yourself.

---

*Built with confidence. Every byte is legal, every feature is open source.*

*License: [MIT](LICENSE) | Data: [CC BY-SA 4.0 / CC BY 4.0](DATA_LICENSE) | Third-party: [THIRD_PARTY_LICENSES](THIRD_PARTY_LICENSES)*
