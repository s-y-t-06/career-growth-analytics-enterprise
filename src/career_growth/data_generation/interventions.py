"""合成干预日志生成。

干预是次要数据，不会影响流失标签或主事件流。
它们在标签计算完成后生成，以便挽回活动仅针对在标签定义下真正流失的用户。
"""

import uuid
from datetime import timedelta

import numpy as np
import pandas as pd

from career_growth import config


def generate_interventions(
    users: pd.DataFrame,
    events: pd.DataFrame,
    labels: pd.DataFrame,
    rng: np.random.Generator,
    seed: int = config.RANDOM_SEED,
) -> pd.DataFrame:
    """基于用户行为生成少量营销干预。

    Args:
        users: 用户 DataFrame（可以是不包含隐藏列的公开版本）。
        events: 事件 DataFrame。
        labels: 包含每个用户 ``is_churned`` 的标签 DataFrame。
        rng: 随机数生成器。
        seed: 用于确定性派生 ID 的生成种子。
    """
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

    churned_by_user = labels.set_index("user_id")["is_churned"].to_dict()
    user_actions = events[events["event_source"] == "user_action"].copy()

    rows = []
    message_counter = 0

    def next_message_id(user_id: str) -> str:
        nonlocal message_counter
        message_counter += 1
        return str(
            uuid.uuid5(
                uuid.NAMESPACE_OID,
                f"intervention-{seed}-{user_id}-{message_counter}",
            )
        )

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

        # 规则 1：第 3 天仍未完成新手引导 -> 提示完成新手引导。
        if not onboarding_done:
            send_time = signup + timedelta(days=3)
            channel = "in_app" if not consent else rng.choice(["email", "push", "in_app"])
            rows.append(
                _build_intervention_row(
                    next_message_id(user_id),
                    user_id,
                    "complete_onboarding",
                    channel,
                    send_time,
                    rng,
                )
            )
            continue

        # 规则 2：首周活跃度低 -> 再互动。
        if len(active_days_first_week) <= 1:
            send_time = signup + timedelta(days=7)
            channel = "in_app" if not consent else rng.choice(["email", "push"])
            rows.append(
                _build_intervention_row(
                    next_message_id(user_id),
                    user_id,
                    "send_reengagement_message",
                    channel,
                    send_time,
                    rng,
                )
            )
            continue

        # 规则 3：标签窗口后的流失用户 -> 挽回。
        # 使用官方流失标签，而不是宽松的最后行为启发式。
        if churned_by_user.get(user_id, 0) == 1:
            label_end = signup + timedelta(days=config.LABEL_WINDOW_END_DAY)
            send_time = label_end + timedelta(days=1)
            channel = "in_app" if not consent else rng.choice(["email", "push"])
            rows.append(
                _build_intervention_row(
                    next_message_id(user_id),
                    user_id,
                    "send_win_back",
                    channel,
                    send_time,
                    rng,
                )
            )

    return pd.DataFrame(rows)


def _build_intervention_row(
    message_id: str,
    user_id: str,
    action_name: str,
    channel: str,
    send_time: pd.Timestamp,
    rng: np.random.Generator,
) -> dict:
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
