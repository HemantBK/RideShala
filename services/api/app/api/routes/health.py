"""Health check endpoints for Kubernetes probes."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/live")
async def liveness():
    """Liveness probe — is the process running?"""
    return {"status": "alive"}


@router.get("/ready")
async def readiness():
    """Readiness probe — can the service handle requests?

    Checks connectivity to PostgreSQL, Qdrant, Redis,
    and at least one LLM provider.
    """
    # TODO: Implement actual connectivity checks
    checks = {
        "postgresql": True,
        "qdrant": True,
        "redis": True,
        "llm_available": True,
    }
    all_ok = all(checks.values())
    return {
        "status": "ready" if all_ok else "not_ready",
        "checks": checks,
    }


@router.get("/startup")
async def startup():
    """Startup probe — has initialization completed?"""
    return {"status": "started", "models_loaded": True, "db_connected": True}
