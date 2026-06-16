"""Next Best Action router."""

from fastapi import APIRouter, HTTPException

from backend.app.schemas import NBARequest, NBAResponse
from backend.app.services.nba_service import get_nba_examples, get_nba_for_user

router = APIRouter(prefix="/api/nba", tags=["nba"])


@router.get("/examples")
def nba_examples(n: int = 10) -> dict:
    """Return example NBA recommendations."""
    return {"examples": get_nba_examples(n)}


@router.post("/recommend", response_model=NBAResponse)
def nba_recommend(payload: NBARequest) -> dict:
    """Return a Next Best Action recommendation for a user."""
    try:
        result = get_nba_for_user(payload.user_id)
        return {
            "user_id": result["user_id"],
            "action_name": result["recommended_action"],
            "channel": result["channel"],
            "reason": result["reason"],
        }
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
