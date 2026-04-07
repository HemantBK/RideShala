"""Tests for chat API endpoints."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_chat_sync_returns_response():
    """Non-streaming chat should return a response object."""
    response = client.post(
        "/api/v1/chat",
        json={"message": "Best bike for Bangalore commute?"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "sources" in data


def test_chat_rejects_empty_message():
    """Empty messages should be rejected with 422."""
    response = client.post(
        "/api/v1/chat",
        json={"message": ""},
    )
    assert response.status_code == 422


def test_chat_rejects_too_long_message():
    """Messages over 2000 chars should be rejected."""
    long_message = "a" * 2001
    response = client.post(
        "/api/v1/chat",
        json={"message": long_message},
    )
    assert response.status_code == 422


def test_chat_sanitizes_html():
    """HTML tags in messages should be stripped."""
    response = client.post(
        "/api/v1/chat",
        json={"message": "<script>alert('xss')</script>Best bike?"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "<script>" not in data["response"]


def test_chat_stream_returns_sse():
    """Streaming endpoint should return SSE content type."""
    response = client.post(
        "/api/v1/chat/stream",
        json={"message": "Compare Meteor 350 vs CB350"},
    )
    assert response.status_code == 200
    assert "text/event-stream" in response.headers["content-type"]
