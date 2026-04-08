"""Tests for health check endpoints."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_liveness():
    """Liveness probe should always return 200."""
    response = client.get("/health/live")
    assert response.status_code == 200
    assert response.json()["status"] == "alive"


def test_readiness():
    """Readiness probe should return service status."""
    response = client.get("/health/ready")
    # Returns 503 when DB/Redis not running (expected in CI), 200 when all healthy
    assert response.status_code in (200, 503)
    data = response.json()
    assert "status" in data
    assert "checks" in data


def test_startup():
    """Startup probe should confirm initialization."""
    response = client.get("/health/startup")
    assert response.status_code == 200
    # "starting" when DB not connected, "started" when fully initialized
    assert response.json()["status"] in ("started", "starting")
