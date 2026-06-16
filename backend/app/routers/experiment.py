"""Experiment analytics router."""

from fastapi import APIRouter

from backend.app.schemas import ExperimentResponse
from backend.app.services.analytics_service import get_experiment

router = APIRouter(prefix="/api/experiment", tags=["experiment"])


@router.get("", response_model=ExperimentResponse)
def experiment() -> dict:
    """Return onboarding A/B experiment analysis."""
    return get_experiment("exp_onboarding_v1")
