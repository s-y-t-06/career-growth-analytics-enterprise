"""Tests for the NBA router."""

from fastapi.testclient import TestClient


def test_nba_recommend(client: TestClient) -> None:
    """NBA recommend endpoint must return a recommendation."""
    response = client.get("/api/users?limit=1")
    user_id = response.json()["users"][0]["user_id"]

    nba_response = client.post("/api/nba/recommend", json={"user_id": user_id})
    assert nba_response.status_code == 200
    data = nba_response.json()
    assert data["user_id"] == user_id
    assert data["action_name"]
    assert data["channel"]
    assert data["reason"]


def test_nba_examples(client: TestClient) -> None:
    """NBA examples endpoint must return recommendations."""
    response = client.get("/api/nba/examples?n=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data["examples"]) <= 5
