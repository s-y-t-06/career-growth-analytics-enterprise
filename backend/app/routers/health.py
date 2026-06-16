"""Health check router."""

from fastapi import APIRouter

from backend.app import config
from backend.app.database import get_connection
from backend.app.schemas import HealthResponse

router = APIRouter(tags=["health"])


def _status_text(exists: bool) -> str:
    return "ok" if exists else "missing"


@router.get("/health", response_model=HealthResponse)
def health() -> dict:
    """Return backend, database, model, and metrics health status."""
    try:
        conn = get_connection()
        conn.execute("SELECT 1")
        conn.close()
        db_status = "ok"
    except Exception as exc:
        db_status = f"error: {exc}"

    return {
        "status": "ok",
        "database": db_status,
        "model": _status_text(config.MODEL_PATH.exists()),
        "metrics": _status_text(config.METRICS_PATH.exists()),
    }
