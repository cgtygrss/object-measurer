"""Tests for measurement API endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    """Test health check endpoint."""
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


@pytest.mark.asyncio
async def test_get_history_empty(client: AsyncClient, auth_headers: dict):
    """Test getting history with no measurements."""
    response = await client.get("/api/v1/measure/history", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["measurements"] == []
    assert data["total"] == 0


@pytest.mark.asyncio
async def test_get_history_unauthorized(client: AsyncClient):
    """Test history without auth."""
    response = await client.get("/api/v1/measure/history")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_session(client: AsyncClient, auth_headers: dict):
    """Test creating a calibration session."""
    response = await client.post(
        "/api/v1/measure/sessions",
        headers=auth_headers,
        json={
            "reference_object": "credit_card",
            "reference_width_mm": 85.6,
            "reference_height_mm": 53.98,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["reference_object"] == "credit_card"
    assert data["reference_width_mm"] == 85.6


@pytest.mark.asyncio
async def test_get_nonexistent_measurement(client: AsyncClient, auth_headers: dict):
    """Test getting a measurement that doesn't exist."""
    response = await client.get(
        "/api/v1/measure/00000000-0000-0000-0000-000000000000",
        headers=auth_headers,
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_nonexistent_measurement(client: AsyncClient, auth_headers: dict):
    """Test deleting a measurement that doesn't exist."""
    response = await client.delete(
        "/api/v1/measure/00000000-0000-0000-0000-000000000000",
        headers=auth_headers,
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_upload_invalid_file_type(client: AsyncClient, auth_headers: dict):
    """Test uploading a non-image file."""
    response = await client.post(
        "/api/v1/measure/upload",
        headers=auth_headers,
        files={"image": ("test.txt", b"not an image", "text/plain")},
        data={"reference_height_mm": "100"},
    )
    assert response.status_code == 400
    assert "JPEG, PNG" in response.json()["detail"]
