"""Shared fixtures for backend tests."""

import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from backend.app.database import init_database
from backend.app.main import app
from backend.app.services.data_service import seed_database


@pytest.fixture
def test_db_path(tmp_path: Path) -> Path:
    """Return a temporary database path."""
    return tmp_path / "test.db"


@pytest.fixture
def client(tmp_path: Path) -> TestClient:
    """Return a FastAPI test client with a seeded temp database."""
    from backend.app import config

    original_db_path = config.APP_DB_PATH
    test_path = tmp_path / "test.db"
    config.APP_DB_PATH = test_path

    init_database(test_path)
    seed_database(test_path)

    with TestClient(app) as test_client:
        yield test_client

    config.APP_DB_PATH = original_db_path
