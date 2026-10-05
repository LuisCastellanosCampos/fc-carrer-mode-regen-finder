import json
from datetime import date

import pytest
from fastapi.testclient import TestClient
from requests.exceptions import ConnectionError, HTTPError, Timeout

from BACKEND.adapters.outbound.sofifa_scraper import SofifaScraperAdapter
from BACKEND.adapters.outbound.sqlite_catalog import SQLiteCatalog
from BACKEND.domain.entities.player import Player
from BACKEND.domain.exceptions.errors import ValidationError
from BACKEND.domain.services.sofifa_runner import SofifaRunner
from BACKEND.domain.services.sofifa_transformer import SofifaTransformer
from BACKEND.main import create_app


def raw_player(
    player_id: str = "p-1",
    *,
    birth_date: str = "1998-04-12",
    nationality: str = "Spain",
    position: str = "ST, CF",
) -> dict[str, object]:
    return {
        "id": player_id,
        "name": "Alejandro Ruiz",
        "birth_date": birth_date,
        "nationality": nationality,
        "position": position,
        "overall": 87,
        "age": 24,
        "season": "2026",
    }


def api_player(player: Player) -> dict[str, object]:
    return {
        "id": player.id,
        "name": player.name,
        "birth_date": player.birth_date.isoformat(),
        "nationality": player.nationality,
        "position": player.position,
        "overall": player.overall,
        "age": player.age,
    }


def test_sofifa_scraper_adapter_saves_and_returns_payload(tmp_path) -> None:
    payload = json.dumps([raw_player()])
    calls: list[tuple[str, int]] = []
    runner = SofifaRunner(tmp_path / "raw")
    adapter = SofifaScraperAdapter(
        scraper=lambda season, page_limit: (
            calls.append((season, page_limit)) or payload
        ),
        runner=runner,
    )

    records = adapter.run(season="2026", page_limit=10)

    assert calls == [("2026", 10)]
    assert records == [raw_player()]
    assert (tmp_path / "raw" / "2026" / "sofifa.json").read_text(
        encoding="utf-8"
    ) == payload


@pytest.mark.parametrize(
    ("scraper_error", "message"),
    [
        (ConnectionError("offline"), "red"),
        (Timeout("timed out"), "red"),
        (HTTPError("503 Server Error"), "HTTP"),
    ],
)
def test_sofifa_scraper_adapter_returns_controlled_network_errors(
    tmp_path, scraper_error: Exception, message: str
) -> None:
    runner = SofifaRunner(tmp_path / "raw")

    def failing_scraper(season: str, page_limit: int) -> str:
        raise scraper_error

    adapter = SofifaScraperAdapter(scraper=failing_scraper, runner=runner)

    with pytest.raises(ValidationError, match=message):
        adapter.run(season="2026", page_limit=10)

    assert not (tmp_path / "raw" / "2026" / "sofifa.json").exists()


def test_sofifa_pipeline_rejects_empty_response_without_writing_artifact(
    tmp_path,
) -> None:
    adapter = SofifaScraperAdapter(
        scraper=lambda season, page_limit: "[]",
        runner=SofifaRunner(tmp_path / "raw"),
    )

    with pytest.raises(ValidationError, match="vacío"):
        adapter.run(season="2026", page_limit=10)

    assert not (tmp_path / "raw" / "2026" / "sofifa.json").exists()


def test_sofifa_pipeline_imports_validated_records_and_recovers_after_app_restart(
    tmp_path,
) -> None:
    raw_dir = tmp_path / "raw"
    payload = json.dumps([raw_player(position="ST, CF")])
    adapter = SofifaScraperAdapter(
        scraper=lambda season, page_limit: payload,
        runner=SofifaRunner(raw_dir),
    )
    records = adapter.run(season="2026", page_limit=10)
    players = SofifaTransformer().to_players(records)
    database_path = tmp_path / "catalog.db"
    first_client = TestClient(create_app(SQLiteCatalog(database_path)))

    import_response = first_client.put(
        "/api/v1/players/catalog",
        json={
            "season": "2026",
            "players": [api_player(player) for player in players],
        },
    )

    assert import_response.status_code == 200
    assert import_response.json() == {
        "season": "2026",
        "inserted": 1,
        "updated": 0,
    }

    restarted_client = TestClient(create_app(SQLiteCatalog(database_path)))
    query_response = restarted_client.get(
        "/api/v1/regens",
        params={
            "birth_date": date(1998, 4, 12).isoformat(),
            "nationality": "Spain",
            "position": "ST, CF",
        },
    )

    assert query_response.status_code == 200
    assert [
        match["player"]["id"] for match in query_response.json()["matches"]
    ] == ["p-1"]


@pytest.mark.parametrize(
    "records",
    [
        [{key: value for key, value in raw_player().items() if key != "birth_date"}],
        [raw_player(birth_date="not-a-date")],
        [raw_player("duplicate"), raw_player("duplicate")],
        [
            raw_player("p-1", position="ST"),
            raw_player("p-2", position="CF"),
        ],
    ],
)
def test_sofifa_pipeline_rejects_invalid_records_before_catalog_import(
    tmp_path, records: list[dict[str, object]]
) -> None:
    database_path = tmp_path / "catalog.db"
    client = TestClient(create_app(SQLiteCatalog(database_path)))
    seed_response = client.put(
        "/api/v1/players/catalog",
        json={
            "season": "2026",
            "players": [
                {
                    "id": "p-existing",
                    "name": "Existing Player",
                    "birth_date": "1998-04-12",
                    "nationality": "Spain",
                    "position": "ST",
                    "overall": 87,
                    "age": 24,
                }
            ],
        },
    )
    adapter = SofifaScraperAdapter(
        scraper=lambda season, page_limit: json.dumps(records),
        runner=SofifaRunner(tmp_path / "raw"),
    )

    assert seed_response.status_code == 200

    with pytest.raises(ValidationError):
        transformed = adapter.run(season="2026", page_limit=10)
        players = SofifaTransformer().to_players(transformed)
        client.put(
            "/api/v1/players/catalog",
            json={
                "season": "2026",
                "players": [api_player(player) for player in players],
            },
        )

    persisted_client = TestClient(create_app(SQLiteCatalog(database_path)))
    query_response = persisted_client.get(
        "/api/v1/regens",
        params={"birth_date": "1998-04-12", "nationality": "Spain"},
    )

    assert [
        match["player"]["id"] for match in query_response.json()["matches"]
    ] == ["p-existing"]
