from BACKEND.application.ports.catalog import CatalogPort
from BACKEND.domain.entities.player import Player
from BACKEND.domain.services.catalog_validation import validate_player_collection


class InMemoryCatalog(CatalogPort):
    """Adaptador de catálogo en memoria para sustituir una persistencia real."""

    def __init__(self) -> None:
        self._players: tuple[Player, ...] = ()

    def read_players(self) -> tuple[Player, ...]:
        return self._players

    def replace_players(self, players: tuple[Player, ...]) -> None:
        validated_players = validate_player_collection(players)
        self._players = validated_players