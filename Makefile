.PHONY: setup test lint typecheck docker-up docker-down seed migrate fmt clean

# ─── Development Setup ─────────────────────────────────
setup:
	cd services/api && pip install -r requirements.txt
	cd apps/web && npm install

# ─── Testing ───────────────────────────────────────────
test:
	cd services/api && PYTHONPATH=. pytest tests/ -v

test-cov:
	cd services/api && PYTHONPATH=. pytest tests/ -v --cov=app --cov-report=term-missing

# ─── Linting & Formatting ─────────────────────────────
lint:
	ruff check packages/ services/

fmt:
	ruff format packages/ services/

typecheck:
	mypy packages/ services/ --ignore-missing-imports

# ─── Docker ────────────────────────────────────────────
docker-up:
	cd infra && docker compose up -d

docker-gpu:
	cd infra && docker compose --profile gpu up -d

docker-down:
	cd infra && docker compose down

docker-clean:
	cd infra && docker compose down -v

# ─── Database ──────────────────────────────────────────
seed:
	python data/seeds/seed_db.py

migrate:
	cd services/api && alembic upgrade head

setup-qdrant:
	python data/migrations/001_create_qdrant_collection.py

setup-meili:
	python data/migrations/002_setup_meilisearch.py

init-db: migrate seed setup-qdrant setup-meili

# ─── Run ───────────────────────────────────────────────
run-api:
	cd services/api && PYTHONPATH=. uvicorn app.main:app --reload --port 8080

run-web:
	cd apps/web && npm run dev

# ─── Evaluation ────────────────────────────────────────
eval:
	python -m packages.ai.evaluation.ragas_eval

# ─── Load Test ─────────────────────────────────────────
loadtest:
	locust -f tests/load/locustfile.py --host http://localhost:8080

# ─── Clean ─────────────────────────────────────────────
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
