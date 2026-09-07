"""
Infrastructure Adapter (Input): FastAPI Router for Players
Exposes HTTP endpoints for player-related operations.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import date

from src.infrastructure.persistence.in_memory.player_repository import InMemoryPlayerRepository
from src.domain.entities.player import Player

router = APIRouter(prefix="/players", tags=["players"])

# Temporary in-memory repo; replace with DI container in production
_player_repo = InMemoryPlayerRepository()


class PlayerResponse(BaseModel):
    id: str
    name: str
    nationality: str
    birth_date: date
    overall_rating: int
    position: str
    is_legendary: bool

    class Config:
        from_attributes = True


class CreatePlayerRequest(BaseModel):
    id: str
    name: str
    nationality: str
    birth_date: date
    overall_rating: int
    position: str
    is_legendary: bool = False
    potential: int | None = None


@router.get("/", response_model=list[PlayerResponse], summary="List legendary players")
async def list_legendaries():
    """Returns all players marked as legendary."""
    players = await _player_repo.find_legendaries()
    return players


@router.get("/{player_id}", response_model=PlayerResponse, summary="Get player by ID")
async def get_player(player_id: str):
    """Retrieve a specific player by their unique ID."""
    player = await _player_repo.find_by_id(player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player


@router.post("/", response_model=PlayerResponse, status_code=201, summary="Create a player")
async def create_player(body: CreatePlayerRequest):
    """Persist a new player in the system."""
    player = Player(
        id=body.id,
        name=body.name,
        nationality=body.nationality,
        birth_date=body.birth_date,
        overall_rating=body.overall_rating,
        position=body.position,
        is_legendary=body.is_legendary,
        potential=body.potential,
    )
    saved = await _player_repo.save(player)
    return saved
