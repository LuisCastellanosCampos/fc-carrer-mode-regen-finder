from dataclasses import dataclass
from datetime import date
from typing import Protocol

from BACKEND.domain.entities.player import Player
from BACKEND.domain.entities.regen_match import RegenMatch


@dataclass(frozen=True, slots=True)
class UpdateCatalogCommand:
    season: str
    players: tuple[Player, ...]


@dataclass(frozen=True, slots=True)
class CatalogUpdateResult:
    season: str
    inserted: int
    updated: int


@dataclass(frozen=True, slots=True)
class FindRegensQuery:
    birth_date: date
    nationality: str
    position: str | None = None


class UpdateCatalogUseCase(Protocol):
    """Puerto de entrada para actualizar el catálogo anual."""

    def execute(self, command: UpdateCatalogCommand) -> CatalogUpdateResult:
        ...


class FindRegensUseCase(Protocol):
    """Puerto de entrada para consultar posibles regens."""

    def execute(self, query: FindRegensQuery) -> tuple[RegenMatch, ...]:
        ...
