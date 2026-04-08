"""RideShala FastAPI application entry point."""

import os
import time
from contextlib import asynccontextmanager
from pathlib import Path
from uuid import uuid4

import structlog
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from prometheus_client import Counter, Histogram, make_asgi_app

from app.api.routes import (
    chat,
    compare,
    contributions,
    feedback,
    health,
    privacy,
    reviews,
    ride_plan,
    specs,
    tracking,
)

# Load .env from project root
_env_path = Path(__file__).resolve().parents[3] / ".env"
load_dotenv(_env_path if _env_path.exists() else None)

logger = structlog.get_logger()

# ─── Prometheus Metrics ─────────────────────────────────
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
    ["method", "endpoint", "status"],
)
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"],
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown."""
    logger.info("rideshala_starting", env=os.getenv("APP_ENV", "development"))

    import asyncpg

    try:
        db_url = os.getenv("DATABASE_URL", "postgresql://rideshala:rideshala@localhost:5432/rideshala")
        app.state.db_pool = await asyncpg.create_pool(db_url, min_size=2, max_size=10)
        logger.info("database_connected", url=db_url.split("@")[-1])
    except Exception as e:
        logger.warning("database_connection_failed", error=str(e))
        app.state.db_pool = None

    try:
        import redis.asyncio as aioredis

        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        app.state.redis = aioredis.from_url(redis_url, decode_responses=True)
        await app.state.redis.ping()
        logger.info("redis_connected")
    except Exception as e:
        logger.warning("redis_connection_failed", error=str(e))
        app.state.redis = None

    try:
        from packages.ai.llm.router import LLMRouter

        app.state.llm_router = LLMRouter()
        providers = list(app.state.llm_router.providers.keys())
        logger.info("llm_router_initialized", providers=providers)
    except Exception as e:
        logger.warning("llm_router_init_failed", error=str(e))
        app.state.llm_router = None

    try:
        from qdrant_client import AsyncQdrantClient

        qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
        app.state.qdrant = AsyncQdrantClient(url=qdrant_url)
        logger.info("qdrant_connected", url=qdrant_url)
    except Exception as e:
        logger.warning("qdrant_connection_failed", error=str(e))
        app.state.qdrant = None

    try:
        from packages.ai.agents.graph import rideshala_graph

        app.state.graph = rideshala_graph
        logger.info("langgraph_initialized")
    except Exception as e:
        logger.warning("langgraph_init_failed", error=str(e))
        app.state.graph = None

    logger.info("rideshala_started_successfully")

    yield

    if app.state.db_pool:
        await app.state.db_pool.close()
    if app.state.redis:
        await app.state.redis.close()

    logger.info("rideshala_shut_down")


app = FastAPI(
    title="RideShala API",
    description="Open-source AI-powered motorcycle comparison for Indian riders",
    version="0.1.0",
    lifespan=lifespan,
)

cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
if "*" in cors_origins and os.getenv("APP_ENV") == "production":
    logger.error("CORS_ORIGINS cannot be '*' in production. Set specific domains.")
    cors_origins = []
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

# Only expose Prometheus metrics in non-production environments
if os.getenv("APP_ENV") != "production":
    metrics_app = make_asgi_app()
    app.mount("/metrics", metrics_app)

app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])
app.include_router(specs.router, prefix="/api/v1/specs", tags=["specs"])
app.include_router(compare.router, prefix="/api/v1/compare", tags=["compare"])
app.include_router(reviews.router, prefix="/api/v1/reviews", tags=["reviews"])
app.include_router(tracking.router, prefix="/api/v1/tracking", tags=["tracking"])
app.include_router(contributions.router, prefix="/api/v1/contributions", tags=["contributions"])
app.include_router(feedback.router, prefix="/api/v1/feedback", tags=["feedback"])
app.include_router(privacy.router, prefix="/api/v1/privacy", tags=["privacy"])
app.include_router(ride_plan.router, prefix="/api/v1/ride-plan", tags=["ride-plan"])


@app.middleware("http")
async def observability_middleware(request: Request, call_next):
    """Add request_id, structured logging, and metrics."""
    request_id = str(uuid4())
    structlog.contextvars.bind_contextvars(request_id=request_id)

    start = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start

    status = str(response.status_code)
    endpoint = request.url.path

    REQUEST_LATENCY.labels(method=request.method, endpoint=endpoint, status=status).observe(duration)
    REQUEST_COUNT.labels(method=request.method, endpoint=endpoint, status=status).inc()

    logger.info(
        "request_completed",
        method=request.method,
        path=endpoint,
        status=response.status_code,
        duration_ms=round(duration * 1000, 2),
    )

    response.headers["X-Request-ID"] = request_id
    return response


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(
        "unhandled_exception",
        error_code="RS-9001",
        error=str(exc),
        error_type=type(exc).__name__,
        path=request.url.path,
        method=request.method,
    )
    return JSONResponse(
        status_code=500,
        content={
            "error_code": "RS-9001",
            "message": "Something went wrong. Please try again.",
        },
    )
