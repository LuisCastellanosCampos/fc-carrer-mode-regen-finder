from datetime import date

import pytest

from BACKEND.adapters.outbound.sqlite_catalog import SQLiteCatalog
from BACKEND.domain.entities.player import Player
from BACKEND.domain.exceptions.errors import ValidationError


def valid_player(player_id: str, overall: int = 87) -> Player:
    return Player(
        id=player_id,
        name="Alejandro Ruiz",
        birth_date=date(1998, 4, 12),
        nationality="Spain",
        position="ST",
        overall=overall,
        age=24,
        season="2026",
    )


def test_sqlite_catalog_persists_players_in_a_configurable_path(tmp_path) -> None:
    db_path = tmp_path / "catalog.db"
    catalog = SQLiteCatalog(db_path)

    players = (valid_player("p-1"), valid_player("p-2"))
    catalog.replace_players(players)

    assert catalog.read_players() == players
    assert db_path.exists()


def test_sqlite_catalog_is_atomic_when_replacement_is_invalid(tmp_path) -> None:
    catalog = SQLiteCatalog(tmp_path / "catalog.db")
    existing = (valid_player("p-1"),)
    catalog.replace_players(existing)

    with pytest.raises(ValidationError, match="ID duplicado"):
        catalog.replace_players((valid_player("p-2"), valid_player("p-2")))

    assert catalog.read_players() == existing
