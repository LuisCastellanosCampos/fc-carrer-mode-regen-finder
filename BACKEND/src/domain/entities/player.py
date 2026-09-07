"""
Domain Entity: Player
Represents a football player in the domain model.
"""
from dataclasses import dataclass, field
from datetime import date
from typing import Optional


@dataclass
class Player:
    """
    Core domain entity representing a football player.
    Contains the essential attributes needed to identify and match regens.
    """
    id: str
    name: str
    nationality: str
    birth_date: date
    overall_rating: int
    position: str
    is_legendary: bool = False
    potential: Optional[int] = None

    def age(self, reference_date: Optional[date] = None) -> int:
        """Calculate the player's age as of a given date."""
        ref = reference_date or date.today()
        return (
            ref.year - self.birth_date.year
            - ((ref.month, ref.day) < (self.birth_date.month, self.birth_date.day))
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Player):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
