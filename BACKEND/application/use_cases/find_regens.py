from unicodedata import normalize

from BACKEND.application.ports.catalog import CatalogPort
from BACKEND.application.ports.use_cases import FindRegensQuery, FindRegensResult
from BACKEND.domain.entities.regen_match import RegenMatch


class FindRegensService:
    """Encuentra jugadores que coinciden exactamente en fecha y nacionalidad."""

    _no_matches_message = "No se encontraron posibles regens."

    def __init__(self, catalog: CatalogPort) -> None:
        self._catalog = catalog

    def execute(self, query: FindRegensQuery) -> FindRegensResult:
        matches: list[RegenMatch] = []
        for player in self._catalog.read_players():
            birth_date_matches = player.birth_date == query.birth_date
            nationality_matches = self._normalize(player.nationality) == query.nationality

            if (
                birth_date_matches
                and nationality_matches
                and player.overall >= 85
            ):
                position_matches = None
                if query.position is not None:
                    position_matches = (
                        self._normalize(player.position) == query.position
                    )

                if position_matches is True:
                    message = (
                        "Posible regen: coinciden fecha de nacimiento, "
                        "nacionalidad y posición."
                    )
                elif position_matches is False:
                    message = (
                        "Posible regen: coinciden fecha de nacimiento y "
                        "nacionalidad, pero no la posición."
                    )
                else:
                    message = (
                        "Posible regen: coinciden fecha de nacimiento "
                        "y nacionalidad."
                    )

                matches.append(
                    RegenMatch(
                        player=player,
                        birth_date_matches=True,
                        nationality_matches=True,
                        position_matches=position_matches,
                        is_possible_regen=True,
                        message=message,
                    )
                )

        matches.sort(
            key=lambda match: (
                -match.player.overall,
                -match.player.age,
                match.player.id,
            )
        )
        message = self._no_matches_message if not matches else None
        return FindRegensResult(tuple(matches), message)

    @staticmethod
    def _normalize(value: str) -> str:
        return normalize("NFKC", value).strip().casefold()