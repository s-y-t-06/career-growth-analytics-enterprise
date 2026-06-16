"""Data loading and persistence services."""

import json
import sqlite3
from pathlib import Path

import joblib
import pandas as pd
from sklearn.pipeline import Pipeline

from backend.app import config
from backend.app.database import get_connection


def load_csv(path: Path) -> pd.DataFrame:
    """Load a CSV file or return an empty DataFrame if missing."""
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def load_users() -> pd.DataFrame:
    """Load users from sample CSV."""
    df = load_csv(config.USERS_CSV)
    if not df.empty:
        df["signup_timestamp"] = pd.to_datetime(df["signup_timestamp"])
    return df


def load_events() -> pd.DataFrame:
    """Load events from sample CSV."""
    df = load_csv(config.EVENTS_CSV)
    if not df.empty:
        df["event_timestamp"] = pd.to_datetime(df["event_timestamp"])
    return df


def load_experiment_assignments() -> pd.DataFrame:
    """Load experiment assignments from sample CSV."""
    return load_csv(config.EXPERIMENT_ASSIGNMENTS_CSV)


def load_interventions() -> pd.DataFrame:
    """Load interventions from sample CSV."""
    df = load_csv(config.INTERVENTIONS_CSV)
    if not df.empty:
        if "sent_timestamp" in df.columns:
            df["sent_timestamp"] = pd.to_datetime(df["sent_timestamp"])
        elif "send_time" in df.columns:
            df["send_time"] = pd.to_datetime(df["send_time"])
    return df


def load_labels() -> pd.DataFrame:
    """Load churn labels from processed CSV."""
    df = load_csv(config.LABELS_CSV)
    if not df.empty:
        for col in ["label_start", "label_end"]:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col])
    return df


def load_model() -> Pipeline:
    """Load the trained churn model artifact."""
    return joblib.load(config.MODEL_PATH)


def load_metrics() -> dict:
    """Load model metrics artifact."""
    with open(config.METRICS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_model_metadata() -> dict:
    """Load model metadata artifact."""
    with open(config.MODEL_METADATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_feature_schema() -> dict:
    """Load feature schema artifact."""
    with open(config.FEATURE_SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_subgroup_metrics() -> list[dict]:
    """Load subgroup metrics artifact."""
    if not config.SUBGROUP_METRICS_PATH.exists():
        return []
    with open(config.SUBGROUP_METRICS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_user_explanations() -> list[dict]:
    """Load user explanations artifact."""
    if not config.USER_EXPLANATIONS_PATH.exists():
        return []
    with open(config.USER_EXPLANATIONS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_nba_examples() -> list[dict]:
    """Load NBA examples artifact."""
    if not config.NBA_EXAMPLES_PATH.exists():
        return []
    with open(config.NBA_EXAMPLES_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def seed_database(db_path: Path | None = None) -> None:
    """Populate the SQLite database from CSV files and artifacts."""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    users = load_users()
    events = load_events()
    assignments = load_experiment_assignments()
    interventions = load_interventions()
    labels = load_labels()

    _insert_users(cursor, users)
    _insert_events(cursor, events)
    _insert_assignments(cursor, assignments)
    _insert_interventions(cursor, interventions)
    _insert_labels(cursor, labels)

    conn.commit()
    conn.close()


def _insert_users(cursor: sqlite3.Cursor, users: pd.DataFrame) -> None:
    """Insert users into the database."""
    if users.empty:
        return
    rows = [
        (
            row["user_id"],
            row["signup_timestamp"].isoformat(),
            row.get("acquisition_channel"),
            row.get("country"),
            row.get("device_type"),
            row.get("user_intent_level"),
            row.get("career_stage"),
            int(bool(row.get("marketing_consent"))),
            row.get("language"),
            row.get("timezone"),
        )
        for _, row in users.iterrows()
    ]
    cursor.executemany(
        """
        INSERT OR REPLACE INTO users
        (user_id, signup_timestamp, acquisition_channel, country, device_type,
         user_intent_level, career_stage, marketing_consent, language, timezone)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        rows,
    )


def _insert_events(cursor: sqlite3.Cursor, events: pd.DataFrame) -> None:
    """Insert events into the database."""
    if events.empty:
        return
    rows = [
        (
            row["event_id"],
            row["user_id"],
            row.get("session_id"),
            row.get("event_name"),
            row["event_timestamp"].isoformat(),
            row.get("event_properties"),
            row.get("page_name"),
            row.get("platform"),
            row.get("event_source"),
            row.get("experiment_id"),
            row.get("variant_id"),
        )
        for _, row in events.iterrows()
    ]
    cursor.executemany(
        """
        INSERT OR REPLACE INTO events
        (event_id, user_id, session_id, event_name, event_timestamp,
         event_properties, page_name, platform, event_source, experiment_id, variant_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        rows,
    )


def _insert_assignments(cursor: sqlite3.Cursor, assignments: pd.DataFrame) -> None:
    """Insert experiment assignments into the database."""
    if assignments.empty:
        return
    rows = [
        (
            row.get("assignment_id", f"{row['user_id']}_{row['experiment_id']}"),
            row["user_id"],
            row["experiment_id"],
            row["variant_id"],
        )
        for _, row in assignments.iterrows()
    ]
    cursor.executemany(
        """
        INSERT OR REPLACE INTO experiment_assignments
        (assignment_id, user_id, experiment_id, variant_id)
        VALUES (?, ?, ?, ?)
        """,
        rows,
    )


def _insert_interventions(cursor: sqlite3.Cursor, interventions: pd.DataFrame) -> None:
    """Insert interventions into the database."""
    if interventions.empty:
        return
    rows = []
    for _, row in interventions.iterrows():
        ts = row.get("sent_timestamp") if "sent_timestamp" in row else row.get("send_time")
        intervention_id = row.get("intervention_id") if "intervention_id" in row else row.get("message_id")
        intervention_type = row.get("intervention_type") if "intervention_type" in row else row.get("action_name")
        rows.append(
            (
                intervention_id,
                row["user_id"],
                intervention_type,
                row.get("channel"),
                ts.isoformat() if pd.notna(ts) else None,
                row.get("reason"),
            )
        )
    cursor.executemany(
        """
        INSERT OR REPLACE INTO interventions
        (intervention_id, user_id, intervention_type, channel, sent_timestamp, reason)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        rows,
    )


def _insert_labels(cursor: sqlite3.Cursor, labels: pd.DataFrame) -> None:
    """Insert labels into the database."""
    if labels.empty:
        return
    rows = [
        (
            row["user_id"],
            int(row["is_churned"]) if pd.notna(row.get("is_churned")) else None,
            row["label_start"].isoformat() if pd.notna(row.get("label_start")) else None,
            row["label_end"].isoformat() if pd.notna(row.get("label_end")) else None,
        )
        for _, row in labels.iterrows()
    ]
    cursor.executemany(
        """
        INSERT OR REPLACE INTO labels
        (user_id, is_churned, label_start, label_end)
        VALUES (?, ?, ?, ?)
        """,
        rows,
    )
