from datetime import date

import pytest

from BACKEND.domain.entities.player import Player
from BACKEND.domain.exceptions.errors import ValidationError


def valid_player(**overrides: object) -> Player:
    values: dict[str, object] = {
        "id": "p-1042",
        "name": "Alejandro Ruiz",
        "birth_date": date(1998, 4, 12),
        "nationality": "Spain",
        "position": "ST",
        "overall": 87,
        "age": 24,
        "season": "2026",
    }
    values.update(overrides)
    return Player(**values)


def test_player_contains_the_active_player_contract() -> None:
    player = valid_player()

    assert player.id == "p-1042"
    assert player.name == "Alejandro Ruiz"
    assert player.birth_date == date(1998, 4, 12)
    assert player.nationality == "Spain"
    assert player.position == "ST"
    assert player.overall == 87
    assert player.age == 24
    assert player.season == "2026"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("id", ""),
        ("name", ""),
        ("nationality", ""),
        ("position", ""),
        ("season", ""),
    ],
)
def test_player_rejects_empty_required_text(field: str, value: str) -> None:
    with pytest.raises(ValueError, match="no puede estar vacío"):
        valid_player(**{field: value})


@pytest.mark.parametrize("overall", [-1, 101, True])
def test_player_rejects_invalid_overall(overall: object) -> None:
    with pytest.raises(ValueError, match="overall"):
        valid_player(overall=overall)


@pytest.mark.parametrize("age", [-1, True])
def test_player_rejects_invalid_age(age: object) -> None:
    with pytest.raises(ValueError, match="edad"):
        valid_player(age=age)


def test_player_rejects_invalid_birth_date() -> None:
    with pytest.raises(ValueError, match="fecha de nacimiento"):
        valid_player(birth_date="1998-04-12")


@pytest.mark.parametrize(
    ("field", "message_fragment"),
    [
        ("id", "id"),
        ("name", "nombre"),
        ("birth_date", "fecha de nacimiento"),
        ("nationality", "nacionalidad"),
        ("overall", "overall"),
        ("age", "edad"),
    ],
)
def test_player_rejects_missing_required_fields(
    field: str, message_fragment: str
) -> None:
    values: dict[str, object] = {
        "id": "p-1042",
        "name": "Alejandro Ruiz",
        "birth_date": date(1998, 4, 12),
        "nationality": "Spain",
        "position": "ST",
        "overall": 87,
        "age": 24,
        "season": "2026",
    }
    values.pop(field)

    with pytest.raises(ValidationError, match=message_fragment):
        Player(**values)
