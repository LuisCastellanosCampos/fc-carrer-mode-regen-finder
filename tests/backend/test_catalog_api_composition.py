from datetime import date

from fastapi.testclient import TestClient

from BACKEND import main
from BACKEND.adapters.outbound.in_memory_catalog import InMemoryCatalog
from BACKEND.adapters.outbound.sqlite_catalog import SQLiteCatalog


class FalseyCatalog(InMemoryCatalog):
    def __bool__(self) -> bool:
        return False


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


def test_default_api_composition_persists_imported_catalog(
    tmp_path, monkeypatch
) -> None:
    database_path = tmp_path / "catalog.db"
    monkeypatch.setattr(
        main,
        "SQLiteCatalog",
        lambda: SQLiteCatalog(database_path),
    )

    import_client = TestClient(main.create_app())
    import_response = import_client.put(
        "/api/v1/players/catalog",
        json={"season": "2026", "players": [player_payload("p-1")]},
    )

    assert import_response.status_code == 200
    assert import_response.json() == {
        "season": "2026",
        "inserted": 1,
        "updated": 0,
    }

    query_client = TestClient(main.create_app())
    query_response = query_client.get(
        "/api/v1/regens",
        params={
            "birth_date": date(1998, 4, 12).isoformat(),
            "nationality": "Spain",
            "position": "ST",
        },
    )

    assert query_response.status_code == 200
    assert [match["player"]["id"] for match in query_response.json()["matches"]] == [
        "p-1"
    ]


def test_api_rejects_duplicate_import_without_changing_persisted_catalog(
    tmp_path, monkeypatch
) -> None:
    database_path = tmp_path / "catalog.db"
    monkeypatch.setattr(
        main,
        "SQLiteCatalog",
        lambda: SQLiteCatalog(database_path),
    )
    client = TestClient(main.create_app())
    existing_player = player_payload("p-existing")

    initial_response = client.put(
        "/api/v1/players/catalog",
        json={"season": "2026", "players": [existing_player]},
    )
    invalid_response = client.put(
        "/api/v1/players/catalog",
        json={
            "season": "2026",
            "players": [player_payload("p-new"), player_payload("p-new")],
        },
    )
    query_response = client.get(
        "/api/v1/regens",
        params={"birth_date": "1998-04-12", "nationality": "Spain"},
    )

    assert initial_response.status_code == 200
    assert invalid_response.status_code == 400
    assert invalid_response.json()["detail"] == "ID duplicado en la colección: p-new"
    assert [match["player"]["id"] for match in query_response.json()["matches"]] == [
        "p-existing"
    ]


def test_api_keeps_an_injected_catalog_even_when_it_is_falsey(
    tmp_path, monkeypatch
) -> None:
    catalog = FalseyCatalog()
    monkeypatch.setattr(
        main,
        "SQLiteCatalog",
        lambda: SQLiteCatalog(tmp_path / "catalog.db"),
    )
    client = TestClient(main.create_app(catalog))

    response = client.put(
        "/api/v1/players/catalog",
        json={"season": "2026", "players": [player_payload("p-1")]},
    )

    assert response.status_code == 200
    assert [player.id for player in catalog.read_players()] == ["p-1"]
