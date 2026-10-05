from collections.abc import Callable

from requests.exceptions import HTTPError, RequestException

from BACKEND.domain.exceptions.errors import ValidationError
from BACKEND.domain.services.sofifa_runner import SofifaRunner


class SofifaScraperAdapter:
    """Ejecuta el scraper externo y guarda su salida sin alterar el catálogo."""

    def __init__(
        self,
        *,
        scraper: Callable[[str, int], str],
        runner: SofifaRunner,
    ) -> None:
        self._scraper = scraper
        self._runner = runner

    def run(self, *, season: str, page_limit: int) -> list[dict]:
        self._runner.validate_request(season=season, page_limit=page_limit)

        try:
            payload = self._scraper(season, page_limit)
        except HTTPError as exc:
            raise ValidationError(
                "El scraper de Sofifa devolvió un error HTTP"
            ) from exc
        except RequestException as exc:
            raise ValidationError(
                "Falló la comunicación de red con el scraper de Sofifa"
            ) from exc

        return self._runner.run(
            season=season,
            page_limit=page_limit,
            payload=payload,
        )
