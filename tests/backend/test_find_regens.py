from datetime import date

from BACKEND.adapters.outbound.in_memory_catalog import InMemoryCatalog
from BACKEND.application.ports.use_cases import FindRegensQuery
from BACKEND.application.use_cases.find_regens import FindRegensService
from BACKEND.domain.entities.player import Player


def player(
    player_id: str,
    *,
    birth_date: date = date(1998, 4, 12),
    nationality: str = "Spain",
) -> Player:
    return Player(
        id=player_id,
        name="Alejandro Ruiz",
        birth_date=birth_date,
        nationality=nationality,
        position="ST",
        overall=80,
        age=24,
        season="2026",
    )


def test_find_regens_returns_only_players_matching_date_and_nationality() -> None:
    catalog = InMemoryCatalog()
    exact_match = player("p-exact", nationality="  EsPaÑa  ")
    wrong_date = player("p-date", birth_date=date(1997, 4, 12))
    wrong_nationality = player("p-nationality", nationality="France")
    catalog.replace_players((exact_match, wrong_date, wrong_nationality))

    matches = FindRegensService(catalog).execute(
        FindRegensQuery(date(1998, 4, 12), " españa ")
    )

    assert [match.player.id for match in matches] == ["p-exact"]
    assert matches[0].birth_date_matches is True
    assert matches[0].nationality_matches is True
    assert matches[0].is_possible_regen is True


def test_find_regens_excludes_partial_matches() -> None:
    catalog = InMemoryCatalog()
    catalog.replace_players(
        (
            player("p-date-only", nationality="France"),
            player("p-nationality-only", birth_date=date(1997, 4, 12)),
        )
    )

    matches = FindRegensService(catalog).execute(
        FindRegensQuery(date(1998, 4, 12), "Spain")
    )

    assert matches == ()