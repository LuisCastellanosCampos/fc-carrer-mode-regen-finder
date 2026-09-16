from datetime import date

import pytest

from BACKEND.domain.entities.player import Player
from BACKEND.domain.exceptions.errors import ValidationError
from BACKEND.domain.services.catalog_validation import validate_player_collection


def valid_player(player_id: str) -> Player:
    return Player(
        id=player_id,
        name="Alejandro Ruiz",
        birth_date=date(1998, 4, 12),
        nationality="Spain",
        position="ST",
        overall=87,
        age=24,
        season="2026",
    )


def test_validate_player_collection_returns_players_in_input_order() -> None:
    players = (valid_player("p-2"), valid_player("p-1"))

    validated = validate_player_collection(players)

    assert validated == players


def test_validate_player_collection_rejects_duplicate_ids() -> None:
    players = (valid_player("p-1"), valid_player("p-1"))

    with pytest.raises(ValidationError, match="ID duplicado.*p-1"):
        validate_player_collection(players)


def test_validate_player_collection_rejects_equivalent_normalized_ids() -> None:
    players = (valid_player("p-1"), valid_player(" P-１ "))

    with pytest.raises(ValidationError, match="ID duplicado"):
        validate_player_collection(players)


def test_validate_player_collection_rejects_non_player_entries() -> None:
    with pytest.raises(ValidationError, match="jugador válido"):
        validate_player_collection((valid_player("p-1"), object()))