"""
Infrastructure Adapter (Output): InMemoryRegenRepository
In-memory implementation of RegenRepository for development and testing.
"""
from typing import Optional
from uuid import uuid4

from src.domain.entities.regen import Regen
from src.domain.ports.regen_repository import RegenRepository


class InMemoryRegenRepository(RegenRepository):
    """
    Volatile, in-memory store for Regen entities.
    """

    def __init__(self) -> None:
        self._store: dict[str, Regen] = {}

    async def find_by_id(self, regen_id: str) -> Optional[Regen]:
        return self._store.get(regen_id)

    async def find_by_legendary_player_id(self, player_id: str) -> list[Regen]:
        return [
            r for r in self._store.values()
            if r.legendary_player.id == player_id
        ]

    async def find_by_season(self, season: str) -> list[Regen]:
        return [r for r in self._store.values() if r.season == season]

    async def save(self, regen: Regen) -> Regen:
        # Use a composite key: legendary_id + regen_candidate_id
        key = f"{regen.legendary_player.id}_{regen.regen_candidate.id}"
        self._store[key] = regen
        return regen
