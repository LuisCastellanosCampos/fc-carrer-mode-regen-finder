import pytest

from BACKEND.domain.entities.player import Player
from BACKEND.domain.exceptions.errors import ValidationError
from BACKEND.domain.services.sofifa_transformer import SofifaTransformer


def test_sofifa_transformer_builds_valid_players_from_raw_records() -> None:
    transformer = SofifaTransformer()
    rows = [
        {
            "id": "1001",
            "name": "Player One",
            "birth_date": "2001-02-03",
            "nationality": "Spain",
            "position": "ST, CF",
            "overall": "87",
            "age": "24",
            "season": "2026",
        },
        {
            "id": "1002",
            "name": "Player Two",
            "birth_date": "1998-11-10",
            "nationality": "Argentina",
            "position": "CM",
            "overall": 90,
            "age": 28,
            "season": "2026",
        },
    ]

    players = transformer.to_players(rows)

    assert players == (
        Player(
            id="1001",
            name="Player One",
            birth_date=__import__("datetime").date(2001, 2, 3),
            nationality="Spain",
            position="ST, CF",
            overall=87,
            age=24,
            season="2026",
        ),
        Player(
            id="1002",
            name="Player Two",
            birth_date=__import__("datetime").date(1998, 11, 10),
            nationality="Argentina",
            position="CM",
            overall=90,
            age=28,
            season="2026",
        ),
    )


def test_sofifa_transformer_rejects_missing_and_invalid_data() -> None:
    transformer = SofifaTransformer()

    with pytest.raises(ValidationError, match="id"):
        transformer.to_players([{"name": "No id"}])

    with pytest.raises(ValidationError, match="fecha"):
        transformer.to_players([
            {
                "id": "12",
                "name": "Bad date",
                "birth_date": "bad-date",
                "nationality": "Spain",
                "position": "ST",
                "overall": 85,
                "age": 24,
                "season": "2026",
            }
        ])

    with pytest.raises(ValidationError, match="overall|0 y 100"):
        transformer.to_players([
            {
                "id": "13",
                "name": "Bad overall",
                "birth_date": "2000-01-01",
                "nationality": "Spain",
                "position": "ST",
                "overall": 140,
                "age": 24,
                "season": "2026",
            }
        ])


def test_sofifa_transformer_rejects_duplicate_ids_and_ambiguous_rows() -> None:
    transformer = SofifaTransformer()

    with pytest.raises(ValidationError, match="duplicado"):
        transformer.to_players([
            {
                "id": "dup",
                "name": "A",
                "birth_date": "2000-01-01",
                "nationality": "Spain",
                "position": "ST",
                "overall": 85,
                "age": 24,
                "season": "2026",
            },
            {
                "id": "dup",
                "name": "B",
                "birth_date": "2000-01-02",
                "nationality": "Spain",
                "position": "ST",
                "overall": 85,
                "age": 24,
                "season": "2026",
            },
        ])

    with pytest.raises(ValidationError, match="ambig|ambiguous"):
        transformer.to_players([
            {
                "id": "15",
                "name": "A",
                "birth_date": "2000-01-01",
                "nationality": "Spain",
                "position": "ST, CF",
                "overall": 85,
                "age": 24,
                "season": "2026",
            },
            {
                "id": "16",
                "name": "B",
                "birth_date": "2000-01-01",
                "nationality": "Spain",
                "position": "CM",
                "overall": 85,
                "age": 24,
                "season": "2026",
            },
        ])
