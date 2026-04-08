# AI Pipeline

## LangGraph Agent Flow

Every user message goes through this pipeline:

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

### Agent Nodes

| Node | What it does | Data sources | LLM |
|------|-------------|-------------|-----|
| **classify_intent** | Detects intent + extracts bike names, user profile | None (LLM only) | vLLM |
| **research** | Queries real bike specs from DB + reviews via hybrid RAG, passes to LLM | PostgreSQL + Qdrant + Meilisearch | vLLM |
| **comparison** | Fetches real specs for each bike + reviews, generates reasoned trade-off analysis | PostgreSQL + Qdrant | vLLM |
| **safety** | Checks safety features from specs + appends hardcoded safety rules LLM cannot override | PostgreSQL + hardcoded rules | vLLM |
| **finance** | Real EMI/RTO/insurance/TCO calculations using published government rates | IRDAI tariffs, state RTO rates, IOCL fuel prices | vLLM |
| **ride_plan** | Full route planning: Nominatim geocoding, OSRM routing, Open-Meteo weather, fuel stop calculator from bike specs | OSRM + Open-Meteo + PostgreSQL | vLLM |
| **synthesize** | Combines agent outputs + source citations. Calls LLM for general chat when no agent ran | Agent outputs | vLLM (for general chat) |
| **guardrail** | Blocks unsafe recommendations (regex), adds financial disclaimers | Hardcoded rules | None |

### State Schema

```python
class RideShalaState(TypedDict):
    messages: list              # Conversation history
    intent: str                 # bike_search, compare, safety, tco, ride_plan, general_chat
    user_profile: dict | None   # height, city, budget, riding_style
    bikes_mentioned: list[str]  # Extracted bike names
    specs_data: dict | None     # From PostgreSQL
    reviews_data: list | None   # From Qdrant hybrid search
    research_result: str | None
    comparison_result: str | None
    safety_result: str | None
    finance_result: str | None
    ride_plan_result: str | None
    provider: str               # vllm, claude, groq
    sources: list[str]          # Citation list
    total_tokens: int
```

## LLM Provider Routing

The router picks the first available provider and falls back automatically on failure.

### Available Providers (all free except Claude)

| Provider | Model | Cost | Rate Limit | When to use |
|----------|-------|------|-----------|-------------|
| **vLLM** | Mistral 7B | FREE (self-hosted) | Unlimited | Have GPU |
| **Groq** | Llama 3.3 70B | FREE | 1,000 req/day | Best quality, no GPU |
| **Gemini** | Gemini 2.0 Flash | FREE | 1,000+ req/day | Google's model, good fallback |
| **HuggingFace** | Llama 3.1 8B | FREE | ~100 req/hr | Backup fallback |
| **Claude** | Sonnet | PAID (optional) | Pay-per-use | Premium reasoning |

### Fallback Chain

```
Request → LLM Router
              │
              ├── Groq available? ──► Use Groq (free, fastest)
              │
              ├── Groq down? ──► Circuit breaker opens
              │                    ├── Gemini key set? ──► Use Gemini (free)
              │                    ├── HuggingFace? ──► Use HF (free)
              │                    └── vLLM running? ──► Use vLLM (GPU)
              │
              └── All providers down? ──► Graceful error (RS-3001)
```

Each provider has an independent circuit breaker (native async, no Tornado dependency):
- Opens after 5 failures in 30 seconds
- Half-open probe every 60 seconds
- When open, auto-routes to next provider in chain

## Hybrid RAG Pipeline

Combines dense (semantic) and sparse (keyword) search for maximum retrieval quality.

```
Query: "Is Meteor 350 comfortable for long rides?"
    │
    ├──────────────────────────────────────────┐
    │                                          │
    ▼                                          ▼
┌─────────────────┐                 ┌─────────────────┐
│ DENSE SEARCH    │                 │ SPARSE SEARCH   │
│ (Qdrant)        │                 │ (Meilisearch)   │
│ nomic-embed-text│                 │ BM25 keywords   │
│ Returns: top 20 │                 │ Returns: top 20 │
└────────┬────────┘                 └────────┬────────┘
         │                                   │
         └──────────────┬────────────────────┘
                        ▼
              Reciprocal Rank Fusion (k=60)
                        │
                        ▼
              Cross-Encoder Re-ranking
              (ms-marco-MiniLM-L-6-v2)
                        │
                        ▼
              Top 10 results + source citations
```

