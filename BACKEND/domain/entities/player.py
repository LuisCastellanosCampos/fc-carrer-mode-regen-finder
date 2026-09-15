from dataclasses import dataclass
from datetime import date
from numbers import Real


@dataclass(frozen=True, slots=True)
class Player:
    """Jugador activo del catálogo anual y sus invariantes de dominio."""

    id: str
    name: str
    birth_date: date
    nationality: str
    position: str
    overall: int | float
    age: int
    season: str

    def __post_init__(self) -> None:
        self._validate_required_text(self.id, "id")
        self._validate_required_text(self.name, "nombre")
        self._validate_required_text(self.nationality, "nacionalidad")
        self._validate_required_text(self.position, "posición")
        self._validate_required_text(self.season, "temporada")

        if type(self.birth_date) is not date:
            raise ValueError("La fecha de nacimiento debe ser una fecha válida")
        if isinstance(self.overall, bool) or not isinstance(self.overall, Real):
            raise ValueError("El overall debe ser un número entre 0 y 100")
        if not 0 <= self.overall <= 100:
            raise ValueError("El overall debe ser un número entre 0 y 100")
        if isinstance(self.age, bool) or not isinstance(self.age, int) or self.age < 0:
            raise ValueError("La edad debe ser un entero no negativo")

    @staticmethod
    def _validate_required_text(value: object, field: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"El campo {field} no puede estar vacío")
