"""Tests for bike specs API endpoints."""

from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_list_bikes_returns_array():
    """List endpoint should return bikes array and total count."""
    response = client.get("/api/v1/specs")
    assert response.status_code == 200
    data = response.json()
    assert "bikes" in data
    assert "total" in data
    assert isinstance(data["bikes"], list)


def test_list_bikes_respects_limit():
    """Limit parameter should be respected."""
    response = client.get("/api/v1/specs?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert data["limit"] == 5


def test_list_bikes_rejects_invalid_limit():
    """Limit over 100 should be rejected."""
    response = client.get("/api/v1/specs?limit=500")
    assert response.status_code == 422


def test_get_single_bike():
    """Single bike endpoint should return bike slug."""
    response = client.get("/api/v1/specs/meteor-350")
    assert response.status_code == 200
