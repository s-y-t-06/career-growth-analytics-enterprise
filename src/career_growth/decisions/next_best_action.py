"""基于规则的下一个最佳动作（Next Best Action）引擎。

本模块实现了已批准的优先级规则。它不需要流失风险模型分数；
当提供分数时会使用分数，否则使用简单的活跃度启发式来识别高风险用户。
"""

from datetime import timedelta
from typing import Any

import pandas as pd

from career_growth import config


def compute_user_state(user_id: str, events: pd.DataFrame, cutoff: pd.Timestamp) -> dict[str, Any]:
    """计算截至截止时间戳的用户生命周期状态。"""
    user_events = events[
        (events["user_id"] == user_id)
        & (events["event_timestamp"] <= cutoff)
        & (events["event_source"] == "user_action")
    ].copy()

    event_names = set(user_events["event_name"])

    recent_start = cutoff - timedelta(days=2)
    recent_events = user_events[user_events["event_timestamp"] >= recent_start]
    recently_active = len(recent_events) > 0

    return {
        "onboarding_completed": "onboarding_complete" in event_names,
        "profile_completed": "profile_complete" in event_names,
        "resume_uploaded": "resume_upload" in event_names,
        "job_recommendation_viewed": "job_recommendation_view" in event_names,
        "job_saved": "job_save" in event_names,
        "growth_task_completed": "growth_task_complete" in event_names,
        "career_report_generated": "career_report_generate" in event_names,
        "recently_active": recently_active,
    }


def recommend_next_action(
    user: pd.Series,
    events: pd.DataFrame,
    cutoff: pd.Timestamp | None = None,
    churn_risk_score: float | None = None,
) -> dict[str, Any]:
    """返回单个用户的推荐下一个最佳动作。

    Args:
        user: 用户 DataFrame 中的一行。
        events: 事件 DataFrame。
        cutoff: 用于计算状态的截止时间戳。默认为注册后 7 天。
        churn_risk_score: 可选的模型分数；如果为 None，则使用近期不活跃作为判断。

    Returns:
        包含 action_name、channel 和 reason 的字典。
    """
    if cutoff is None:
        cutoff = user["signup_timestamp"] + timedelta(days=config.PREDICTION_CUTOFF_DAY)

    state = compute_user_state(user["user_id"], events, cutoff)
    consent = bool(user["marketing_consent"])

    # 规则 1：高流失风险且同意营销 -> 再互动。
    # 当没有模型分数时，仅标记已完成新手引导但不活跃的用户；
    # 新用户会被引导至新手引导。
    high_risk = (
        (churn_risk_score is not None and churn_risk_score >= 0.70)
        or (
            churn_risk_score is None
            and state["onboarding_completed"]
            and not state["recently_active"]
        )
    )
    if high_risk:
        if consent:
            return {
                "action_name": "send_reengagement_message",
                "channel": "email",
                "reason": "high churn risk with marketing consent",
            }
        return {
            "action_name": "send_reengagement_message",
            "channel": "in_app",
            "reason": "high churn risk without marketing consent",
        }

    # 规则 2：未完成新手引导。
    if not state["onboarding_completed"]:
        return {
            "action_name": "complete_onboarding",
            "channel": "in_app",
            "reason": "onboarding not completed",
        }

    # 规则 3：未完善资料。
    if not state["profile_completed"]:
        return {
            "action_name": "complete_profile",
            "channel": "in_app",
            "reason": "profile not completed",
        }

    # 规则 4：未上传简历。
    if not state["resume_uploaded"]:
        return {
            "action_name": "upload_resume",
            "channel": "in_app",
            "reason": "resume not uploaded",
        }

    # 规则 5：未查看职位推荐。
    if not state["job_recommendation_viewed"]:
        return {
            "action_name": "view_job_recommendations",
            "channel": "in_app",
            "reason": "job recommendations not viewed",
        }

    # 规则 6：已查看但未保存。
    if not state["job_saved"]:
        return {
            "action_name": "save_relevant_job",
            "channel": "in_app",
            "reason": "job viewed but not saved",
        }

    # 规则 7：未完成成长任务。
    if not state["growth_task_completed"]:
        return {
            "action_name": "complete_growth_task",
            "channel": "in_app",
            "reason": "growth task not completed",
        }

    # 规则 8：未生成职业报告。
    if not state["career_report_generated"]:
        return {
            "action_name": "generate_career_report",
            "channel": "in_app",
            "reason": "career report not generated",
        }

    # 规则 9：已完成所有核心行为。
    return {
        "action_name": "continue_weekly_engagement",
        "channel": "email" if consent else "in_app",
        "reason": "all core actions completed",
    }
