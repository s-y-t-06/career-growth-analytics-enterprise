"""User scoring and detail router."""

from datetime import timedelta

from fastapi import APIRouter, HTTPException, Query

from backend.app import config
from backend.app.schemas import (
    ScoreRequest,
    ScoreResponse,
    UserDetailResponse,
    UserListResponse,
    UserSummary,
)
from backend.app.services.data_service import (
    load_events,
    load_experiment_assignments,
    load_model_metadata,
    load_users,
)
from backend.app.services.model_service import explain_user, score_all_users, score_single_user

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("", response_model=UserListResponse)
def list_users(
    limit: int = Query(50, ge=1, le=1000),
    sort_by: str = Query("risk"),
    min_risk: float | None = Query(None, ge=0.0, le=1.0),
    acquisition_channel: str | None = Query(None),
    career_stage: str | None = Query(None),
) -> dict:
    """Return a list of users with churn risk and NBA recommendations."""
    scored = score_all_users()
    users = load_users()

    merged = scored.merge(
        users[["user_id", "acquisition_channel", "career_stage", "device_type"]],
        on="user_id",
        how="left",
    )

    if min_risk is not None:
        merged = merged[merged["predicted_risk"] >= min_risk]
    if acquisition_channel:
        merged = merged[merged["acquisition_channel"] == acquisition_channel]
    if career_stage:
        merged = merged[merged["career_stage"] == career_stage]

    if sort_by == "risk":
        merged = merged.sort_values("predicted_risk", ascending=False)

    total = len(merged)
    page = merged.head(limit)

    records = [
        UserSummary(
            user_id=row["user_id"],
            acquisition_channel=row.get("acquisition_channel", ""),
            career_stage=row.get("career_stage", ""),
            device_type=row.get("device_type", ""),
            churn_probability=row["predicted_risk"],
            predicted_class=row["predicted_class"],
            recommended_action=row["action_name"],
            channel=row["channel"],
        )
        for _, row in page.iterrows()
    ]

    return {"users": records, "total": total}


@router.get("/{user_id}", response_model=UserDetailResponse)
def user_detail(user_id: str) -> dict:
    """Return detailed profile, risk, explanation, and timeline for a user."""
    users = load_users()
    events = load_events()

    user_row = users[users["user_id"] == user_id]
    if user_row.empty:
        raise HTTPException(status_code=404, detail="User not found")

    user = user_row.iloc[0]
    score = score_single_user(user_id)
    explanation = explain_user(user_id)

    cutoff = user["signup_timestamp"] + timedelta(days=config.CUTOFF_DAY)
    user_events = events[
        (events["user_id"] == user_id)
        & (events["event_timestamp"] <= cutoff)
    ].sort_values("event_timestamp")

    timeline = [
        {
            "event_name": row["event_name"],
            "event_timestamp": row["event_timestamp"].isoformat(),
            "event_source": row.get("event_source", ""),
        }
        for _, row in user_events.iterrows()
    ]

    from career_growth.features.model_features import build_model_features

    features_df = build_model_features(user_row, user_events, load_experiment_assignments())
    features = {col: _serialize(features_df[col].iloc[0]) for col in features_df.columns if col != "signup_timestamp"}

    return {
        "user_id": user_id,
        "profile": {
            "acquisition_channel": user.get("acquisition_channel"),
            "country": user.get("country"),
            "device_type": user.get("device_type"),
            "user_intent_level": user.get("user_intent_level"),
            "career_stage": user.get("career_stage"),
            "marketing_consent": bool(user.get("marketing_consent")),
            "language": user.get("language"),
            "timezone": user.get("timezone"),
            "signup_timestamp": user["signup_timestamp"].isoformat(),
        },
        "features": features,
        "churn_probability": score["churn_probability"],
        "predicted_class": score["predicted_class"],
        "explanation": explanation,
        "recommended_action": score["recommended_action"],
        "channel": score["channel"],
        "reason": score["reason"],
        "timeline": timeline,
    }


def _serialize(value) -> str | float | int | bool | None:
    """Serialize a scalar value for JSON output."""
    import pandas as pd

    if pd.isna(value):
        return None
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return value


@router.post("/score", response_model=ScoreResponse)
def score_user(payload: ScoreRequest) -> dict:
    """Score a single user by ID and return risk + recommendation."""
    try:
        return score_single_user(payload.user_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
