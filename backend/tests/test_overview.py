"""Tests for the overview endpoint."""

from fastapi.testclient import TestClient


def test_overview(client: TestClient) -> None:
    """Overview endpoint must return KPIs and model metrics."""
    response = client.get("/api/overview")
    assert response.status_code == 200
    data = response.json()
    assert data["users"] == 1000
    assert 0.0 <= data["churn_rate"] <= 1.0
    assert 0.0 <= data["d1_retention"] <= 1.0
    assert 0.0 <= data["d7_retention"] <= 1.0
    assert 0.0 <= data["d14_retention"] <= 1.0
    assert data["selected_model"] == "logistic_regression"
    assert 0.0 <= data["test_pr_auc"] <= 1.0
    assert 0.0 <= data["test_roc_auc"] <= 1.0
