"""Retention analytics router."""

from fastapi import APIRouter

from backend.app.schemas import RetentionResponse
from backend.app.services.analytics_service import get_retention

router = APIRouter(prefix="/api/retention", tags=["retention"])


@router.get("", response_model=RetentionResponse)
def retention() -> dict:
    """Return D1/D7/D14 retention and cohort retention."""
    return get_retention()
