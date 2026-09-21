from datetime import date

import pytest

from BACKEND.adapters.outbound.in_memory_catalog import InMemoryCatalog
from BACKEND.application.ports.use_cases import UpdateCatalogCommand
from BACKEND.application.use_cases.update_catalog import UpdateCatalogService
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


def test_update_catalog_inserts_new_players() -> None:
    catalog = InMemoryCatalog()
    service = UpdateCatalogService(catalog)

    result = service.execute(
        UpdateCatalogCommand("2026", (valid_player("p-1"), valid_player("p-2")))
    )

    assert result.season == "2026"
    assert result.inserted == 2
    assert result.updated == 0
    assert {player.id for player in catalog.read_players()} == {"p-1", "p-2"}


def test_update_catalog_replaces_existing_player_by_id() -> None:
    catalog = InMemoryCatalog()
    catalog.replace_players((valid_player("p-1", overall=80),))
    service = UpdateCatalogService(catalog)

    result = service.execute(
        UpdateCatalogCommand("2027", (valid_player("p-1", overall=91),))
    )

    assert result.inserted == 0
    assert result.updated == 1
    assert catalog.read_players()[0].overall == 91


def test_update_catalog_loads_initial_catalog_atomically() -> None:
    catalog = InMemoryCatalog()
    service = UpdateCatalogService(catalog)
    players = (valid_player("p-1"), valid_player("p-2"))

    result = service.execute(UpdateCatalogCommand("2026", players))

    assert result.inserted == 2
    assert result.updated == 0
    assert catalog.read_players() == players


def test_update_catalog_inserts_and_updates_in_the_same_annual_load() -> None:
    catalog = InMemoryCatalog()
    catalog.replace_players((valid_player("p-existing", overall=80),))
    service = UpdateCatalogService(catalog)
    updated_player = valid_player("p-existing", overall=91)
    new_player = valid_player("p-new", overall=88)

    result = service.execute(
        UpdateCatalogCommand("2027", (updated_player, new_player))
    )

    assert result.inserted == 1
    assert result.updated == 1
    assert catalog.read_players() == (updated_player, new_player)


@pytest.mark.parametrize(
    "players",
    [
        (valid_player("p-1"), valid_player("p-1")),
        (valid_player("p-2"), object()),
    ],
)
def test_update_catalog_is_atomic_when_collection_is_invalid(
    players: tuple[object, ...],
) -> None:
    catalog = InMemoryCatalog()
    existing = (valid_player("p-existing"),)
    catalog.replace_players(existing)
    service = UpdateCatalogService(catalog)

    with pytest.raises(ValidationError):
        service.execute(UpdateCatalogCommand("2026", players))  # type: ignore[arg-type]

    assert catalog.read_players() == existing


def test_update_catalog_rejects_invalid_data_before_any_replacement() -> None:
    catalog = InMemoryCatalog()
    existing = (valid_player("p-existing", overall=80),)
    catalog.replace_players(existing)
    service = UpdateCatalogService(catalog)

    with pytest.raises(ValidationError, match="jugador válido"):
        service.execute(
            UpdateCatalogCommand("2026", (valid_player("p-new"), None))  # type: ignore[arg-type]
        )

    assert catalog.read_players() == existing
