from unicodedata import normalize

from BACKEND.application.ports.catalog import CatalogPort
from BACKEND.application.ports.use_cases import FindRegensQuery
from BACKEND.domain.entities.regen_match import RegenMatch


class FindRegensService:
    """Encuentra jugadores que coinciden exactamente en fecha y nacionalidad."""

    def __init__(self, catalog: CatalogPort) -> None:
        self._catalog = catalog

    def execute(self, query: FindRegensQuery) -> tuple[RegenMatch, ...]:
        matches: list[RegenMatch] = []
        for player in self._catalog.read_players():
            birth_date_matches = player.birth_date == query.birth_date
            nationality_matches = self._normalize(player.nationality) == query.nationality

            if birth_date_matches and nationality_matches:
                matches.append(
                    RegenMatch(
                        player=player,
                        birth_date_matches=True,
                        nationality_matches=True,
                        position_matches=None,
                        is_possible_regen=True,
                        message=(
                            "Posible regen: coinciden fecha de nacimiento "
                            "y nacionalidad."
                        ),
                    )
                )

        return tuple(matches)

    @staticmethod
    def _normalize(value: str) -> str:
        return normalize("NFKC", value).strip().casefold()