from dataclasses import dataclass
from datetime import date
from numbers import Real
from unicodedata import normalize

from BACKEND.domain.exceptions.errors import ValidationError


@dataclass(frozen=True, slots=True)
class Player:
    """Jugador activo del catálogo anual y sus invariantes de dominio."""

    id: str | None = None
    name: str | None = None
    birth_date: date | None = None
    nationality: str | None = None
    position: str | None = None
    overall: int | float | None = None
    age: int | None = None
    season: str | None = None

    def __post_init__(self) -> None:
        if isinstance(self.id, str):
            object.__setattr__(self, "id", normalize("NFKC", self.id).strip().casefold())

        self._validate_required_text(self.id, "id")
        self._validate_required_text(self.name, "nombre")
        self._validate_required_text(self.nationality, "nacionalidad")
        self._validate_required_text(self.position, "posición")
        self._validate_required_text(self.season, "temporada")

        if type(self.birth_date) is not date:
            raise ValidationError("La fecha de nacimiento debe ser una fecha válida")
        if isinstance(self.overall, bool) or not isinstance(self.overall, Real):
            raise ValidationError("El overall debe ser un número entre 0 y 100")
        if not 0 <= self.overall <= 100:
            raise ValidationError("El overall debe ser un número entre 0 y 100")
        if isinstance(self.age, bool) or not isinstance(self.age, int) or self.age < 0:
            raise ValidationError("La edad debe ser un entero no negativo")

    @staticmethod
    def _validate_required_text(value: object, field: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValidationError(f"El campo {field} no puede estar vacío")
