from typing import Protocol

from BACKEND.domain.entities.player import Player


class CatalogPort(Protocol):
    """Puerto para leer y reemplazar el catálogo de jugadores."""

    def read_players(self) -> tuple[Player, ...]:
        """Devuelve el catálogo actual sin exponer su persistencia."""
        ...

    def replace_players(self, players: tuple[Player, ...]) -> None:
        """Reemplaza el catálogo de forma atómica."""
        ...
