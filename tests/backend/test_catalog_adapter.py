from datetime import date

import pytest

from BACKEND.adapters.outbound.in_memory_catalog import InMemoryCatalog
from BACKEND.domain.entities.player import Player
from BACKEND.domain.exceptions.errors import ValidationError


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


def test_catalog_starts_empty() -> None:
    catalog = InMemoryCatalog()

    assert catalog.read_players() == ()


def test_catalog_replaces_and_reads_players_through_port() -> None:
    catalog = InMemoryCatalog()
    players = (valid_player("p-1"), valid_player("p-2"))

    catalog.replace_players(players)

    assert catalog.read_players() == players
    assert isinstance(catalog.read_players(), tuple)


def test_catalog_rejects_invalid_replacement_without_changing_existing_data() -> None:
    catalog = InMemoryCatalog()
    existing = (valid_player("p-1"),)
    catalog.replace_players(existing)

    with pytest.raises(ValidationError, match="ID duplicado"):
        catalog.replace_players((valid_player("p-2"), valid_player("p-2")))

    assert catalog.read_players() == existing