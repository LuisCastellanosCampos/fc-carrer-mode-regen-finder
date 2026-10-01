from dataclasses import dataclass

from BACKEND.domain.exceptions.errors import ValidationError


@dataclass(frozen=True, slots=True)
class SofifaScraperPolicy:
    """Política aprobada para la versión y dependencias del scraper Sofifa."""

    repository: str
    version: str
    commit: str
    dependencies: dict[str, str]
    license: str
    max_pages: int
    reproducible_procedure: str
    credentials_required: bool = False
    traceability_required: bool = True

    def __post_init__(self) -> None:
        self._validate_repository()
        self._validate_version()
        self._validate_commit()
        self._validate_dependencies()
        self._validate_license()
        self._validate_max_pages()
        self._validate_procedure()
        self._validate_credentials()
        self._validate_traceability()

    def _validate_repository(self) -> None:
        if not isinstance(self.repository, str) or not self.repository.strip():
            raise ValidationError("El repositorio del scraper no puede estar vacío")

    def _validate_version(self) -> None:
        if not isinstance(self.version, str) or not self.version.strip():
            raise ValidationError("La versión del scraper no puede estar vacía")

    def _validate_commit(self) -> None:
        if not isinstance(self.commit, str) or not self.commit.strip():
            raise ValidationError("El commit del scraper no puede estar vacío")

    def _validate_dependencies(self) -> None:
        if not isinstance(self.dependencies, dict) or not self.dependencies:
            raise ValidationError("Las dependencias del scraper deben incluir requests y parsel")
        if "requests" not in self.dependencies:
            raise ValidationError("La dependencia requests es obligatoria")
        if "parsel" not in self.dependencies:
            raise ValidationError("La dependencia parsel es obligatoria")
        for dependency, version in self.dependencies.items():
            if not isinstance(dependency, str) or not dependency.strip():
                raise ValidationError("Cada dependencia debe tener nombre válido")
            if not isinstance(version, str) or not version.strip():
                raise ValidationError(f"La versión de {dependency} no puede estar vacía")

    def _validate_license(self) -> None:
        if not isinstance(self.license, str) or not self.license.strip():
            raise ValidationError("La licencia del scraper no puede estar vacía")
        if self.license != "MIT":
            raise ValidationError("La licencia del scraper debe ser MIT")

    def _validate_max_pages(self) -> None:
        if isinstance(self.max_pages, bool) or not isinstance(self.max_pages, int):
            raise ValidationError("El límite de páginas debe ser un entero positivo")
        if self.max_pages <= 0:
            raise ValidationError("El límite de páginas debe ser un entero positivo")

    def _validate_procedure(self) -> None:
        if not isinstance(self.reproducible_procedure, str) or not self.reproducible_procedure.strip():
            raise ValidationError("El procedimiento reproducible del scraper no puede estar vacío")

    def _validate_credentials(self) -> None:
        if self.credentials_required:
            raise ValidationError(
                "No se admiten credenciales ni secretos para ejecutar el scraper de Sofifa."
            )

    def _validate_traceability(self) -> None:
        if not self.traceability_required:
            raise ValidationError(
                "Cada cambio del scraper debe ser trazable por versión o commit."
            )
