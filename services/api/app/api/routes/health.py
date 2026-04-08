"""Health check endpoints for Kubernetes probes.

Performs real connectivity checks against all dependent services.
"""

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/live")
async def liveness():
    """Liveness probe — is the process running?"""
    return {"status": "alive"}


@router.get("/ready")
async def readiness(req: Request):
    """Readiness probe — can the service handle requests?

    Checks actual connectivity to PostgreSQL, Redis, Qdrant,
    and at least one LLM provider.
    """
    checks = {}

    # Check PostgreSQL
    db_pool = getattr(req.app.state, "db_pool", None)
    if db_pool:
        try:
            await db_pool.fetchval("SELECT 1")
            checks["postgresql"] = True
        except Exception:
            checks["postgresql"] = False
    else:
        checks["postgresql"] = False

    # Check Redis
    redis = getattr(req.app.state, "redis", None)
    if redis:
        try:
            await redis.ping()
            checks["redis"] = True
        except Exception:
            checks["redis"] = False
    else:
        checks["redis"] = False

    # Check Qdrant
    qdrant = getattr(req.app.state, "qdrant", None)
    if qdrant:
        try:
            await qdrant.get_collections()
            checks["qdrant"] = True
        except Exception:
            checks["qdrant"] = False
    else:
        checks["qdrant"] = False

    # Check LLM (at least one provider configured)
    llm_router = getattr(req.app.state, "llm_router", None)
    checks["llm_available"] = llm_router is not None and len(llm_router.providers) > 0

    # Check LangGraph
    checks["langgraph"] = getattr(req.app.state, "graph", None) is not None

    all_ok = all(checks.values())

    return JSONResponse(
        status_code=200 if all_ok else 503,
        content={
            "status": "ready" if all_ok else "degraded",
            "checks": checks,
            "providers": llm_router.get_status() if llm_router else {},
        },
    )


@router.get("/startup")
async def startup(req: Request):
    """Startup probe — has initialization completed?"""
    db_ok = getattr(req.app.state, "db_pool", None) is not None
    graph_ok = getattr(req.app.state, "graph", None) is not None

    return {
        "status": "started" if (db_ok or graph_ok) else "starting",
        "db_connected": db_ok,
        "graph_loaded": graph_ok,
    }
