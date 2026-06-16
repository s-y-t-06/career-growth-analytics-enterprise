"""Tests for the retention endpoint."""

from fastapi.testclient import TestClient


def test_retention(client: TestClient) -> None:
    """Retention endpoint must return day retention and cohorts."""
    response = client.get("/api/retention")
    assert response.status_code == 200
    data = response.json()
    assert 0.0 <= data["d1_retention"] <= 1.0
    assert 0.0 <= data["d7_retention"] <= 1.0
    assert 0.0 <= data["d14_retention"] <= 1.0
    assert isinstance(data["cohorts"], list)
    assert len(data["cohorts"]) > 0
