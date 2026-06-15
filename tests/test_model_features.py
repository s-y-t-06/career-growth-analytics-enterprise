"""Tests for churn model feature engineering."""

import pandas as pd
import pytest

from career_growth.features.model_features import (
    ALL_FEATURE_COLUMNS,
    CATEGORICAL_FEATURES,
    NUMERIC_FEATURES,
    attach_labels,
    build_model_features,
    prepare_model_matrix,
)


@pytest.fixture
def sample_data(synthetic_data):
    """Return a small deterministic dataset for feature tests."""
    return {
        "users": synthetic_data["users"].head(200).copy(),
        "events": synthetic_data["events"].copy(),
        "experiment_assignments": synthetic_data["experiment_assignments"].copy(),
        "labels": synthetic_data["labels"].copy(),
    }


def test_build_model_features_columns(sample_data):
    """The feature matrix must contain the expected columns and no leakage columns."""
    features = build_model_features(
        sample_data["users"],
        sample_data["events"],
        sample_data["experiment_assignments"],
    )

    assert "user_id" in features.columns
    for col in ALL_FEATURE_COLUMNS:
        assert col in features.columns, f"Missing feature column: {col}"

    forbidden = {"last_active_date", "days_since_last_active", "is_churned", "future_"}
    for col in features.columns:
        for prefix in forbidden:
            assert not col.startswith(prefix), f"Forbidden column found: {col}"


def test_build_model_features_no_null_categoricals(sample_data):
    """Categorical features must be populated; numeric columns must be finite."""
    features = build_model_features(
        sample_data["users"],
        sample_data["events"],
        sample_data["experiment_assignments"],
    )

    for col in CATEGORICAL_FEATURES:
        assert features[col].notna().all(), f"Null values found in {col}"

    for col in NUMERIC_FEATURES:
        assert features[col].notna().all(), f"Null values found in {col}"
        assert pd.api.types.is_numeric_dtype(features[col]), f"{col} is not numeric"


def test_build_model_features_uses_pre_cutoff_events_only(sample_data):
    """Features must ignore events at or after the prediction cutoff."""
    users = sample_data["users"].head(10).copy()
    events = sample_data["events"].copy()

    features = build_model_features(users, events)

    for _, user in users.iterrows():
        cutoff = user["signup_timestamp"] + pd.Timedelta(days=7)
        user_events = events[
            (events["user_id"] == user["user_id"])
            & (events["event_timestamp"] >= cutoff)
        ]
        # No post-cutoff events should influence the feature values.
        row = features[features["user_id"] == user["user_id"]].iloc[0]
        assert row["num_user_actions"] == int(
            len(
                events[
                    (events["user_id"] == user["user_id"])
                    & (events["event_timestamp"] < cutoff)
                    & (events["event_source"] == "user_action")
                ]
            )
        )
        assert user_events.empty or row["num_user_actions"] >= 0


def test_variant_feature_joined(sample_data):
    """The onboarding variant feature must match experiment assignments."""
    features = build_model_features(
        sample_data["users"],
        sample_data["events"],
        sample_data["experiment_assignments"],
    )

    merged = features.merge(
        sample_data["experiment_assignments"][
            sample_data["experiment_assignments"]["experiment_id"] == "exp_onboarding_v1"
        ][["user_id", "variant_id"]],
        on="user_id",
        how="left",
    )
    assert (merged["onboarding_variant"] == merged["variant_id"].fillna("unknown")).all()


def test_attach_labels(sample_data):
    """Labels must be attached correctly and leakage must raise an error."""
    features = build_model_features(
        sample_data["users"],
        sample_data["events"],
        sample_data["experiment_assignments"],
    )
    labeled = attach_labels(features, sample_data["labels"])

    assert "is_churned" in labeled.columns
    assert labeled["is_churned"].isin({0, 1}).all()

    leaked_features = features.copy()
    leaked_features["future_events"] = 0
    with pytest.raises(ValueError, match="Feature leakage detected"):
        attach_labels(leaked_features, sample_data["labels"])


def test_prepare_model_matrix(sample_data):
    """The complete modeling matrix must preserve all users with labels."""
    matrix = prepare_model_matrix(
        sample_data["users"],
        sample_data["events"],
        sample_data["labels"],
        sample_data["experiment_assignments"],
    )

    expected_users = set(sample_data["users"]["user_id"]) & set(
        sample_data["labels"]["user_id"]
    )
    assert set(matrix["user_id"]) == expected_users
    assert "is_churned" in matrix.columns
