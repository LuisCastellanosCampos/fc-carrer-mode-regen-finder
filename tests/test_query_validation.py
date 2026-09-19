from datetime import date, datetime

import pytest

from BACKEND.application.ports.use_cases import FindRegensQuery
from BACKEND.domain.exceptions.errors import ValidationError


def test_query_normalizes_nationality_and_optional_position() -> None:
    query = FindRegensQuery(
        birth_date=date(1998, 4, 12),
        nationality="  EsPaÑa  ",
        position="  St  ",
    )

    assert query.nationality == "españa"
    assert query.position == "st"


def test_query_allows_missing_position() -> None:
    query = FindRegensQuery(date(1998, 4, 12), "Spain")

    assert query.position is None


@pytest.mark.parametrize(
    "birth_date",
    ["1998-04-12", datetime(1998, 4, 12)],
)
def test_query_rejects_non_exact_dates(birth_date: object) -> None:
    with pytest.raises(ValidationError, match="fecha de nacimiento"):
        FindRegensQuery(birth_date, "Spain")  # type: ignore[arg-type]


@pytest.mark.parametrize("field", ["nationality", "position"])
@pytest.mark.parametrize("value", ["", "   "])
def test_query_rejects_empty_text(field: str, value: str) -> None:
    kwargs = {
        "birth_date": date(1998, 4, 12),
        "nationality": "Spain",
        field: value,
    }

    with pytest.raises(ValidationError, match="no puede estar vacío"):
        FindRegensQuery(**kwargs)  # type: ignore[arg-type]