"""Funnel analytics router."""

from fastapi import APIRouter

from backend.app.schemas import FunnelResponse, FunnelStep
from backend.app.services.analytics_service import get_funnel

router = APIRouter(prefix="/api/funnel", tags=["funnel"])


@router.get("", response_model=FunnelResponse)
def funnel() -> dict:
    """Return the core user lifecycle funnel."""
    steps = get_funnel()
    return {"steps": [FunnelStep(**s) for s in steps]}
