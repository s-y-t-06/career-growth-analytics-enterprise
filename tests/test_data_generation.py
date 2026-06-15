"""Tests for the synthetic data generation pipeline."""

from career_growth import config
from career_growth.data_generation.generator import generate_all_data


def test_generation_reproducibility():
    data_a = generate_all_data(count=200, seed=123, output_dir="data_test_a")
    data_b = generate_all_data(count=200, seed=123, output_dir="data_test_b")

    assert list(data_a["users"]["user_id"]) == list(data_b["users"]["user_id"])
    assert data_a["events"].shape == data_b["events"].shape
    assert data_a["events"]["event_id"].tolist() == data_b["events"]["event_id"].tolist()


def test_users_schema_and_no_hidden_variables(synthetic_data):
    hidden_cols = [
        "intrinsic_engagement",
        "career_urgency",
        "product_fit",
        "notification_sensitivity",
        "intent_score",
        "career_stage_score",
        "device_score",
    ]
    for col in hidden_cols:
        assert col not in synthetic_data["users"].columns


def test_events_after_signup(synthetic_data):
    merged = synthetic_data["events"].merge(
        synthetic_data["users"][["user_id", "signup_timestamp"]], on="user_id"
    )
    assert (merged["event_timestamp"] >= merged["signup_timestamp"]).all()


def test_churn_rate_within_target(synthetic_data):
    churn_rate = synthetic_data["labels"]["is_churned"].mean()
    assert 0.25 <= churn_rate <= 0.45


def test_onboarding_treatment_effect_direction(synthetic_data):
    rates = (
        synthetic_data["experiment_assignments"]
        .groupby("variant_id")["is_converted"]
        .mean()
    )
    assert rates["personalized"] > rates["control"]
    assert rates["simplified"] > rates["control"]


def test_experiment_assignment_proportions(synthetic_data):
    counts = synthetic_data["experiment_assignments"]["variant_id"].value_counts(normalize=True)
    assert abs(counts["control"] - 0.40) < 0.05
    assert abs(counts["personalized"] - 0.30) < 0.05
    assert abs(counts["simplified"] - 0.30) < 0.05


def test_active_events_only_for_label(synthetic_data):
    churned_user = synthetic_data["labels"][synthetic_data["labels"]["is_churned"] == 1].iloc[0]
    label_start = churned_user["label_start"]
    label_end = churned_user["label_end"]
    active_events = synthetic_data["events"][
        (synthetic_data["events"]["user_id"] == churned_user["user_id"])
        & (synthetic_data["events"]["event_source"] == "user_action")
        & (synthetic_data["events"]["event_timestamp"] >= label_start)
        & (synthetic_data["events"]["event_timestamp"] <= label_end)
    ]
    assert len(active_events) == 0
