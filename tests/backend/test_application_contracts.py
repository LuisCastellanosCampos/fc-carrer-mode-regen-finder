from datetime import date
from typing import Protocol, get_type_hints

import pytest

from BACKEND.domain.entities.player import Player
from BACKEND.domain.entities.regen_match import RegenMatch
from BACKEND.domain.exceptions.errors import CatalogUnavailableError, ValidationError


def test_catalog_port_contract_reads_and_replaces_players() -> None:
    from BACKEND.application.ports.catalog import CatalogPort

    assert issubclass(CatalogPort, Protocol)
    hints = get_type_hints(CatalogPort.read_players)
    assert hints["return"] == tuple[Player, ...]
    assert "players" in get_type_hints(CatalogPort.replace_players)


def test_application_use_case_ports_cover_update_and_query() -> None:
    from BACKEND.application.ports.use_cases import (
        CatalogUpdateResult,
        FindRegensQuery,
        FindRegensUseCase,
        UpdateCatalogCommand,
        UpdateCatalogUseCase,
    )

    assert issubclass(UpdateCatalogUseCase, Protocol)
    assert issubclass(FindRegensUseCase, Protocol)
    assert UpdateCatalogCommand.__annotations__.keys() == {"season", "players"}
    assert FindRegensQuery.__annotations__.keys() == {
        "birth_date",
        "nationality",
        "position",
    }
    assert CatalogUpdateResult.__annotations__.keys() == {
        "season",
        "inserted",
        "updated",
    }
    assert get_type_hints(FindRegensUseCase.execute)["return"] == tuple[RegenMatch, ...]


def test_domain_errors_communicate_spanish_messages() -> None:
    assert issubclass(ValidationError, ValueError)
    assert issubclass(CatalogUnavailableError, RuntimeError)
    assert "inválido" in str(ValidationError("El campo overall es inválido"))
    assert "catálogo" in str(CatalogUnavailableError("El catálogo no está disponible"))


def test_ports_do_not_depend_on_frameworks_or_persistence() -> None:
    import BACKEND.application.ports.catalog as catalog_module
    import BACKEND.application.ports.use_cases as use_cases_module

    for module in (catalog_module, use_cases_module):
        names = set(vars(module))
        assert "fastapi" not in names
        assert "pydantic" not in names
        assert "sqlalchemy" not in names
