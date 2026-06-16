"""Tests for the funnel endpoint."""

from fastapi.testclient import TestClient


def test_funnel(client: TestClient) -> None:
    """Funnel endpoint must return ordered steps."""
    response = client.get("/api/funnel")
    assert response.status_code == 200
    data = response.json()
    steps = data["steps"]
    assert len(steps) > 0
    assert steps[0]["step"] == "signup"
    assert steps[0]["users"] == 1000
    for step in steps:
        assert "step" in step
        assert "users" in step
        assert "conversion_rate" in step
        assert "drop_off_rate" in step
