"""
Application Use Case: FindRegensUseCase
Core business logic to find regen candidates for legendary players.
"""
from src.domain.entities.regen import Regen
from src.domain.ports.player_repository import PlayerRepository
from src.domain.ports.regen_repository import RegenRepository


class FindRegensUseCase:
    """
    Given the list of legendary/retired players, find potential regens
    among younger players by crossing nationality and birth date data.
    """

    def __init__(
        self,
        player_repo: PlayerRepository,
        regen_repo: RegenRepository,
        season: str,
        min_match_score: float = 0.85,
    ) -> None:
        self._player_repo = player_repo
        self._regen_repo = regen_repo
        self._season = season
        self._min_match_score = min_match_score

    async def execute(self) -> list[Regen]:
        """
        Entry point for the use case.
        Returns all confirmed regen matches for the current season.
        """
        legendaries = await self._player_repo.find_legendaries()
        regens: list[Regen] = []

        for legend in legendaries:
            candidates = await self._player_repo.find_by_nationality_and_birth_date(
                nationality=legend.nationality,
                birth_date=legend.birth_date,
            )

            for candidate in candidates:
                if candidate.id == legend.id:
                    continue  # skip the legend itself

                score = self._compute_match_score(legend, candidate)
                if score >= self._min_match_score:
                    regen = Regen(
                        legendary_player=legend,
                        regen_candidate=candidate,
                        match_score=score,
                        season=self._season,
                    )
                    await self._regen_repo.save(regen)
                    regens.append(regen)

        return regens

    def _compute_match_score(self, legend, candidate) -> float:
        """
        Simple heuristic: both nationality and birth_date must match.
        Future versions can include position, stats similarity, etc.
        """
        score = 0.0
        if legend.nationality == candidate.nationality:
            score += 0.5
        if legend.birth_date == candidate.birth_date:
            score += 0.5
        return score
