"""Tests for the health endpoint."""

from fastapi.testclient import TestClient


def test_health(client: TestClient) -> None:
    """Health endpoint must report backend and artifacts are ok."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["database"] == "ok"
    assert data["model"] == "ok"
    assert data["metrics"] == "ok"
