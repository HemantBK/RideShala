# Deployment

## Development (Docker Compose)

See [setup.md](setup.md) for local development.

## Production (Single Server)

For MVP with under 1000 users, a single VPS with GPU is sufficient.

### Requirements

- VPS with NVIDIA GPU (RTX 4090 / A10G / A100)
- 24GB+ GPU VRAM (for Mistral 7B AWQ + embeddings)
- 16GB+ RAM
- 50GB+ SSD

### Docker Compose Production

```bash
# Clone and configure
git clone https://github.com/HemantBK/RideShala.git
cd RideShala
cp .env.example .env
# Edit .env with production values (strong passwords, real domain)

# Build and start
cd infra
docker compose --profile gpu --profile monitoring -f docker-compose.yml up -d

# Initialize databases (run once after first deploy)
cd ..
python data/seeds/seed_db.py
python data/migrations/001_create_qdrant_collection.py
python data/migrations/002_setup_meilisearch.py
```

### vLLM GPU Configuration

Single 24GB GPU memory budget:

| Component | Memory |
|-----------|--------|
| Mistral 7B AWQ 4-bit weights | ~6 GB |
| nomic-embed-text FP16 | ~0.5 GB |
| KV cache (managed by vLLM) | ~15 GB |
| Overhead | ~2.5 GB |

Supports ~20-30 concurrent inference requests.

### GPU Hosting Options (India-friendly)

| Provider | GPU | Cost/month |
|----------|-----|------------|
| vast.ai | RTX 4090 (24GB) | Rs 2,000-4,000 |
| RunPod | A10G (24GB) | Rs 4,000-6,000 |
| Lambda Cloud | A100 (40GB) | Rs 8,000-12,000 |

## Health Checks

```bash
curl http://your-server:8080/health/live     # Process running?
curl http://your-server:8080/health/ready    # Can serve traffic?
```

## Monitoring

With the `monitoring` Docker profile:

- **Grafana**: http://your-server:3001 (admin/admin)
- **Prometheus**: http://your-server:9090
- **Metrics endpoint**: http://your-server:8080/metrics

Key metrics:
- `http_request_duration_seconds` — latency p50/p95/p99
- `http_requests_total` — request count by endpoint
- LLM token usage via `usage_logs` PostgreSQL table

## Backups

```bash
# PostgreSQL daily backup
docker exec rideshala-postgres pg_dump -U rideshala rideshala > backup_$(date +%Y%m%d).sql

# Qdrant snapshot
curl -X POST http://localhost:6333/collections/user_reviews/snapshots
```

## SSL/TLS

Use a reverse proxy (Caddy or Nginx) in front of the API:

```bash
# Caddy (auto HTTPS)
caddy reverse-proxy --from rideshala.in --to localhost:8080
```
