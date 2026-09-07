"""
Application Use Case: GetPlayerRegensUseCase
Retrieves all regen matches for a specific legendary player.
"""
from src.domain.entities.regen import Regen
from src.domain.ports.regen_repository import RegenRepository


class GetPlayerRegensUseCase:
    """
    Retrieves the regen history for a given legendary player.
    """

    def __init__(self, regen_repo: RegenRepository) -> None:
        self._regen_repo = regen_repo

    async def execute(self, legendary_player_id: str) -> list[Regen]:
        """Return all regens associated with a legendary player."""
        return await self._regen_repo.find_by_legendary_player_id(legendary_player_id)
