"""Tests for review submission API."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_submit_review_requires_consent():
    """Reviews without consent should be rejected."""
    response = client.post(
        "/api/v1/reviews",
        json={
            "bike_model": "Meteor 350",
            "text": "Great bike for daily commuting in Bangalore. Comfortable seat and smooth engine." * 2,
            "rating": 4.5,
            "consent_granted": False,
            "is_original": True,
        },
    )
    assert response.status_code == 422


def test_submit_review_requires_original():
    """Reviews must be confirmed as original content."""
    response = client.post(
        "/api/v1/reviews",
        json={
            "bike_model": "Meteor 350",
            "text": "Great bike for daily commuting in Bangalore. Comfortable seat and smooth engine." * 2,
            "rating": 4.5,
            "consent_granted": True,
            "is_original": False,
        },
    )
    assert response.status_code == 422


def test_submit_review_rejects_short_text():
    """Reviews under 50 characters should be rejected."""
    response = client.post(
        "/api/v1/reviews",
        json={
            "bike_model": "Meteor 350",
            "text": "Good bike",
            "rating": 4.5,
            "consent_granted": True,
            "is_original": True,
        },
    )
    assert response.status_code == 422


def test_submit_valid_review():
    """Valid review should be accepted for moderation."""
    response = client.post(
        "/api/v1/reviews",
        json={
            "bike_model": "Meteor 350",
            "text": "Owned for 18 months and ridden 12000 km. Incredibly comfortable for city riding and weekend trips to Coorg." * 2,
            "rating": 4.2,
            "mileage_kpl": 33.5,
            "ownership_months": 18,
            "consent_granted": True,
            "is_original": True,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "pending_moderation"


def test_submit_review_rejects_invalid_rating():
    """Rating outside 1-5 should be rejected."""
    response = client.post(
        "/api/v1/reviews",
        json={
            "bike_model": "Meteor 350",
            "text": "Excellent bike for daily use in the city. Very comfortable riding position." * 2,
            "rating": 6.0,
            "consent_granted": True,
            "is_original": True,
        },
    )
    assert response.status_code == 422
