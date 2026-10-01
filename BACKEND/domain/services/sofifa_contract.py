from datetime import date
from unicodedata import normalize

from BACKEND.domain.entities.player import Player
from BACKEND.domain.exceptions.errors import ValidationError


class SofifaContract:
    """Contrato versionado para transformar la salida de Sofifa en entidades Player."""

    REQUIRED_FIELDS = {
        "id",
        "name",
        "birth_date",
        "nationality",
        "position",
        "overall",
        "age",
        "season",
    }

    def to_player(self, payload: dict) -> Player:
        if not isinstance(payload, dict):
            raise ValidationError("El payload del contrato Sofifa debe ser un diccionario")

        missing = sorted(self.REQUIRED_FIELDS - set(payload.keys()))
        if missing:
            raise ValidationError(f"Faltan campos obligatorios: {', '.join(missing)}")

        cleaned = {
            "id": self._string(payload["id"], "id"),
            "name": self._string(payload["name"], "name"),
            "birth_date": self._parse_date(payload["birth_date"]),
            "nationality": self._string(payload["nationality"], "nacionalidad"),
            "position": self._string(payload["position"], "posición"),
            "overall": self._parse_overall(payload["overall"]),
            "age": self._parse_age(payload["age"]),
            "season": self._string(payload["season"], "temporada"),
        }

        return Player(**cleaned)

    @staticmethod
    def _string(value: object, field_name: str) -> str:
        if not isinstance(value, str):
            raise ValidationError(f"El campo {field_name} debe ser texto")
        cleaned = normalize("NFKC", value).strip()
        if not cleaned:
            raise ValidationError(f"El campo {field_name} no puede estar vacío")
        return cleaned

    @staticmethod
    def _parse_date(value: object) -> date:
        if isinstance(value, date):
            return value
        if not isinstance(value, str):
            raise ValidationError("La fecha de nacimiento debe tener formato ISO yyyy-mm-dd")
        try:
            return date.fromisoformat(value.strip())
        except ValueError as exc:
            raise ValidationError("La fecha de nacimiento debe ser una fecha válida") from exc

    @staticmethod
    def _parse_overall(value: object) -> int:
        if isinstance(value, bool):
            raise ValidationError("El overall debe ser un número entre 0 y 100")
        if isinstance(value, str):
            value = value.strip()
            try:
                value = int(value)
            except ValueError as exc:
                raise ValidationError("El overall debe ser un número entre 0 y 100") from exc
        if not isinstance(value, int):
            raise ValidationError("El overall debe ser un número entre 0 y 100")
        if not 0 <= value <= 100:
            raise ValidationError("El overall debe ser un número entre 0 y 100")
        return value

    @staticmethod
    def _parse_age(value: object) -> int:
        if isinstance(value, bool):
            raise ValidationError("La edad debe ser un entero no negativo")
        if isinstance(value, str):
            value = value.strip()
            try:
                value = int(value)
            except ValueError as exc:
                raise ValidationError("La edad debe ser un entero no negativo") from exc
        if not isinstance(value, int) or value < 0:
            raise ValidationError("La edad debe ser un entero no negativo")
        return value
