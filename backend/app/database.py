"""SQLite database utilities for the enterprise backend."""

import sqlite3
from pathlib import Path

from backend.app import config


def get_connection(db_path: Path | None = None) -> sqlite3.Connection:
    """Return a SQLite connection with row factory enabled."""
    path = db_path or config.APP_DB_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_database(db_path: Path | None = None) -> None:
    """Create backend tables if they do not exist."""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            signup_timestamp TEXT NOT NULL,
            acquisition_channel TEXT,
            country TEXT,
            device_type TEXT,
            user_intent_level TEXT,
            career_stage TEXT,
            marketing_consent INTEGER,
            language TEXT,
            timezone TEXT
        );

        CREATE TABLE IF NOT EXISTS events (
            event_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            session_id TEXT,
            event_name TEXT,
            event_timestamp TEXT NOT NULL,
            event_properties TEXT,
            page_name TEXT,
            platform TEXT,
            event_source TEXT,
            experiment_id TEXT,
            variant_id TEXT
        );

        CREATE TABLE IF NOT EXISTS experiment_assignments (
            assignment_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            experiment_id TEXT NOT NULL,
            variant_id TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS interventions (
            intervention_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            intervention_type TEXT,
            channel TEXT,
            sent_timestamp TEXT,
            reason TEXT
        );

        CREATE TABLE IF NOT EXISTS labels (
            user_id TEXT PRIMARY KEY,
            is_churned INTEGER,
            label_start TEXT,
            label_end TEXT
        );

        CREATE TABLE IF NOT EXISTS model_scores (
            user_id TEXT PRIMARY KEY,
            predicted_risk REAL,
            predicted_class INTEGER,
            action_name TEXT,
            channel TEXT,
            reason TEXT
        );

        CREATE TABLE IF NOT EXISTS nba_recommendations (
            user_id TEXT PRIMARY KEY,
            action_name TEXT,
            channel TEXT,
            reason TEXT,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        );
        """
    )
    conn.commit()
    conn.close()
