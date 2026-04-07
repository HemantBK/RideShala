"""Tests for health check endpoints."""

from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_liveness():
    """Liveness probe should always return 200."""
    response = client.get("/health/live")
    assert response.status_code == 200
    assert response.json()["status"] == "alive"


def test_readiness():
    """Readiness probe should return service status."""
    response = client.get("/health/ready")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "checks" in data


def test_startup():
    """Startup probe should confirm initialization."""
    response = client.get("/health/startup")
    assert response.status_code == 200
    assert response.json()["status"] == "started"
