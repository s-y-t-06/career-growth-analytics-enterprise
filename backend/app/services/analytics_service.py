"""Analytics services for overview, funnel, retention, and experiment APIs."""

import json
from pathlib import Path

import pandas as pd

from backend.app import config
from backend.app.services.data_service import (
    load_events,
    load_experiment_assignments,
    load_labels,
    load_metrics,
    load_users,
)
from career_growth.analytics.experiments import analyze_experiment
from career_growth.analytics.funnel import compute_funnel
from career_growth.analytics.retention import (
    compute_cohort_retention,
    compute_day_retention,
)


def get_overview() -> dict:
    """Return high-level platform and model overview."""
    users = load_users()
    events = load_events()
    labels = load_labels()
    metrics = load_metrics()

    churn_rate = float(labels["is_churned"].mean()) if not labels.empty else 0.0
    d1 = float(compute_day_retention(users, events, 1)["retention_rate"].iloc[0])
    d7 = float(compute_day_retention(users, events, 7)["retention_rate"].iloc[0])
    d14 = float(compute_day_retention(users, events, 14)["retention_rate"].iloc[0])
    test_metrics = metrics.get("test", {})

    return {
        "users": len(users),
        "events": len(events),
        "churn_rate": churn_rate,
        "d1_retention": d1,
        "d7_retention": d7,
        "d14_retention": d14,
        "selected_model": metrics.get("selected_model", "unknown"),
        "test_pr_auc": test_metrics.get("pr_auc", 0.0),
        "test_roc_auc": test_metrics.get("roc_auc", 0.0),
        "test_f1": test_metrics.get("f1_score", 0.0),
        "test_brier": test_metrics.get("brier_score", 0.0),
    }


def get_funnel() -> list[dict]:
    """Return the core user lifecycle funnel."""
    users = load_users()
    events = load_events()
    funnel_df = compute_funnel(users, events)
    return funnel_df.to_dict(orient="records")


def get_retention() -> dict:
    """Return day retention and cohort retention."""
    users = load_users()
    events = load_events()

    d1 = float(compute_day_retention(users, events, 1)["retention_rate"].iloc[0])
    d7 = float(compute_day_retention(users, events, 7)["retention_rate"].iloc[0])
    d14 = float(compute_day_retention(users, events, 14)["retention_rate"].iloc[0])

    cohort_df = compute_cohort_retention(
        users, events, days=[1, 7, 14], cohort_col="signup_week"
    )
    cohorts = cohort_df.to_dict(orient="records")

    return {
        "d1_retention": d1,
        "d7_retention": d7,
        "d14_retention": d14,
        "cohorts": cohorts,
    }


def get_experiment(experiment_id: str = "exp_onboarding_v1") -> dict:
    """Return A/B experiment analysis."""
    users = load_users()
    events = load_events()
    assignments = load_experiment_assignments()
    return analyze_experiment(users, events, assignments, experiment_id)
