"""Tests for the experiment endpoint."""

from fastapi.testclient import TestClient


def test_experiment(client: TestClient) -> None:
    """Experiment endpoint must return variant metrics."""
    response = client.get("/api/experiment")
    assert response.status_code == 200
    data = response.json()
    assert data["experiment_id"] == "exp_onboarding_v1"
    assert "sample_sizes" in data
    assert "srm_p_value" in data
    assert "metrics" in data
    assert "onboarding_completion_rate" in data["metrics"]
