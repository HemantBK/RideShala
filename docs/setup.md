# Development Setup

## Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- NVIDIA GPU (optional — for local vLLM inference)

## Option 1: Docker Compose (recommended)

```bash
# Clone
git clone https://github.com/HemantBK/RideShala.git
cd RideShala

# Configure
cp .env.example .env
# Edit .env if needed (defaults work out of the box)

# Start all services
cd infra
docker compose up -d                      # Without GPU (uses API fallbacks)
docker compose --profile gpu up -d        # With GPU (runs vLLM locally)
docker compose --profile monitoring up -d # With Grafana + Prometheus
```

### Service URLs

| Service | URL |
|---------|-----|
| Web App | http://localhost:3000 |
| API (Swagger) | http://localhost:8080/docs |
| Health Check | http://localhost:8080/health/ready |
| Qdrant Dashboard | http://localhost:6333/dashboard |
| Meilisearch | http://localhost:7700 |
| Grafana | http://localhost:3001 (admin/admin) |
| Prometheus | http://localhost:9090 |
| PostgreSQL | localhost:5432 |
| Redis | localhost:6379 |

### Stop services

```bash
docker compose down           # Stop services (keep data)
docker compose down -v        # Stop services + delete all data
```

## Option 2: Manual Setup (without Docker)

### Backend

```bash
cd services/api
python -m venv .venv
source .venv/bin/activate     # Linux/Mac
# .venv\Scripts\activate      # Windows

pip install -r requirements.txt
```

Start required services (PostgreSQL, Redis, etc.) manually or via Docker:

```bash
cd infra
docker compose up -d postgres redis qdrant meilisearch
```

Run the API:

```bash
cd services/api
PYTHONPATH=. uvicorn app.main:app --reload --port 8080
```

### Frontend

```bash
cd apps/web
npm install
npm run dev
```

Open http://localhost:3000

## Initialize Data

After services are running, set up the databases:

```bash
# Seed PostgreSQL with 30 bikes
python data/seeds/seed_db.py

# Create Qdrant vector collection
python data/migrations/001_create_qdrant_collection.py

# Setup Meilisearch index
python data/migrations/002_setup_meilisearch.py

# Run Alembic migration (if using PostgreSQL directly)
cd services/api
alembic upgrade head
```

## Running Tests

```bash
cd services/api
PYTHONPATH=. pytest tests/ -v
```

## Running Linter

```bash
# From project root
ruff check packages/ services/
```

## Environment Variables

See `.env.example` for the full list. Key variables:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | Yes | (in docker-compose) | PostgreSQL connection string |
| `REDIS_URL` | Yes | (in docker-compose) | Redis connection string |
| `QDRANT_URL` | Yes | (in docker-compose) | Qdrant server URL |
| `VLLM_BASE_URL` | For AI features | (in docker-compose) | vLLM server URL |
| `VLLM_MODEL` | No | `mistralai/Mistral-7B-Instruct-v0.3` | LLM model name |
| `ANTHROPIC_API_KEY` | No | (not set) | Optional: Claude API for premium reasoning |
| `GROQ_API_KEY` | No | (not set) | Optional: Groq free tier fallback |

## Common Issues

**Port already in use:**
```bash
docker compose down  # Stop any running containers
```

**GPU not detected by vLLM:**
```bash
nvidia-smi           # Check GPU is available
docker compose --profile gpu up vllm  # Start only vLLM to see errors
```

**Tests fail with ModuleNotFoundError:**
```bash
cd services/api
PYTHONPATH=. pytest tests/  # Ensure PYTHONPATH is set
```
