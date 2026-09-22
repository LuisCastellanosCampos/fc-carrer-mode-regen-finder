from fastapi.testclient import TestClient

from BACKEND.adapters.outbound.in_memory_catalog import InMemoryCatalog
from BACKEND.main import create_app


def test_regen_search_requires_birth_date_and_nationality() -> None:
    client = TestClient(create_app(InMemoryCatalog()))

    response = client.get("/api/v1/regens")

    assert response.status_code == 400
    assert response.json()["detail"] == "La fecha de nacimiento es inválida."


def test_catalog_update_rejects_payload_without_required_season() -> None:
    client = TestClient(create_app(InMemoryCatalog()))

    response = client.put(
        "/api/v1/players/catalog",
        json={"players": []},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "La petición es inválida."