"""
Domain Entity: Regen
Represents a regen (reincarnation) match between a legendary player
and a young player in Career Mode.
"""
from dataclasses import dataclass
from datetime import date
from typing import Optional

from src.domain.entities.player import Player


@dataclass
class Regen:
    """
    Represents a regen match: a young player who is the 'reincarnation'
    of a retired legendary player, sharing nationality and birth date.
    """
    legendary_player: Player
    regen_candidate: Player
    match_score: float  # 0.0 - 1.0, confidence of the match
    season: str         # e.g. "2024/2025"
    notes: Optional[str] = None

    @property
    def is_confirmed(self) -> bool:
        """A regen is considered confirmed when the match score is high enough."""
        return self.match_score >= 0.85

    @property
    def shares_nationality(self) -> bool:
        return self.legendary_player.nationality == self.regen_candidate.nationality

    @property
    def shares_birth_date(self) -> bool:
        return self.legendary_player.birth_date == self.regen_candidate.birth_date
