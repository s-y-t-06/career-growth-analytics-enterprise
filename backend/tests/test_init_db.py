"""Tests for the database initialization script."""

from pathlib import Path

from backend.app.database import get_connection, init_database
from backend.app.services.data_service import seed_database


def test_init_and_seed(tmp_path: Path) -> None:
    """Database initialization and seeding must create expected tables."""
    db_path = tmp_path / "app.db"
    init_database(db_path)
    seed_database(db_path)

    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = {row["name"] for row in cursor.fetchall()}
    conn.close()

    expected = {
        "users",
        "events",
        "experiment_assignments",
        "interventions",
        "labels",
        "model_scores",
        "nba_recommendations",
    }
    assert expected.issubset(tables)