**Why hybrid?** Dense search finds "great for long rides" when user asks about "comfort." Sparse search finds "Meteor 350 rear suspension stiff" by exact keyword match. Hybrid catches both.

## Prompt Engineering

Prompts are versioned as Python code in `packages/ai/prompts/system_base.py`:

- **PERSONA** — Base personality applied to all tasks
- **COMPARISON_PROMPT** — Structured comparison format with per-claim citations
- **SAFETY_PROMPT** — Hardcoded safety rules the LLM cannot override
- **FINANCE_PROMPT** — TCO calculation format with source requirements
- **RIDE_PLAN_PROMPT** — Route planning with fuel/weather/safety
- **INTENT_CLASSIFICATION_PROMPT** — JSON output schema for intent detection

## Guardrails

Hardcoded rules in `guardrail.py` that the LLM **cannot override**:

- Blocks any response suggesting removing/disabling ABS
- Blocks responses suggesting riding without proper gear
- Blocks responses encouraging speeding or illegal modifications
- Adds financial disclaimers to TCO/EMI calculations
- Always includes safety reminders in safety-related responses

## Cost Tracking

Every LLM call is logged:
- Provider, model, input/output tokens
- Feature that triggered the call (chat, comparison, safety, tco)
- Cost in USD (0.00 for vLLM and Groq free tier)

Tracked in `usage_logs` PostgreSQL table for monitoring dashboards.

## Embedding Pipeline

When a user submits a review and it passes moderation:

1. Review is saved to the JSON store (MVP) / PostgreSQL (production)
2. Review is pushed to Redis `embedding_queue`
3. Background worker (`packages/ai/rag/embeddings.py`) processes the queue:
   - Detects aspects in the review text (comfort, mileage, performance, etc.)
   - Chunks the review per aspect for better retrieval
   - Embeds chunks via vLLM embedding server (nomic-embed-text, free)
   - Upserts vectors to Qdrant `user_reviews` collection

Aspect detection keywords: comfort (seat, posture, back), mileage (fuel, kpl, tank), performance (power, speed, torque), build_quality (paint, rust, vibration), value (price, worth, money), service (dealer, maintenance, warranty).

## Review Moderation

Every submitted review passes through 4 automated checks before approval:

| Check | Method | What it catches |
|-------|--------|----------------|
| **Plagiarism** | Jaccard similarity (word sets) against existing reviews | Copy-pasted reviews, duplicates (threshold: 0.85) |
| **Toxicity** | Keyword matching against toxic word list | Hate speech, abuse, personal attacks |
| **Spam** | Regex patterns | Links, phone numbers, promotions, ads |
| **Quality** | Heuristics (length, caps ratio, repeated chars) | Low-effort reviews, ALL CAPS, "goooood bikeeeee" |

All checks are local Python logic — no paid moderation API needed.

## Evaluation (RAGAS)

Automated RAG quality evaluation using the RAGAS framework (Apache 2.0):

**Golden test set:** 49 curated Q&A pairs across 6 categories:
- `spec_lookup` — factual spec questions with exact answers
- `comparison` — multi-bike trade-off analysis
- `recommendation` — personalized bike suggestions
- `finance` — EMI, RTO, TCO calculations
- `safety` — safety feature checks, gear advice
- `ride_plan` — route planning with fuel/weather

**Target thresholds:**
| Metric | Target | What it measures |
|--------|--------|-----------------|
| Faithfulness | > 0.85 | Does the answer stick to retrieved data? |
| Answer Relevancy | > 0.80 | Does it actually answer the question? |
| Context Precision | > 0.75 | Are retrieved documents relevant? |
| Context Recall | > 0.70 | Did we retrieve all needed documents? |

Run evaluation: `python -m packages.ai.evaluation.ragas_eval`
