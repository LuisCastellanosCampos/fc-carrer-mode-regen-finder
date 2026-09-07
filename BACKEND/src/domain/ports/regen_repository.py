"""
Domain Port (Output Port): RegenRepository
Defines the interface for persisting and querying regen matches.
"""
from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities.regen import Regen


class RegenRepository(ABC):
    """
    Abstract repository interface for Regen persistence.
    """

    @abstractmethod
    async def find_by_id(self, regen_id: str) -> Optional[Regen]:
        """Retrieve a regen match by its identifier."""
        ...

    @abstractmethod
    async def find_by_legendary_player_id(self, player_id: str) -> list[Regen]:
        """Find all regen candidates for a given legendary player."""
        ...

    @abstractmethod
    async def find_by_season(self, season: str) -> list[Regen]:
        """Retrieve all regens found in a particular season."""
        ...

    @abstractmethod
    async def save(self, regen: Regen) -> Regen:
        """Persist a regen match."""
        ...
