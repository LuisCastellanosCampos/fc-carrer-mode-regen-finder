from datetime import date

from fastapi.testclient import TestClient

from BACKEND.adapters.outbound.in_memory_catalog import InMemoryCatalog
from BACKEND.domain.entities.player import Player
from BACKEND.main import create_app


def player(
    player_id: str,
    *,
    overall: int = 85,
    age: int = 24,
    position: str = "ST",
) -> Player:
    return Player(
        id=player_id,
        name=f"Player {player_id}",
        birth_date=date(1998, 4, 12),
        nationality="Spain",
        position=position,
        overall=overall,
        age=age,
        season="2026",
    )


def test_get_regens_returns_ordered_matches_and_query() -> None:
    catalog = InMemoryCatalog()
    catalog.replace_players(
        (
            player("p-younger", overall=90, age=24),
            player("p-older", overall=90, age=25),
        )
    )
    client = TestClient(create_app(catalog))

    response = client.get(
        "/api/v1/regens",
        params={
            "birth_date": "1998-04-12",
            "nationality": "Spain",
            "position": "ST",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "query": {
            "birth_date": "1998-04-12",
            "nationality": "Spain",
            "position": "ST",
        },
        "matches": [
            {
                "player": {
                    "id": "p-older",
                    "name": "Player p-older",
                    "birth_date": "1998-04-12",
                    "nationality": "Spain",
                    "position": "ST",
                    "overall": 90,
                    "age": 25,
                    "season": "2026",
                },
                "match": {
                    "birth_date": True,
                    "nationality": True,
                    "position": True,
                    "is_possible_regen": True,
                    "message": (
                        "Posible regen: coinciden fecha de nacimiento, "
                        "nacionalidad y posición."
                    ),
                },
            },
            {
                "player": {
                    "id": "p-younger",
                    "name": "Player p-younger",
                    "birth_date": "1998-04-12",
                    "nationality": "Spain",
                    "position": "ST",
                    "overall": 90,
                    "age": 24,
                    "season": "2026",
                },
                "match": {
                    "birth_date": True,
                    "nationality": True,
                    "position": True,
                    "is_possible_regen": True,
                    "message": (
                        "Posible regen: coinciden fecha de nacimiento, "
                        "nacionalidad y posición."
                    ),
                },
            },
        ],
        "message": None,
    }


def test_get_regens_accepts_query_without_position() -> None:
    catalog = InMemoryCatalog()
    catalog.replace_players((player("p-1", position="CM"),))
    client = TestClient(create_app(catalog))

    response = client.get(
        "/api/v1/regens",
        params={"birth_date": "1998-04-12", "nationality": "Spain"},
    )

    assert response.status_code == 200
    assert response.json()["query"] == {
        "birth_date": "1998-04-12",
        "nationality": "Spain",
        "position": None,
    }
    assert response.json()["matches"][0]["match"]["position"] is None


def test_get_regens_returns_empty_list_and_message() -> None:
    client = TestClient(create_app(InMemoryCatalog()))

    response = client.get(
        "/api/v1/regens",
        params={"birth_date": "1998-04-12", "nationality": "Spain"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "query": {
            "birth_date": "1998-04-12",
            "nationality": "Spain",
            "position": None,
        },
        "matches": [],
        "message": "No se encontraron posibles regens.",
    }