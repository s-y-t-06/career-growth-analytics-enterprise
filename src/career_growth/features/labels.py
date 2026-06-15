"""具有严格时间边界的流失标签构建。"""

import pandas as pd

from career_growth import config


def build_labels(users: pd.DataFrame, events: pd.DataFrame) -> pd.DataFrame:
    """从事件中构建流失标签。

    标签仅来源于 event_source 为 "user_action" 且
    落在注册后第 8 天至第 21 天（含）之间的事件。

    只包含拥有完整 21 天观察窗口的用户。
    数据生成器通过不生成晚于 `END_DATE - 21 天` 的注册来确保这一点。
    """
    user_actions = events[events["event_source"] == "user_action"].copy()

    records = []
    for _, user in users.iterrows():
        signup = user["signup_timestamp"]
        cutoff = signup + pd.Timedelta(days=config.PREDICTION_CUTOFF_DAY)
        label_start = signup + pd.Timedelta(days=config.LABEL_WINDOW_START_DAY)
        label_end = signup + pd.Timedelta(days=config.LABEL_WINDOW_END_DAY)

        user_events = user_actions[user_actions["user_id"] == user["user_id"]]
        active_in_label = user_events[
            (user_events["event_timestamp"] >= label_start)
            & (user_events["event_timestamp"] <= label_end)
        ]
        is_churned = int(len(active_in_label) == 0)

        records.append(
            {
                "user_id": user["user_id"],
                "signup_timestamp": signup,
                "prediction_cutoff": cutoff,
                "label_start": label_start,
                "label_end": label_end,
                "is_churned": is_churned,
            }
        )

    return pd.DataFrame(records)


def check_label_leakage(features: pd.DataFrame, labels: pd.DataFrame) -> list[str]:
    """如果特征列包含未来信息，则返回泄漏问题列表。"""
    forbidden_prefixes = ("future_", "post_", "label_")
    forbidden_columns = {
        "last_active_date",
        "days_since_last_active",
        "current_stage",
        "churn_risk_score",
        "conversion_propensity_score",
        "is_churned",
    }
    issues = []
    for col in features.columns:
        if col.startswith(forbidden_prefixes) or col in forbidden_columns:
            issues.append(f"Feature column contains potential leakage: {col}")
    return issues
