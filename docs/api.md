# API Reference

Base URL: `http://localhost:8080`
Interactive Swagger docs: `http://localhost:8080/docs`

## Chat (AI Advisor)

### POST /api/v1/chat/stream

Stream AI response via Server-Sent Events. Routes through LangGraph multi-agent system.

```bash
curl -N -X POST http://localhost:8080/api/v1/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"message": "Best bike for Bangalore commute under 2L?"}'
```

**Request:**
```json
{
  "message": "string (1-2000 chars, required)",
  "bike_models": ["string (optional, max 5)"],
  "session_id": "string (optional)"
}
```

**Response:** `text/event-stream`
```
data: {"type": "token", "content": "I recommend "}
data: {"type": "token", "content": "the Meteor 350 "}
data: {"type": "done", "sources": [...], "intent": "bike_search", "tokens_used": 523}
```

### POST /api/v1/chat

Non-streaming chat (returns full response at once).

```bash
curl -X POST http://localhost:8080/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Compare Meteor 350 vs CB350"}'
```

**Response:**
```json
{
  "response": "string",
  "sources": ["string"],
  "intent": "compare",
  "provider": "vllm",
  "tokens_used": 523
}
```

## Bike Specs

### GET /api/v1/specs

List bikes with optional filters. Returns real data from 30-bike seed database.

```bash
curl "http://localhost:8080/api/v1/specs?brand=Royal+Enfield&max_price=300000&limit=10"
```

**Query params:** `search`, `brand`, `min_price`, `max_price`, `category`, `limit` (1-100), `offset`

### GET /api/v1/specs/{bike_slug}

Get full specs for a single bike. Returns 404 if not found.

```bash
curl http://localhost:8080/api/v1/specs/royal-enfield-meteor-350
```

### GET /api/v1/specs/{bike_slug}/reviews/summary

Get AI-generated review summary for a bike.

```bash
curl http://localhost:8080/api/v1/specs/royal-enfield-meteor-350/reviews/summary
```

## Comparison

### POST /api/v1/compare

AI-powered bike comparison. Routes through LangGraph comparison agent, falls back to raw spec table if LLM unavailable.

```bash
curl -X POST http://localhost:8080/api/v1/compare \
  -H "Content-Type: application/json" \
  -d '{
    "bikes": ["Meteor 350", "CB350"],
    "user_height_cm": 170,
    "user_city": "Bangalore",
    "user_budget": 250000
  }'
```

**Request:**
```json
{
  "bikes": ["string (2-4 required)"],
  "user_height_cm": "int (100-220, optional)",
  "user_city": "string (optional)",
  "user_budget": "int (optional)"
}
```

### POST /api/v1/compare/tco

Total Cost of Ownership comparison using real financial calculators. Uses published RTO rates, IRDAI insurance tariffs, and IOCL fuel prices.

```bash
curl -X POST http://localhost:8080/api/v1/compare/tco \
  -H "Content-Type: application/json" \
  -d '{"bikes": ["Meteor 350", "CB350"], "user_city": "Karnataka"}'
```

**Response includes:** ex-showroom, RTO charges, insurance (year 1 + subsequent), EMI calculation, 5-year fuel cost, 5-year service cost, total TCO, monthly cost — with sources for every number.

## Reviews

### POST /api/v1/reviews

Submit a user review. Goes through moderation pipeline (plagiarism, toxicity, spam, quality checks). Approved reviews are queued for embedding.

```bash
curl -X POST http://localhost:8080/api/v1/reviews \
  -H "Content-Type: application/json" \
  -d '{
    "bike_model": "Meteor 350",
    "text": "Owned for 18 months, 12000 km. Very comfortable for city riding and weekend highway trips to Coorg. Mileage around 33 kpl in mixed riding.",
    "rating": 4.2,
    "mileage_kpl": 33.5,
    "ownership_months": 18,
    "consent_granted": true,
    "is_original": true
  }'
```

**Moderation checks:** plagiarism (Jaccard similarity), toxicity (keyword filter), spam (regex patterns), quality (length, caps, repeats). Review is rejected with specific reason if any check fails.

### GET /api/v1/reviews/{bike_model}

Get reviews for a bike. Returns avg rating, avg real-world mileage.

```bash
curl "http://localhost:8080/api/v1/reviews/meteor-350?sort=recent&limit=20"
```

## Mileage Tracking

### POST /api/v1/tracking/mileage

Log a fuel fill-up. Used to calculate real-world mileage from consecutive full-tank fills.

```bash
curl -X POST http://localhost:8080/api/v1/tracking/mileage \
  -H "Content-Type: application/json" \
  -d '{
    "bike_model": "Meteor 350",
    "odometer_km": 12500,
    "litres_filled": 11.2,
    "price_per_litre": 102.86,
    "city": "Bangalore",
    "is_full_tank": true
  }'
```

