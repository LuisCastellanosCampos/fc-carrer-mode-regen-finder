from collections.abc import Iterable

from BACKEND.domain.entities.player import Player
from BACKEND.domain.exceptions.errors import ValidationError


def validate_player_collection(players: Iterable[Player]) -> tuple[Player, ...]:
    """Valida una carga completa del catálogo antes de cualquier reemplazo."""
    materialized = tuple(players)
    seen_ids: set[str] = set()

    for player in materialized:
        if not isinstance(player, Player):
            raise ValidationError("Cada entrada debe ser un jugador válido")
        if player.id in seen_ids:
            raise ValidationError(f"ID duplicado en la colección: {player.id}")
        seen_ids.add(player.id)

    return materialized