"""Tests for comparison API endpoints."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_compare_requires_at_least_two_bikes():
    """Comparison needs minimum 2 bikes."""
    response = client.post(
        "/api/v1/compare",
        json={"bikes": ["Meteor 350"]},
    )
    assert response.status_code == 422


def test_compare_rejects_more_than_four_bikes():
    """Comparison limited to 4 bikes max."""
    response = client.post(
        "/api/v1/compare",
        json={"bikes": ["Meteor 350", "CB350", "Hunter 350", "Speed 400", "Dominar 400"]},
    )
    assert response.status_code == 422


def test_compare_valid_request():
    """Valid comparison request should return response."""
    response = client.post(
        "/api/v1/compare",
        json={"bikes": ["Meteor 350", "CB350"]},
    )
    assert response.status_code == 200
    data = response.json()
    assert "bikes" in data
    assert len(data["bikes"]) == 2


def test_compare_tco_endpoint():
    """TCO comparison endpoint should return response."""
    response = client.post(
        "/api/v1/compare/tco",
        json={"bikes": ["Meteor 350", "CB350"], "user_city": "Bangalore"},
    )
    assert response.status_code == 200
