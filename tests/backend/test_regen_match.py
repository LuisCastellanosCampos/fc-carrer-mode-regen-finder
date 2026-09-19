from datetime import date

import pytest

from BACKEND.domain.entities.player import Player
from BACKEND.domain.entities.regen_match import RegenMatch


def test_regen_match_represents_player_and_match_states() -> None:
    player = Player(
        id="p-1042",
        name="Alejandro Ruiz",
        birth_date=date(1998, 4, 12),
        nationality="Spain",
        position="ST",
        overall=87,
        age=24,
        season="2026",
    )
    match = RegenMatch(
        player=player,
        birth_date_matches=True,
        nationality_matches=True,
        position_matches=True,
        is_possible_regen=True,
        message="Posible regen: coinciden fecha de nacimiento, nacionalidad y posición.",
    )

    assert match.player is player
    assert match.birth_date_matches is True
    assert match.nationality_matches is True
    assert match.position_matches is True
    assert match.is_possible_regen is True
    assert match.message.startswith("Posible regen:")


def test_regen_match_allows_position_state_to_be_unknown() -> None:
    player = Player(
        id="p-1042",
        name="Alejandro Ruiz",
        birth_date=date(1998, 4, 12),
        nationality="Spain",
        position="ST",
        overall=87,
        age=24,
        season="2026",
    )

    match = RegenMatch(
        player=player,
        birth_date_matches=True,
        nationality_matches=True,
        position_matches=None,
        is_possible_regen=True,
        message="Posible regen: coinciden fecha de nacimiento y nacionalidad.",
    )

    assert match.position_matches is None
    assert match.is_possible_regen is True


@pytest.mark.parametrize(
    ("birth_date_matches", "nationality_matches"),
    [(False, True), (True, False), (False, False)],
)
def test_regen_match_rejects_possible_regen_without_required_matches(
    birth_date_matches: bool,
    nationality_matches: bool,
) -> None:
    player = Player(
        id="p-1042",
        name="Alejandro Ruiz",
        birth_date=date(1998, 4, 12),
        nationality="Spain",
        position="ST",
        overall=87,
        age=24,
        season="2026",
    )

    with pytest.raises(ValueError, match="fecha y nacionalidad"):
        RegenMatch(
            player=player,
            birth_date_matches=birth_date_matches,
            nationality_matches=nationality_matches,
            position_matches=False,
            is_possible_regen=True,
            message="Resultado incompatible.",
        )
