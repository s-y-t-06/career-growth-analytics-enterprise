"""Model scoring and explainability services."""

import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline

from backend.app import config
from backend.app.services.data_service import (
    load_events,
    load_experiment_assignments,
    load_model_metadata,
    load_users,
)
from career_growth.decisions.next_best_action import recommend_next_action
from career_growth.features.model_features import build_model_features


_model: Pipeline | None = None
_model_metadata: dict | None = None
_feature_schema: dict | None = None


def get_model() -> Pipeline:
    """Return the cached trained model."""
    global _model
    if _model is None:
        _model = joblib.load(config.MODEL_PATH)
    return _model


def get_model_metadata() -> dict:
    """Return cached model metadata."""
    global _model_metadata
    if _model_metadata is None:
        with open(config.MODEL_METADATA_PATH, "r", encoding="utf-8") as f:
            _model_metadata = json.load(f)
    return _model_metadata


def get_feature_schema() -> dict:
    """Return cached feature schema."""
    global _feature_schema
    if _feature_schema is None:
        with open(config.FEATURE_SCHEMA_PATH, "r", encoding="utf-8") as f:
            _feature_schema = json.load(f)
    return _feature_schema


def _threshold() -> float:
    """Return the model operating threshold."""
    return float(get_model_metadata().get("selected_threshold", 0.5))


def _feature_columns() -> list[str]:
    """Return ordered feature columns used by the model."""
    return get_model_metadata().get("feature_columns", [])


def score_single_user(user_id: str) -> dict:
    """Score a single user and return risk + NBA recommendation."""
    users = load_users()
    events = load_events()
    assignments = load_experiment_assignments()

    user_row = users[users["user_id"] == user_id]
    if user_row.empty:
        raise ValueError(f"User {user_id} not found")

    user = user_row.iloc[0]
    user_events = events[events["user_id"] == user_id].copy()
    user_events["event_timestamp"] = pd.to_datetime(user_events["event_timestamp"])

    user_df = pd.DataFrame([user])
    user_df["signup_timestamp"] = pd.to_datetime(user_df["signup_timestamp"])

    features = build_model_features(user_df, user_events, assignments)
    feature_cols = _feature_columns()
    missing = set(feature_cols) - set(features.columns)
    if missing:
        raise ValueError(f"Missing features: {missing}")

    model = get_model()
    prob = float(model.predict_proba(features[feature_cols])[:, 1][0])
    predicted_class = int(prob >= _threshold())

    rec = recommend_next_action(
        user,
        user_events,
        cutoff=None,
        churn_risk_score=prob,
    )

    return {
        "user_id": user_id,
        "churn_probability": prob,
        "predicted_class": predicted_class,
        "recommended_action": rec["action_name"],
        "channel": rec["channel"],
        "reason": rec["reason"],
    }


def score_all_users() -> pd.DataFrame:
    """Score all users in the sample and return a DataFrame."""
    users = load_users()
    events = load_events()
    assignments = load_experiment_assignments()

    users_copy = users.copy()
    users_copy["signup_timestamp"] = pd.to_datetime(users_copy["signup_timestamp"])
    events_copy = events.copy()
    events_copy["event_timestamp"] = pd.to_datetime(events_copy["event_timestamp"])

    features = build_model_features(users_copy, events_copy, assignments)
    feature_cols = _feature_columns()
    missing = set(feature_cols) - set(features.columns)
    if missing:
        raise ValueError(f"Missing features: {missing}")

    model = get_model()
    probs = model.predict_proba(features[feature_cols])[:, 1]
    threshold = _threshold()

    records = []
    for idx, user in users_copy.reset_index(drop=True).iterrows():
        prob = float(probs[idx])
        rec = recommend_next_action(
            user,
            events_copy,
            cutoff=None,
            churn_risk_score=prob,
        )
        records.append(
            {
                "user_id": user["user_id"],
                "predicted_risk": prob,
                "predicted_class": int(prob >= threshold),
                "action_name": rec["action_name"],
                "channel": rec["channel"],
                "reason": rec["reason"],
            }
        )

    return pd.DataFrame(records)


def explain_user(user_id: str, top_n: int = 5) -> list[dict]:
    """Return a simple feature-based explanation for a single user.

    For logistic regression, the explanation uses coefficient * feature value
    after one-hot encoding. For tree-based models, it falls back to the top
    raw features by deviation from the population mean.
    """
    users = load_users()
    events = load_events()
    assignments = load_experiment_assignments()

    user_row = users[users["user_id"] == user_id]
    if user_row.empty:
        raise ValueError(f"User {user_id} not found")

    user_df = user_row.copy()
    user_df["signup_timestamp"] = pd.to_datetime(user_df["signup_timestamp"])
    events_copy = events.copy()
    events_copy["event_timestamp"] = pd.to_datetime(events_copy["event_timestamp"])

    features = build_model_features(user_df, events_copy, assignments)
    feature_cols = _feature_columns()
    feature_matrix = features[feature_cols].reset_index(drop=True)

    model = get_model()
    model_name = get_model_metadata().get("model_name", "")

    if model_name == "logistic_regression":
        preprocessor = model.named_steps.get("preprocessor")
        classifier = model.named_steps.get("classifier")
        if preprocessor is None or classifier is None:
            return []
        transformed = preprocessor.transform(feature_matrix)
        if hasattr(transformed, "toarray"):
            transformed = transformed.toarray()
        transformed = np.asarray(transformed)[0]
        coef = classifier.coef_[0]
        feature_names = preprocessor.get_feature_names_out()
        contributions = transformed * coef
        top_indices = np.argsort(np.abs(contributions))[-top_n:][::-1]
        return [
            {
                "feature": str(feature_names[i]),
                "contribution": float(contributions[i]),
            }
            for i in top_indices
        ]

    # Fallback: numeric features ranked by deviation from population mean.
    numeric_cols = get_feature_schema().get("numeric_features", [])
    available = [c for c in numeric_cols if c in features.columns]
    if not available:
        return []

    population = build_model_features(users, events_copy, assignments)
    user_values = features[available].iloc[0]
    means = population[available].mean()
    stds = population[available].std().replace(0, np.nan)
    deviations = ((user_values - means) / stds).abs().fillna(0)
    top = deviations.sort_values(ascending=False).head(top_n)
    return [
        {"feature": col, "contribution": float(deviations[col])}
        for col in top.index
    ]
