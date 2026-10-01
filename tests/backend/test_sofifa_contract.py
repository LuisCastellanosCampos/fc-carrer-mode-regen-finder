from datetime import date

import pytest

from BACKEND.domain.entities.player import Player
from BACKEND.domain.exceptions.errors import ValidationError
from BACKEND.domain.services.sofifa_contract import SofifaContract


def test_sofifa_contract_maps_valid_payload_to_player() -> None:
    contract = SofifaContract()
    payload = {
        "id": "12345",
        "name": "Lionel Messi",
        "birth_date": "1990-01-01",
        "nationality": "Argentina",
        "position": "RW, CF",
        "overall": "92",
        "age": "35",
        "season": "2026",
    }

    player = contract.to_player(payload)

    assert isinstance(player, Player)
    assert player.id == "12345"
    assert player.name == "Lionel Messi"
    assert player.birth_date == date(1990, 1, 1)
    assert player.nationality == "Argentina"
    assert player.position == "RW, CF"
    assert player.overall == 92
    assert player.age == 35
    assert player.season == "2026"


def test_sofifa_contract_requires_required_fields_and_valid_date() -> None:
    contract = SofifaContract()

    with pytest.raises(ValidationError, match="id"):
        contract.to_player({
            "name": "Player",
            "birth_date": "1990-01-01",
            "nationality": "Argentina",
            "position": "RW",
            "overall": "90",
            "age": "30",
            "season": "2026",
        })

    with pytest.raises(ValidationError, match="fecha"):
        contract.to_player({
            "id": "123",
            "name": "Player",
            "birth_date": "not-a-date",
            "nationality": "Argentina",
            "position": "RW",
            "overall": "90",
            "age": "30",
            "season": "2026",
        })

    with pytest.raises(ValidationError, match="nat|nacionalidad"):
        contract.to_player({
            "id": "123",
            "name": "Player",
            "birth_date": "1990-01-01",
            "nationality": "",
            "position": "RW",
            "overall": "90",
            "age": "30",
            "season": "2026",
        })


def test_sofifa_contract_normalizes_multiple_positions_and_numeric_values() -> None:
    contract = SofifaContract()
    payload = {
        "id": "777",
        "name": "A. Player",
        "birth_date": "2001-02-03",
        "nationality": "  Spain  ",
        "position": "  ST, CF  ",
        "overall": " 87 ",
        "age": " 24 ",
        "season": "2026",
    }

    player = contract.to_player(payload)

    assert player.nationality == "Spain"
    assert player.position == "ST, CF"
    assert player.overall == 87
    assert player.age == 24


def test_sofifa_contract_handles_missing_optional_values_and_rejects_invalid_overall() -> None:
    contract = SofifaContract()

    payload = {
        "id": "77",
        "name": "A",
        "birth_date": "2001-02-03",
        "nationality": "Spain",
        "position": "ST",
        "overall": "101",
        "age": "24",
        "season": "2026",
    }

    with pytest.raises(ValidationError, match="overall|0 y 100"):
        contract.to_player(payload)

    missing = {
        "id": "77",
        "name": "A",
        "birth_date": "2001-02-03",
        "nationality": "Spain",
        "position": "ST",
        "overall": "80",
        "age": "24",
    }

    with pytest.raises(ValidationError, match="season|temporada"):
        contract.to_player(missing)
