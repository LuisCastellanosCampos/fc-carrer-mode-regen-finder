from fastapi.testclient import TestClient

from BACKEND.adapters.outbound.in_memory_catalog import InMemoryCatalog
from BACKEND.domain.exceptions.errors import CatalogUnavailableError
from BACKEND.main import create_app


def player_payload(player_id: str = "p-1") -> dict[str, object]:
    return {
        "id": player_id,
        "name": "Alejandro Ruiz",
        "birth_date": "1998-04-12",
        "nationality": "Spain",
        "position": "ST",
        "overall": 87,
        "age": 24,
    }


class UnavailableCatalog(InMemoryCatalog):
    def read_players(self):
        raise CatalogUnavailableError("El catálogo no está disponible")


class BrokenCatalog(InMemoryCatalog):
    def read_players(self):
        raise RuntimeError("database exploded")


def test_invalid_query_returns_bad_request_in_spanish() -> None:
    client = TestClient(create_app(InMemoryCatalog()))

    response = client.get(
        "/api/v1/regens",
        params={"birth_date": "1998-02-30", "nationality": "Spain"},
    )

    assert response.status_code == 400
    assert "fecha" in response.json()["detail"].lower()


def test_invalid_catalog_update_returns_bad_request_without_partial_changes() -> None:
    catalog = InMemoryCatalog()
    client = TestClient(create_app(catalog))
    client.put(
        "/api/v1/players/catalog",
        json={"season": "2026", "players": [player_payload()]},
    )

    response = client.put(
        "/api/v1/players/catalog",
        json={
            "season": "2027",
            "players": [player_payload("p-2"), player_payload("p-2")],
        },
    )

    assert response.status_code == 400
    assert "duplicado" in response.json()["detail"].lower()
    assert [player.id for player in catalog.read_players()] == ["p-1"]


def test_older_catalog_update_returns_conflict() -> None:
    catalog = InMemoryCatalog()
    client = TestClient(create_app(catalog))
    client.put(
        "/api/v1/players/catalog",
        json={"season": "2026", "players": [player_payload()]},
    )

    response = client.put(
        "/api/v1/players/catalog",
        json={"season": "2025", "players": [player_payload()]},
    )

    assert response.status_code == 409
    assert "temporada" in response.json()["detail"].lower()


def test_unavailable_catalog_returns_service_unavailable() -> None:
    client = TestClient(create_app(UnavailableCatalog()), raise_server_exceptions=False)

    response = client.get(
        "/api/v1/regens",
        params={"birth_date": "1998-04-12", "nationality": "Spain"},
    )

    assert response.status_code == 503
    assert "catálogo" in response.json()["detail"].lower()


def test_unexpected_catalog_failure_returns_internal_server_error() -> None:
    client = TestClient(create_app(BrokenCatalog()), raise_server_exceptions=False)

    response = client.get(
        "/api/v1/regens",
        params={"birth_date": "1998-04-12", "nationality": "Spain"},
    )

    assert response.status_code == 500
    assert response.json()["detail"] == "Error interno del servidor."