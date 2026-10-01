from datetime import date
from typing import Iterable

from BACKEND.domain.entities.player import Player
from BACKEND.domain.exceptions.errors import ValidationError


class SofifaTransformer:
    """Transforma filas de Sofifa al modelo Player y valida la colección."""

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

    def to_players(self, rows: Iterable[dict]) -> tuple[Player, ...]:
        if rows is None:
            raise ValidationError("La colección Sofifa no puede ser nula")

        normalized_rows = list(rows)
        if not normalized_rows:
            raise ValidationError("La colección Sofifa no puede estar vacía")

        seen_ids: set[str] = set()
        players: list[Player] = []

        for index, row in enumerate(normalized_rows):
            if not isinstance(row, dict):
                raise ValidationError(f"La fila {index} de Sofifa no es un objeto válido")

            missing = sorted(self.REQUIRED_FIELDS - set(row.keys()))
            if missing:
                raise ValidationError(f"Faltan campos obligatorios: {', '.join(missing)}")

            player = self._to_player(row)
            if player.id in seen_ids:
                raise ValidationError(f"El identificador {player.id} está duplicado")
            seen_ids.add(player.id)
            players.append(player)

        self._validate_ambiguity(players)
        return tuple(players)

    @staticmethod
    def _to_player(row: dict) -> Player:
        birth_date = SofifaTransformer._parse_date(row["birth_date"])
        overall = SofifaTransformer._parse_overall(row["overall"])
        age = SofifaTransformer._parse_age(row["age"])
        position = SofifaTransformer._clean_text(row["position"], "posición")
        nationality = SofifaTransformer._clean_text(row["nationality"], "nacionalidad")
        season = SofifaTransformer._clean_text(row["season"], "temporada")

        return Player(
            id=SofifaTransformer._clean_text(row["id"], "id"),
            name=SofifaTransformer._clean_text(row["name"], "name"),
            birth_date=birth_date,
            nationality=nationality,
            position=position,
            overall=overall,
            age=age,
            season=season,
        )

    @staticmethod
    def _clean_text(value: object, field_name: str) -> str:
        if not isinstance(value, str):
            raise ValidationError(f"El campo {field_name} debe ser texto")
        cleaned = value.strip()
        if not cleaned:
            raise ValidationError(f"El campo {field_name} no puede estar vacío")
        return cleaned

    @staticmethod
    def _parse_date(value: object) -> date:
        if not isinstance(value, str):
            raise ValidationError("La fecha de nacimiento debe ser una fecha válida")
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

    @staticmethod
    def _validate_ambiguity(players: list[Player]) -> None:
        by_identity: dict[tuple[str, date], set[str]] = {}
        for player in players:
            key = (player.nationality, player.birth_date)
            by_identity.setdefault(key, set()).add(player.position)

        for positions in by_identity.values():
            if len(positions) > 1:
                raise ValidationError("La colección Sofifa contiene registros ambiguos")