### GET /api/v1/tracking/mileage/{bike_model}

Get aggregated real-world mileage stats. Calculates kpl from consecutive full-tank entries.

```bash
curl http://localhost:8080/api/v1/tracking/mileage/meteor-350
```

**Response:**
```json
{
  "bike": "meteor-350",
  "avg_mileage_kpl": 33.2,
  "min_mileage_kpl": 28.5,
  "max_mileage_kpl": 38.1,
  "calculated_entries": 47,
  "source": "Calculated from 47 full-tank fill-ups on RideShala"
}
```

## Service Cost Tracking

### POST /api/v1/tracking/service

Log a service visit with cost and work done.

```bash
curl -X POST http://localhost:8080/api/v1/tracking/service \
  -H "Content-Type: application/json" \
  -d '{
    "bike_model": "Meteor 350",
    "odometer_km": 10000,
    "total_cost_inr": 3200,
    "service_type": "regular",
    "work_done": "Oil change, chain adjustment, brake check, air filter clean",
    "dealer_or_local": "dealer",
    "city": "Bangalore"
  }'
```

### GET /api/v1/tracking/service/{bike_model}

Get aggregated service cost stats — average, by type, dealer vs local.

```bash
curl http://localhost:8080/api/v1/tracking/service/meteor-350
```

## Community Spec Contributions

### POST /api/v1/contributions

Submit a spec correction. Requires OEM source URL.

```bash
curl -X POST http://localhost:8080/api/v1/contributions \
  -H "Content-Type: application/json" \
  -d '{
    "bike_slug": "royal-enfield-meteor-350",
    "field_name": "price_ex_showroom_inr",
    "old_value": "211000",
    "new_value": "215000",
    "source_url": "https://www.royalenfield.com/in/en/motorcycles/meteor-350/",
    "reason": "Price updated for 2026 model year"
  }'
```

**Editable fields:** engine_cc, power_bhp, torque_nm, cylinders, cooling, weight_kg, seat_height_mm, ground_clearance_mm, fuel_tank_litres, wheelbase_mm, abs_type, traction_control, riding_modes, price_ex_showroom_inr, gears, transmission_type, top_speed_kmph, mileage_claimed_kpl, year

### GET /api/v1/contributions

List contributions by status.

```bash
curl "http://localhost:8080/api/v1/contributions?status=pending&limit=20"
```

### GET /api/v1/contributions/{id}

Get a single contribution.

```bash
curl http://localhost:8080/api/v1/contributions/1
```

## Health Checks

```bash
curl http://localhost:8080/health/live      # Process alive?
curl http://localhost:8080/health/ready     # Real connectivity checks (DB, Redis, Qdrant, LLM)
curl http://localhost:8080/health/startup   # Initialization complete?
```

The `/health/ready` endpoint performs actual pings to PostgreSQL, Redis, Qdrant, and checks that at least one LLM provider is configured. Returns 503 if any check fails.

## Metrics

Prometheus metrics at `http://localhost:8080/metrics`:
- `http_request_duration_seconds` — request latency histogram
- `http_requests_total` — request count by endpoint and status

## Feedback

### POST /api/v1/feedback

Submit thumbs up/down feedback on an AI response. Used to track satisfaction and build fine-tuning dataset.

```bash
curl -X POST http://localhost:8080/api/v1/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Best bike for Bangalore commute under 2L?",
    "response": "I recommend the Pulsar NS200...",
    "rating": "thumbs_up",
    "intent": "bike_search",
    "provider": "vllm",
    "comment": "Very helpful recommendation!"
  }'
```

**Rating values:** `thumbs_up` or `thumbs_down`

### GET /api/v1/feedback/stats

Get aggregated feedback statistics — satisfaction percentage, breakdown by intent and provider, fine-tuning readiness.

```bash
curl http://localhost:8080/api/v1/feedback/stats
```

**Response:**
```json
{
  "total": 847,
  "thumbs_up": 712,
  "thumbs_down": 135,
  "satisfaction_pct": 84.1,
  "by_intent": {"bike_search": {"up": 300, "down": 40}, ...},
  "by_provider": {"vllm": {"up": 650, "down": 120}, ...},
  "fine_tuning_ready": false,
  "fine_tuning_progress": "847/10000 (8.5%)"
}
```

## Auto-Generated Docs

| URL | Description |
|-----|-------------|
| `http://localhost:8080/docs` | Swagger UI (interactive API explorer) |
| `http://localhost:8080/redoc` | ReDoc (alternative API docs) |
| `http://localhost:8080/openapi.json` | Raw OpenAPI 3.0 spec |
| `http://localhost:8080/metrics` | Prometheus metrics endpoint |
