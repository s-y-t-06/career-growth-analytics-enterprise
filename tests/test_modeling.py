"""Tests for churn model training, evaluation, and explainability."""

import numpy as np
import pandas as pd
import pytest

from career_growth.features.model_features import prepare_model_matrix
from career_growth.modeling.evaluate import compute_metrics, select_threshold
from career_growth.modeling.explain import (
    compute_permutation_importance,
    extract_feature_names,
    extract_logistic_coefficients,
)
from career_growth.modeling.pipeline import (
    build_hist_gradient_boosting_pipeline,
    build_logistic_regression_pipeline,
)
from career_growth.modeling.split import chronological_split, split_users_and_labels
from career_growth.modeling.train import train_and_select_model


@pytest.fixture
def model_matrix(synthetic_data):
    """Return a modeling matrix for the shared synthetic dataset."""
    return prepare_model_matrix(
        synthetic_data["users"],
        synthetic_data["events"],
        synthetic_data["labels"],
        synthetic_data["experiment_assignments"],
    )


def test_chronological_split_order_and_disjoint(tmp_path):
    """Chronological split must preserve time order and produce disjoint sets."""
    df = pd.DataFrame(
        {
            "user_id": [f"u{i}" for i in range(10)],
            "signup_timestamp": pd.date_range("2026-01-01", periods=10, freq="D"),
        }
    )
    train, val, test = chronological_split(df, train_frac=0.6, val_frac=0.2)

    assert len(train) == 6
    assert len(val) == 2
    assert len(test) == 2
    assert set(train["user_id"]).isdisjoint(set(val["user_id"]))
    assert set(train["user_id"]).isdisjoint(set(test["user_id"]))
    assert set(val["user_id"]).isdisjoint(set(test["user_id"]))
    assert train["signup_timestamp"].max() <= val["signup_timestamp"].min()
    assert val["signup_timestamp"].max() <= test["signup_timestamp"].min()


def test_split_users_and_labels(synthetic_data):
    """User and label splits must be consistent and chronological."""
    users = synthetic_data["users"]
    labels = synthetic_data["labels"]

    train_u, val_u, test_u, train_l, val_l, test_l = split_users_and_labels(
        users, labels
    )

    assert set(train_l["user_id"]) == set(train_u["user_id"])
    assert set(val_l["user_id"]) == set(val_u["user_id"])
    assert set(test_l["user_id"]) == set(test_u["user_id"])
    assert train_u["signup_timestamp"].max() <= val_u["signup_timestamp"].min()
    assert val_u["signup_timestamp"].max() <= test_u["signup_timestamp"].min()


def test_logistic_regression_pipeline(model_matrix):
    """The logistic regression pipeline must fit and predict probabilities."""
    feature_cols = [c for c in model_matrix.columns if c not in {"user_id", "signup_timestamp", "is_churned"}]
    X = model_matrix[feature_cols]
    y = model_matrix["is_churned"].to_numpy()

    pipeline = build_logistic_regression_pipeline(random_state=42)
    pipeline.fit(X, y)
    prob = pipeline.predict_proba(X)[:, 1]

    assert prob.shape == (len(model_matrix),)
    assert np.all((prob >= 0.0) & (prob <= 1.0))


def test_hist_gradient_boosting_pipeline(model_matrix):
    """The gradient boosting pipeline must fit and predict probabilities."""
    feature_cols = [c for c in model_matrix.columns if c not in {"user_id", "signup_timestamp", "is_churned"}]
    X = model_matrix[feature_cols]
    y = model_matrix["is_churned"].to_numpy()

    pipeline = build_hist_gradient_boosting_pipeline(random_state=42)
    pipeline.fit(X, y)
    prob = pipeline.predict_proba(X)[:, 1]

    assert prob.shape == (len(model_matrix),)
    assert np.all((prob >= 0.0) & (prob <= 1.0))


