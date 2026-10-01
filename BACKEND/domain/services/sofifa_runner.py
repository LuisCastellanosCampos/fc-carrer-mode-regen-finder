import json
from pathlib import Path

from BACKEND.domain.exceptions.errors import ValidationError


class SofifaRunner:
    """Guarda el artefacto original de Sofifa sin tocar el catálogo local."""

    def __init__(self, output_dir: str | Path) -> None:
        self.output_dir = Path(output_dir)

    def run(self, *, season: str, page_limit: int, payload: str) -> list[dict]:
        self._validate_season(season)
        self._validate_page_limit(page_limit)
        self._validate_payload(payload)

        records = json.loads(payload)
        if not isinstance(records, list):
            raise ValidationError("El payload del scraper debe ser una lista JSON")

        season_dir = self.output_dir / season
        season_dir.mkdir(parents=True, exist_ok=True)
        artifact_path = season_dir / "sofifa.json"
        artifact_path.write_text(payload, encoding="utf-8")

        return records

    @staticmethod
    def _validate_season(season: str) -> None:
        if not isinstance(season, str) or not season.strip():
            raise ValidationError("La temporada del catálogo no puede estar vacía")

    @staticmethod
    def _validate_page_limit(page_limit: int) -> None:
        if isinstance(page_limit, bool) or not isinstance(page_limit, int):
            raise ValidationError("El límite de páginas debe ser un entero positivo")
        if page_limit <= 0:
            raise ValidationError("El límite de páginas debe ser un entero positivo")

    @staticmethod
    def _validate_payload(payload: str) -> None:
        if not isinstance(payload, str) or not payload.strip():
            raise ValidationError("El payload del scraper no puede estar vacío")
        if payload.strip() == "[]":
            raise ValidationError("El payload del scraper no puede estar vacío")
