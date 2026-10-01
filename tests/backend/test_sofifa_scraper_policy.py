import pytest

from BACKEND.domain.exceptions.errors import ValidationError
from BACKEND.domain.services.sofifa_scraper_policy import SofifaScraperPolicy


def test_sofifa_scraper_policy_accepts_fixed_version_and_dependencies() -> None:
    policy = SofifaScraperPolicy(
        repository="sofifa-scraper",
        version="v1.2.3",
        commit="8f3d91a",
        dependencies={"requests": "2.32.3", "parsel": "1.9.1"},
        license="MIT",
        max_pages=50,
        reproducible_procedure=(
            "git checkout 8f3d91a; pip install requests==2.32.3 parsel==1.9.1"
        ),
        credentials_required=False,
        traceability_required=True,
    )

    assert policy.repository == "sofifa-scraper"
    assert policy.version == "v1.2.3"
    assert policy.commit == "8f3d91a"
    assert policy.dependencies == {"requests": "2.32.3", "parsel": "1.9.1"}
    assert policy.license == "MIT"
    assert policy.max_pages == 50
    assert policy.credentials_required is False
    assert policy.traceability_required is True
    assert policy.reproducible_procedure == (
        "git checkout 8f3d91a; pip install requests==2.32.3 parsel==1.9.1"
    )


def test_sofifa_scraper_policy_rejects_missing_version_or_dependencies() -> None:
    with pytest.raises(ValidationError, match="versión"):
        SofifaScraperPolicy(
            repository="sofifa-scraper",
            version="",
            commit="8f3d91a",
            dependencies={"requests": "2.32.3", "parsel": "1.9.1"},
            license="MIT",
            max_pages=50,
            reproducible_procedure="git checkout 8f3d91a",
            credentials_required=False,
            traceability_required=True,
        )

    with pytest.raises(ValidationError, match="requests"):
        SofifaScraperPolicy(
            repository="sofifa-scraper",
            version="v1.2.3",
            commit="8f3d91a",
            dependencies={"parsel": "1.9.1"},
            license="MIT",
            max_pages=50,
            reproducible_procedure="git checkout 8f3d91a",
            credentials_required=False,
            traceability_required=True,
        )

    with pytest.raises(ValidationError, match="MIT"):
        SofifaScraperPolicy(
            repository="sofifa-scraper",
            version="v1.2.3",
            commit="8f3d91a",
            dependencies={"requests": "2.32.3", "parsel": "1.9.1"},
            license="Apache-2.0",
            max_pages=50,
            reproducible_procedure="git checkout 8f3d91a",
            credentials_required=False,
            traceability_required=True,
        )

    with pytest.raises(ValidationError, match="credenciales"):
        SofifaScraperPolicy(
            repository="sofifa-scraper",
            version="v1.2.3",
            commit="8f3d91a",
            dependencies={"requests": "2.32.3", "parsel": "1.9.1"},
            license="MIT",
            max_pages=50,
            reproducible_procedure="git checkout 8f3d91a",
            credentials_required=True,
            traceability_required=True,
        )
