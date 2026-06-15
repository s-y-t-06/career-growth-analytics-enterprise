"""Synthetic intervention log generation.

Interventions are secondary data and do not influence the churn label or the
main event stream. They are generated after the fact to simulate a simple
campaign system.
"""

import uuid
from datetime import timedelta

import numpy as np
import pandas as pd

from career_growth import config


def generate_interventions(
    users: pd.DataFrame,
    events: pd.DataFrame,
    rng: np.random.Generator,
) -> pd.DataFrame:
    """Generate a small set of marketing interventions based on user behavior."""
    if events.empty:
        return pd.DataFrame(
            columns=[
                "message_id",
                "user_id",
                "action_name",
                "channel",
                "send_time",
                "open_time",
                "click_time",
                "conversion_time",
                "experiment_id",
            ]
        )

    user_actions = events[events["event_source"] == "user_action"].copy()
    user_last_action = user_actions.groupby("user_id")["event_timestamp"].max()

    rows = []
    for _, user in users.iterrows():
        user_id = user["user_id"]
        signup = user["signup_timestamp"]
        consent = user["marketing_consent"]

        user_events = events[events["user_id"] == user_id]
        active_days_first_week = set()
        for _, ev in user_events.iterrows():
            if ev["event_source"] == "user_action":
                day = (ev["event_timestamp"] - signup).days
                if 0 <= day <= config.PREDICTION_CUTOFF_DAY:
                    active_days_first_week.add(day)

        onboarding_done = (
            user_events[
                (user_events["event_name"] == "onboarding_complete")
                & (user_events["event_source"] == "user_action")
            ].shape[0]
            > 0
        )

        # Rule 1: incomplete onboarding by day 3 -> prompt to complete onboarding.
        if not onboarding_done:
            send_time = signup + timedelta(days=3)
            channel = "in_app" if not consent else rng.choice(["email", "push", "in_app"])
            rows.append(
                _build_intervention_row(
                    user_id,
                    "complete_onboarding",
                    channel,
                    send_time,
                    rng,
                )
            )
            continue

        # Rule 2: low engagement in first week -> reengagement.
        if len(active_days_first_week) <= 1:
            send_time = signup + timedelta(days=7)
            channel = "in_app" if not consent else rng.choice(["email", "push"])
            rows.append(
                _build_intervention_row(
                    user_id,
                    "send_reengagement_message",
                    channel,
                    send_time,
                    rng,
                )
            )

        # Rule 3: churned users after label window -> win-back.
        last_action = user_last_action.get(user_id)
        label_end = signup + timedelta(days=config.LABEL_WINDOW_END_DAY)
        if last_action is not None and last_action <= label_end:
            send_time = label_end + timedelta(days=1)
            channel = "in_app" if not consent else rng.choice(["email", "push"])
            rows.append(
                _build_intervention_row(
                    user_id,
                    "send_reengagement_message",
                    channel,
                    send_time,
                    rng,
                )
            )

    return pd.DataFrame(rows)


def _build_intervention_row(
    user_id: str,
    action_name: str,
    channel: str,
    send_time: pd.Timestamp,
    rng: np.random.Generator,
) -> dict:
    message_id = str(uuid.uuid4())
    open_time = send_time + timedelta(hours=int(rng.integers(1, 48))) if rng.random() < 0.20 else None
    click_time = (
        open_time + timedelta(minutes=int(rng.integers(1, 60)))
        if open_time is not None and rng.random() < 0.30
        else None
    )
    conversion_time = (
        click_time + timedelta(hours=int(rng.integers(1, 24)))
        if click_time is not None and rng.random() < 0.10
        else None
    )
    return {
        "message_id": message_id,
        "user_id": user_id,
        "action_name": action_name,
        "channel": channel,
        "send_time": send_time,
        "open_time": open_time,
        "click_time": click_time,
        "conversion_time": conversion_time,
        "experiment_id": None,
    }
