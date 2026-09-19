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
    position: str = "ST",
    overall: int = 85,
    age: int = 24,
) -> Player:
    return Player(
        id=player_id,
        name="Alejandro Ruiz",
        birth_date=birth_date,
        nationality=nationality,
        position=position,
        overall=overall,
        age=age,
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


def test_find_regens_without_matches_returns_empty_list_and_message() -> None:
    catalog = InMemoryCatalog()
    catalog.replace_players((player("p-other", nationality="France"),))
    service = FindRegensService(catalog)

    matches = service.execute(FindRegensQuery(date(1998, 4, 12), "Spain"))

    assert matches == ()
    assert matches.message == "No se encontraron posibles regens."


def test_find_regens_without_position_keeps_position_match_unknown() -> None:
    catalog = InMemoryCatalog()
    catalog.replace_players((player("p-exact"),))

    matches = FindRegensService(catalog).execute(
        FindRegensQuery(date(1998, 4, 12), "Spain")
    )

    assert matches[0].position_matches is None
    assert matches[0].message == (
        "Posible regen: coinciden fecha de nacimiento y nacionalidad."
    )


def test_find_regens_reports_position_match_without_excluding_difference() -> None:
    catalog = InMemoryCatalog()
    catalog.replace_players(
        (
            player("p-same-position", position="ST"),
            player("p-different-position", position="CM"),
        )
    )

    matches = FindRegensService(catalog).execute(
        FindRegensQuery(date(1998, 4, 12), "Spain", " st ")
    )

    assert [match.player.id for match in matches] == [
        "p-different-position",
        "p-same-position",
    ]
    assert [match.position_matches for match in matches] == [False, True]
    assert matches[1].message == (
        "Posible regen: coinciden fecha de nacimiento, nacionalidad y posición."
    )
    assert matches[0].message == (
        "Posible regen: coinciden fecha de nacimiento y nacionalidad, "
        "pero no la posición."
    )


def test_find_regens_excludes_overall_below_85_and_includes_85() -> None:
    catalog = InMemoryCatalog()
    catalog.replace_players(
        (
            player("p-below-threshold", overall=84),
            player("p-at-threshold", overall=85),
        )
    )

    matches = FindRegensService(catalog).execute(
        FindRegensQuery(date(1998, 4, 12), "Spain")
    )

    assert [match.player.id for match in matches] == ["p-at-threshold"]
    assert matches[0].player.overall == 85


def test_find_regens_orders_by_overall_age_then_id() -> None:
    catalog = InMemoryCatalog()
    catalog.replace_players(
        (
            player("p-z", overall=90, age=30),
            player("p-b", overall=85, age=24),
            player("p-a", overall=85, age=24),
            player("p-younger", overall=90, age=25),
            player("p-older", overall=90, age=31),
        )
    )

    matches = FindRegensService(catalog).execute(
        FindRegensQuery(date(1998, 4, 12), "Spain")
    )

    assert [match.player.id for match in matches] == [
        "p-older",
        "p-z",
        "p-younger",
        "p-a",
        "p-b",
    ]