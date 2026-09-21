from datetime import date

from fastapi import APIRouter
from pydantic import BaseModel

from BACKEND.application.ports.use_cases import (
    UpdateCatalogCommand,
    UpdateCatalogUseCase,
)
from BACKEND.domain.entities.player import Player


class PlayerPayload(BaseModel):
    id: str
    name: str
    birth_date: date
    nationality: str
    position: str
    overall: int | float
    age: int

    def to_domain(self, season: str) -> Player:
        return Player(
            id=self.id,
            name=self.name,
            birth_date=self.birth_date,
            nationality=self.nationality,
            position=self.position,
            overall=self.overall,
            age=self.age,
            season=season,
        )


class CatalogUpdatePayload(BaseModel):
    season: str
    players: list[PlayerPayload]


class CatalogUpdateResponse(BaseModel):
    season: str
    inserted: int
    updated: int


def create_catalog_router(update_catalog_use_case: UpdateCatalogUseCase) -> APIRouter:
    router = APIRouter()

    @router.put(
        "/api/v1/players/catalog",
        response_model=CatalogUpdateResponse,
    )
    def update_catalog(payload: CatalogUpdatePayload) -> CatalogUpdateResponse:
        result = update_catalog_use_case.execute(
            UpdateCatalogCommand(
                season=payload.season,
                players=tuple(
                    player.to_domain(payload.season) for player in payload.players
                ),
            )
        )
        return CatalogUpdateResponse(
            season=result.season,
            inserted=result.inserted,
            updated=result.updated,
        )

    return router