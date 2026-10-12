"""Tests for MIRA FastAPI routes (health, info, safety verification, triage)."""

import pytest
from httpx import ASGITransport, AsyncClient
from src.api.app import create_app


@pytest.fixture
def test_app():
    """Initializes FastAPI test application instance."""
    return create_app()


@pytest.mark.asyncio
async def test_health_endpoint(test_app):
    """Verifies that /health reports healthy status across all subsystems."""
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["app_name"] == "MIRA"
        assert "Block 2" in data["current_block"]
        assert "brain" in data["subsystems"]
        assert "safety" in data["subsystems"]
        assert "knowledge" in data["subsystems"]
        assert "tools" in data["subsystems"]
        assert "character" in data["subsystems"]
        assert "voice" in data["subsystems"]


@pytest.mark.asyncio
async def test_info_endpoint(test_app):
    """Verifies that /api/v1/info accurately reflects product specifications."""
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/info")
        assert response.status_code == 200
        data = response.json()
        assert data["identity"]["name"] == "MIRA"
        assert data["identity"]["is_human"] is False
        assert data["identity"]["replaces_professionals"] is False
        assert data["canonical_introduction"] == "I'm MIRA, an AI healthcare assistant."
        assert len(data["architecture"]) == 3


@pytest.mark.asyncio
async def test_verify_safety_endpoint_safe(test_app):
    """Verifies that valid AI responses pass the safety check endpoint."""
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {"text": "I'm MIRA, an AI healthcare assistant. How can I help you today?"}
        response = await client.post("/api/v1/verify-safety", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["is_safe"] is True
        assert len(data["violations"]) == 0


@pytest.mark.asyncio
async def test_verify_safety_endpoint_violation(test_app):
    """Verifies that human-claiming text triggers safety violation."""
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {"text": "I am your human nurse today, don't worry."}
        response = await client.post("/api/v1/verify-safety", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["is_safe"] is False
        assert len(data["violations"]) > 0


@pytest.mark.asyncio
async def test_triage_evaluate_endpoint(test_app):
    """Verifies triage endpoint correctly processes symptoms."""
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {"symptoms_text": "I have sudden severe slurred speech and facial drooping"}
        response = await client.post("/api/v1/triage-evaluate", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["urgency"] == "emergency"
        assert data["requires_emergency_dispatch"] is True
