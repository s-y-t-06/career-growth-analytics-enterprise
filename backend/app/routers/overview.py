"""Overview dashboard router."""

from fastapi import APIRouter

from backend.app.schemas import OverviewResponse
from backend.app.services.analytics_service import get_overview

router = APIRouter(prefix="/api/overview", tags=["overview"])


@router.get("", response_model=OverviewResponse)
def overview() -> dict:
    """Return high-level platform and model overview."""
    return get_overview()