def test_threshold_selection(model_matrix):
    """Threshold selection must return a value in [0, 1]."""
    feature_cols = [c for c in model_matrix.columns if c not in {"user_id", "signup_timestamp", "is_churned"}]
    X = model_matrix[feature_cols]
    y = model_matrix["is_churned"].to_numpy()

    pipeline = build_logistic_regression_pipeline(random_state=42)
    pipeline.fit(X, y)
    prob = pipeline.predict_proba(X)[:, 1]

    for criterion in ["f1", "precision", "recall", "f2", "youden"]:
        threshold = select_threshold(y, prob, criterion=criterion)
        assert 0.0 <= threshold <= 1.0


def test_train_and_select_model(model_matrix):
    """The training harness must select a model and produce validation/test metrics."""
    train_df, val_df, test_df = chronological_split(
        model_matrix, train_frac=0.6, val_frac=0.2
    )

    result = train_and_select_model(
        train_df,
        val_df,
        test_df,
        threshold_criterion="f1",
        random_state=42,
    )

    assert result.model_name in {"logistic_regression", "hist_gradient_boosting"}
    assert 0.0 <= result.threshold <= 1.0
    assert set(result.val_metrics.keys()) >= {
        "pr_auc",
        "roc_auc",
        "log_loss",
        "precision",
        "recall",
        "f1_score",
        "accuracy",
    }
    assert set(result.test_metrics.keys()) >= {
        "pr_auc",
        "roc_auc",
        "log_loss",
        "precision",
        "recall",
        "f1_score",
        "accuracy",
    }
    assert len(result.feature_columns) > 0


def test_logistic_coefficients(model_matrix):
    """Logistic regression coefficients must match the preprocessor output dimension."""
    feature_cols = [c for c in model_matrix.columns if c not in {"user_id", "signup_timestamp", "is_churned"}]
    X = model_matrix[feature_cols]
    y = model_matrix["is_churned"].to_numpy()

    pipeline = build_logistic_regression_pipeline(random_state=42)
    pipeline.fit(X, y)

    names = extract_feature_names(pipeline)
    coef_df = extract_logistic_coefficients(pipeline)

    assert len(names) == len(coef_df)
    assert "feature" in coef_df.columns and "coefficient" in coef_df.columns


def test_permutation_importance(model_matrix):
    """Permutation importance must return non-negative importance scores."""
    feature_cols = [c for c in model_matrix.columns if c not in {"user_id", "signup_timestamp", "is_churned"}]
    train_df, val_df, _ = chronological_split(
        model_matrix, train_frac=0.6, val_frac=0.2
    )

    pipeline = build_logistic_regression_pipeline(random_state=42)
    pipeline.fit(train_df[feature_cols], train_df["is_churned"].to_numpy())

    importance = compute_permutation_importance(
        pipeline,
        val_df[feature_cols],
        val_df["is_churned"].to_numpy(),
        n_repeats=3,
        random_state=42,
    )

    assert len(importance) == len(feature_cols)
    assert importance["importance_mean"].max() >= 0.0


def test_metrics_computed_at_selected_threshold(model_matrix):
    """Metrics must reflect the selected threshold rather than the default 0.5."""
    train_df, val_df, test_df = chronological_split(
        model_matrix, train_frac=0.6, val_frac=0.2
    )

    result = train_and_select_model(
        train_df,
        val_df,
        test_df,
        threshold_criterion="f1",
        random_state=42,
    )

    y_test = test_df["is_churned"].to_numpy()
    recomputed = compute_metrics(y_test, result.test_probabilities, result.threshold)
    assert pytest.approx(result.test_metrics["f1_score"], rel=1e-6) == recomputed["f1_score"]
    assert pytest.approx(result.test_metrics["precision"], rel=1e-6) == recomputed["precision"]
    assert pytest.approx(result.test_metrics["recall"], rel=1e-6) == recomputed["recall"]
