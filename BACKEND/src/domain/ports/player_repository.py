"""
Domain Port (Output Port): PlayerRepository
Defines the interface that any player data source must implement.
Following Hexagonal Architecture, this port belongs to the Domain layer.
"""
from abc import ABC, abstractmethod
from typing import Optional
from datetime import date

from src.domain.entities.player import Player


class PlayerRepository(ABC):
    """
    Abstract repository interface for Player persistence.
    Infrastructure adapters (e.g. SQLAlchemy, in-memory) must implement this.
    """

    @abstractmethod
    async def find_by_id(self, player_id: str) -> Optional[Player]:
        """Retrieve a player by their unique identifier."""
        ...

    @abstractmethod
    async def find_by_nationality_and_birth_date(
        self,
        nationality: str,
        birth_date: date,
    ) -> list[Player]:
        """
        Find all players matching a given nationality and birth date.
        Core query for regen detection.
        """
        ...

    @abstractmethod
    async def find_legendaries(self) -> list[Player]:
        """Retrieve all players marked as legendary (retired icons)."""
        ...

    @abstractmethod
    async def save(self, player: Player) -> Player:
        """Persist a new or updated player."""
        ...

    @abstractmethod
    async def delete(self, player_id: str) -> None:
        """Remove a player by their identifier."""
        ...
