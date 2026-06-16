"""Tests for model-related endpoints."""

from fastapi.testclient import TestClient


def test_model_metrics(client: TestClient) -> None:
    """Model metrics endpoint must return selected model and test metrics."""
    response = client.get("/api/model/metrics")
    assert response.status_code == 200
    data = response.json()
    assert data["selected_model"] == "logistic_regression"
    assert "validation" in data
    assert "test" in data
    assert "confusion_matrix" in data


def test_model_subgroups(client: TestClient) -> None:
    """Subgroup endpoint must return evaluation groups."""
    response = client.get("/api/model/subgroups")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["groups"], list)
    assert len(data["groups"]) > 0
