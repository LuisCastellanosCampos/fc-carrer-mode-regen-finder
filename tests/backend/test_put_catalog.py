from fastapi.testclient import TestClient

from BACKEND.adapters.outbound.in_memory_catalog import InMemoryCatalog
from BACKEND.main import create_app


def player_payload(player_id: str, overall: int = 87) -> dict[str, object]:
    return {
        "id": player_id,
        "name": "Alejandro Ruiz",
        "birth_date": "1998-04-12",
        "nationality": "Spain",
        "position": "ST",
        "overall": overall,
        "age": 24,
    }


def test_put_catalog_returns_inserted_and_updated_summary() -> None:
    catalog = InMemoryCatalog()
    client = TestClient(create_app(catalog))

    response = client.put(
        "/api/v1/players/catalog",
        json={
            "season": "2026",
            "players": [player_payload("p-1"), player_payload("p-2")],
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "season": "2026",
        "inserted": 2,
        "updated": 0,
    }


def test_put_catalog_updates_players_by_id() -> None:
    catalog = InMemoryCatalog()
    client = TestClient(create_app(catalog))
    client.put(
        "/api/v1/players/catalog",
        json={
            "season": "2026",
            "players": [player_payload("p-1", overall=80)],
        },
    )

    response = client.put(
        "/api/v1/players/catalog",
        json={
            "season": "2027",
            "players": [player_payload("p-1", overall=91)],
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "season": "2027",
        "inserted": 0,
        "updated": 1,
    }
    assert catalog.read_players()[0].overall == 91