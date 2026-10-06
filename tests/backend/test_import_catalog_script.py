from fastapi.testclient import TestClient

from BACKEND.main import create_app
from BACKEND.adapters.outbound.in_memory_catalog import InMemoryCatalog
from scripts.import_catalog import load_payload


def test_example_csv_can_be_sent_to_catalog_api() -> None:
    payload = load_payload()
    client = TestClient(create_app(InMemoryCatalog()))

    response = client.put("/api/v1/players/catalog", json=payload)

    assert response.status_code == 200
    assert response.json()["season"] == "2026"
    assert response.json()["inserted"] == len(payload["players"])
