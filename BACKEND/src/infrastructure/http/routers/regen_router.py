"""
Infrastructure Adapter (Input): FastAPI Router for Regens
Exposes HTTP endpoints to trigger regen searches and retrieve results.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import date

from src.infrastructure.persistence.in_memory.player_repository import InMemoryPlayerRepository
from src.infrastructure.persistence.in_memory.regen_repository import InMemoryRegenRepository
from src.application.use_cases.find_regens import FindRegensUseCase
from src.application.use_cases.get_player_regens import GetPlayerRegensUseCase

router = APIRouter(prefix="/regens", tags=["regens"])

# Temporary shared repos; replace with DI container in production
_player_repo = InMemoryPlayerRepository()
_regen_repo = InMemoryRegenRepository()


class RegenResponse(BaseModel):
    legendary_player_id: str
    legendary_player_name: str
    regen_candidate_id: str
    regen_candidate_name: str
    match_score: float
    season: str
    is_confirmed: bool


@router.post(
    "/search",
    response_model=list[RegenResponse],
    summary="Search regens for current season",
)
async def search_regens(season: str = "2024/2025"):
    """
    Triggers the regen-finding algorithm across all legendary players
    and returns confirmed regen matches.
    """
    use_case = FindRegensUseCase(
        player_repo=_player_repo,
        regen_repo=_regen_repo,
        season=season,
    )
    regens = await use_case.execute()
    return [
        RegenResponse(
            legendary_player_id=r.legendary_player.id,
            legendary_player_name=r.legendary_player.name,
            regen_candidate_id=r.regen_candidate.id,
            regen_candidate_name=r.regen_candidate.name,
            match_score=r.match_score,
            season=r.season,
            is_confirmed=r.is_confirmed,
        )
        for r in regens
    ]


@router.get(
    "/{player_id}",
    response_model=list[RegenResponse],
    summary="Get regens for a legendary player",
)
async def get_player_regens(player_id: str):
    """Returns all regen matches found for a specific legendary player."""
    use_case = GetPlayerRegensUseCase(regen_repo=_regen_repo)
    regens = await use_case.execute(player_id)
    if not regens:
        raise HTTPException(status_code=404, detail="No regens found for this player")
    return [
        RegenResponse(
            legendary_player_id=r.legendary_player.id,
            legendary_player_name=r.legendary_player.name,
            regen_candidate_id=r.regen_candidate.id,
            regen_candidate_name=r.regen_candidate.name,
            match_score=r.match_score,
            season=r.season,
            is_confirmed=r.is_confirmed,
        )
        for r in regens
    ]
