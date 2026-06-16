"""Model metrics and subgroup router."""

from fastapi import APIRouter, HTTPException

from backend.app.schemas import ModelMetricsResponse, SubgroupResponse
from backend.app.services.data_service import load_metrics, load_subgroup_metrics

router = APIRouter(prefix="/api/model", tags=["model"])


@router.get("/metrics", response_model=ModelMetricsResponse)
def model_metrics() -> dict:
    """Return model metrics from artifacts."""
    metrics = load_metrics()
    return {
        "selected_model": metrics.get("selected_model", "unknown"),
        "selected_threshold": metrics.get("selected_threshold", 0.0),
        "validation": metrics.get("validation", {}),
        "test": metrics.get("test", {}),
        "confusion_matrix": metrics.get("confusion_matrix", {}),
    }


@router.get("/subgroups", response_model=SubgroupResponse)
def model_subgroups() -> dict:
    """Return subgroup evaluation metrics."""
    groups = load_subgroup_metrics()
    return {"groups": groups}
