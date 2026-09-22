from datetime import date

from fastapi import APIRouter
from pydantic import BaseModel

from BACKEND.application.ports.use_cases import (
    FindRegensQuery,
    FindRegensUseCase,
    UpdateCatalogCommand,
    UpdateCatalogUseCase,
)
from BACKEND.domain.entities.player import Player
from BACKEND.domain.entities.regen_match import RegenMatch


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


class PlayerResponse(BaseModel):
    id: str
    name: str
    birth_date: date
    nationality: str
    position: str
    overall: int | float
    age: int
    season: str

    @classmethod
    def from_domain(cls, player: Player) -> "PlayerResponse":
        return cls(
            id=player.id,
            name=player.name,
            birth_date=player.birth_date,
            nationality=player.nationality,
            position=player.position,
            overall=player.overall,
            age=player.age,
            season=player.season,
        )


class RegenMatchResponse(BaseModel):
    player: PlayerResponse
    match: "MatchStatusResponse"

    @classmethod
    def from_domain(cls, match: RegenMatch) -> "RegenMatchResponse":
        return cls(
            player=PlayerResponse.from_domain(match.player),
            match=MatchStatusResponse(
                birth_date=match.birth_date_matches,
                nationality=match.nationality_matches,
                position=match.position_matches,
                is_possible_regen=match.is_possible_regen,
                message=match.message,
            ),
        )


class MatchStatusResponse(BaseModel):
    birth_date: bool
    nationality: bool
    position: bool | None
    is_possible_regen: bool
    message: str


class RegenQueryResponse(BaseModel):
    birth_date: date
    nationality: str
    position: str | None


class RegenSearchResponse(BaseModel):
    query: RegenQueryResponse
    matches: list[RegenMatchResponse]
    message: str | None


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


def create_regen_router(find_regens_use_case: FindRegensUseCase) -> APIRouter:
    router = APIRouter()

    @router.get("/api/v1/regens", response_model=RegenSearchResponse)
    def find_regens(
        birth_date: date,
        nationality: str,
        position: str | None = None,
    ) -> RegenSearchResponse:
        result = find_regens_use_case.execute(
            FindRegensQuery(
                birth_date=birth_date,
                nationality=nationality,
                position=position,
            )
        )
        return RegenSearchResponse(
            query=RegenQueryResponse(
                birth_date=birth_date,
                nationality=nationality,
                position=position,
            ),
            matches=[RegenMatchResponse.from_domain(match) for match in result],
            message=result.message,
        )

    return router