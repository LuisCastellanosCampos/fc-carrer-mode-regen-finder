import pytest

from BACKEND.domain.exceptions.errors import ValidationError
from BACKEND.domain.services.sofifa_catalog_scope import SofifaCatalogScope


def test_sofifa_scope_approves_unique_annual_source_and_local_search_only() -> None:
    scope = SofifaCatalogScope(
        source="Sofifa",
        season="2026",
        max_pages=50,
        import_mode="manual_or_scheduled",
    )

    assert scope.source == "Sofifa"
    assert scope.season == "2026"
    assert scope.max_pages == 50
    assert scope.import_mode == "manual_or_scheduled"
    assert scope.search_uses_local_catalog_only is True
    assert scope.simultaneous_sources_allowed is False
    assert scope.error_handling == "fail_closed"


def test_sofifa_scope_rejects_multiple_sources_or_real_time_lookup() -> None:
    with pytest.raises(ValidationError, match="fuente única"):
        SofifaCatalogScope(
            source="Sofifa y Transfermarkt",
            season="2026",
            max_pages=50,
            import_mode="manual_or_scheduled",
        )

    with pytest.raises(ValidationError, match="búsqueda"):
        SofifaCatalogScope(
            source="Sofifa",
            season="2026",
            max_pages=50,
            import_mode="manual_or_scheduled",
            search_uses_local_catalog_only=False,
        )

    with pytest.raises(ValidationError, match="simultáneas"):
        SofifaCatalogScope(
            source="Sofifa",
            season="2026",
            max_pages=50,
            import_mode="manual_or_scheduled",
            simultaneous_sources_allowed=True,
        )
