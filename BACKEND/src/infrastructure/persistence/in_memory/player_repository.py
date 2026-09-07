"""
Infrastructure Adapter (Output): InMemoryPlayerRepository
In-memory implementation of PlayerRepository for development and testing.
"""
from datetime import date
from typing import Optional

from src.domain.entities.player import Player
from src.domain.ports.player_repository import PlayerRepository


class InMemoryPlayerRepository(PlayerRepository):
    """
    Volatile, in-memory store for Player entities.
    Replace with a real database adapter (e.g. SQLAlchemy) in production.
    """

    def __init__(self) -> None:
        self._store: dict[str, Player] = {}

    async def find_by_id(self, player_id: str) -> Optional[Player]:
        return self._store.get(player_id)

    async def find_by_nationality_and_birth_date(
        self,
        nationality: str,
        birth_date: date,
    ) -> list[Player]:
        return [
            p for p in self._store.values()
            if p.nationality == nationality and p.birth_date == birth_date
        ]

    async def find_legendaries(self) -> list[Player]:
        return [p for p in self._store.values() if p.is_legendary]

    async def save(self, player: Player) -> Player:
        self._store[player.id] = player
        return player

    async def delete(self, player_id: str) -> None:
        self._store.pop(player_id, None)
