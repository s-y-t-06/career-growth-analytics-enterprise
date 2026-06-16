"""Next Best Action services."""

import pandas as pd

from backend.app.services.data_service import load_events, load_users
from backend.app.services.model_service import score_single_user
from career_growth.decisions.next_best_action import recommend_next_action


def get_nba_for_user(user_id: str) -> dict:
    """Return a Next Best Action recommendation for a user.

    The recommendation is driven by the model score and user state, never by
    the true churn label.
    """
    return score_single_user(user_id)


def get_nba_examples(n: int = 10) -> list[dict]:
    """Return example NBA recommendations across the risk spectrum."""
    users = load_users()
    records = []
    for user_id in users["user_id"].head(n):
        try:
            rec = score_single_user(user_id)
            records.append(rec)
        except Exception:
            continue
    return records
