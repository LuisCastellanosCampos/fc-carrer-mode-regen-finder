from pathlib import Path

import pytest

from BACKEND.domain.exceptions.errors import ValidationError
from BACKEND.domain.services.sofifa_runner import SofifaRunner


def test_sofifa_runner_writes_raw_artifact_and_returns_records(tmp_path: Path) -> None:
    raw_dir = tmp_path / "data" / "raw" / "2026"
    raw_dir.mkdir(parents=True)
    artifact = raw_dir / "sofifa.json"
    artifact.write_text('[{"id":"1","name":"Player One"}]', encoding="utf-8")

    runner = SofifaRunner(output_dir=tmp_path / "data" / "raw")
    result = runner.run(season="2026", page_limit=10, payload='[{"id":"1","name":"Player One"}]')

    assert result == [{"id": "1", "name": "Player One"}]
    assert artifact.exists()
    assert artifact.read_text(encoding="utf-8") == '[{"id":"1","name":"Player One"}]'


def test_sofifa_runner_rejects_invalid_season_or_page_limit() -> None:
    runner = SofifaRunner(output_dir=Path("data/raw"))

    with pytest.raises(ValidationError, match="temporada"):
        runner.run(season="", page_limit=10, payload='[]')

    with pytest.raises(ValidationError, match="páginas"):
        runner.run(season="2026", page_limit=0, payload='[]')


def test_sofifa_runner_rejects_empty_payload() -> None:
    runner = SofifaRunner(output_dir=Path("data/raw"))

    with pytest.raises(ValidationError, match="vacío"):
        runner.run(season="2026", page_limit=10, payload='')

    with pytest.raises(ValidationError, match="vacío"):
        runner.run(season="2026", page_limit=10, payload='[]')
