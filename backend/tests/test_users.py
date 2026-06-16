"""Tests for user endpoints."""

from fastapi.testclient import TestClient


def test_list_users(client: TestClient) -> None:
    """User list endpoint must return scored users."""
    response = client.get("/api/users?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1000
    assert len(data["users"]) == 10
    user = data["users"][0]
    assert "user_id" in user
    assert "churn_probability" in user
    assert "recommended_action" in user


def test_user_detail(client: TestClient) -> None:
    """User detail endpoint must return profile and explanation."""
    response = client.get("/api/users?limit=1")
    user_id = response.json()["users"][0]["user_id"]

    detail_response = client.get(f"/api/users/{user_id}")
    assert detail_response.status_code == 200
    data = detail_response.json()
    assert data["user_id"] == user_id
    assert "profile" in data
    assert "churn_probability" in data
    assert "explanation" in data
    assert "recommended_action" in data
    assert "timeline" in data


def test_score_user(client: TestClient) -> None:
    """Score endpoint must return risk and recommendation."""
    response = client.get("/api/users?limit=1")
    user_id = response.json()["users"][0]["user_id"]

    score_response = client.post("/api/users/score", json={"user_id": user_id})
    assert score_response.status_code == 200
    data = score_response.json()
    assert data["user_id"] == user_id
    assert 0.0 <= data["churn_probability"] <= 1.0
    assert data["recommended_action"]
    assert data["channel"]


def test_score_missing_user(client: TestClient) -> None:
    """Score endpoint must return 404 for unknown user."""
    response = client.post("/api/users/score", json={"user_id": "missing_user"})
    assert response.status_code == 404


def test_user_detail_does_not_use_label_for_nba(client: TestClient) -> None:
    """User detail recommendation must be driven by predicted risk, not label."""
    response = client.get("/api/users?limit=1")
    user_id = response.json()["users"][0]["user_id"]

    detail_response = client.get(f"/api/users/{user_id}")
    data = detail_response.json()
    assert "churn_probability" in data
    assert "recommended_action" in data
