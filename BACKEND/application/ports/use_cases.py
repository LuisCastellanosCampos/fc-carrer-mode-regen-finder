from dataclasses import dataclass
from datetime import date
from typing import Protocol
from unicodedata import normalize

from BACKEND.domain.entities.player import Player
from BACKEND.domain.exceptions.errors import ValidationError
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


class FindRegensResult(tuple[RegenMatch, ...]):
    message: str | None

    def __new__(
        cls,
        matches: tuple[RegenMatch, ...],
        message: str | None = None,
    ) -> "FindRegensResult":
        result = super().__new__(cls, matches)
        result.message = message
        return result


@dataclass(frozen=True, slots=True)
class FindRegensQuery:
    birth_date: date
    nationality: str
    position: str | None = None

    def __post_init__(self) -> None:
        if type(self.birth_date) is not date:
            raise ValidationError(
                "La fecha de nacimiento debe ser una fecha exacta válida"
            )

        object.__setattr__(
            self,
            "nationality",
            self._normalize_required_text(self.nationality, "nacionalidad"),
        )
        if self.position is not None:
            object.__setattr__(
                self,
                "position",
                self._normalize_required_text(self.position, "posición"),
            )

    @staticmethod
    def _normalize_required_text(value: object, field: str) -> str:
        if not isinstance(value, str):
            raise ValidationError(f"El campo {field} no puede estar vacío")

        normalized = normalize("NFKC", value).strip().casefold()
        if not normalized:
            raise ValidationError(f"El campo {field} no puede estar vacío")
        return normalized


class UpdateCatalogUseCase(Protocol):
    """Puerto de entrada para actualizar el catálogo anual."""

    def execute(self, command: UpdateCatalogCommand) -> CatalogUpdateResult:
        ...


class FindRegensUseCase(Protocol):
    """Puerto de entrada para consultar posibles regens."""

    def execute(self, query: FindRegensQuery) -> FindRegensResult:
        ...
