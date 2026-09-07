"""
Unit tests for the FindRegensUseCase.
"""
import pytest
from datetime import date

from src.domain.entities.player import Player
from src.infrastructure.persistence.in_memory.player_repository import InMemoryPlayerRepository
from src.infrastructure.persistence.in_memory.regen_repository import InMemoryRegenRepository
from src.application.use_cases.find_regens import FindRegensUseCase


@pytest.fixture
def legend() -> Player:
    return Player(
        id="legend-1",
        name="Ronaldinho",
        nationality="Brazil",
        birth_date=date(1980, 3, 21),
        overall_rating=95,
        position="CAM",
        is_legendary=True,
    )


@pytest.fixture
def regen_candidate() -> Player:
    return Player(
        id="regen-1",
        name="Unknown Brazilian",
        nationality="Brazil",
        birth_date=date(1980, 3, 21),
        overall_rating=60,
        position="CAM",
        is_legendary=False,
    )


@pytest.fixture
def no_match_player() -> Player:
    return Player(
        id="nomatch-1",
        name="Other Player",
        nationality="Argentina",
        birth_date=date(1985, 6, 15),
        overall_rating=70,
        position="ST",
        is_legendary=False,
    )


@pytest.mark.asyncio
async def test_find_regens_returns_confirmed_match(legend, regen_candidate):
    player_repo = InMemoryPlayerRepository()
    regen_repo = InMemoryRegenRepository()

    await player_repo.save(legend)
    await player_repo.save(regen_candidate)

    use_case = FindRegensUseCase(
        player_repo=player_repo,
        regen_repo=regen_repo,
        season="2024/2025",
    )

    regens = await use_case.execute()

    assert len(regens) == 1
    assert regens[0].legendary_player.id == "legend-1"
    assert regens[0].regen_candidate.id == "regen-1"
    assert regens[0].match_score == 1.0
    assert regens[0].is_confirmed is True


@pytest.mark.asyncio
async def test_find_regens_ignores_non_matching_players(legend, no_match_player):
    player_repo = InMemoryPlayerRepository()
    regen_repo = InMemoryRegenRepository()

    await player_repo.save(legend)
    await player_repo.save(no_match_player)

    use_case = FindRegensUseCase(
        player_repo=player_repo,
        regen_repo=regen_repo,
        season="2024/2025",
    )

    regens = await use_case.execute()
    assert len(regens) == 0


@pytest.mark.asyncio
async def test_find_regens_does_not_match_legend_with_itself(legend):
    player_repo = InMemoryPlayerRepository()
    regen_repo = InMemoryRegenRepository()

    await player_repo.save(legend)

    use_case = FindRegensUseCase(
        player_repo=player_repo,
        regen_repo=regen_repo,
        season="2024/2025",
    )

    regens = await use_case.execute()
    assert len(regens) == 0
