from dataclasses import dataclass

from BACKEND.domain.exceptions.errors import ValidationError


@dataclass(frozen=True, slots=True)
class SofifaCatalogScope:
    """Regla aprobada del alcance del catálogo Sofifa para la fase 002."""

    source: str = "Sofifa"
    season: str = "2026"
    max_pages: int = 50
    import_mode: str = "manual_or_scheduled"
    search_uses_local_catalog_only: bool = True
    simultaneous_sources_allowed: bool = False
    error_handling: str = "fail_closed"

    def __post_init__(self) -> None:
        self._validate_source()
        self._validate_season()
        self._validate_page_limit()
        self._validate_import_mode()
        self._validate_search_scope()
        self._validate_sources_policy()
        self._validate_error_handling()

    def _validate_source(self) -> None:
        if not isinstance(self.source, str) or not self.source.strip():
            raise ValidationError("La fuente del catálogo no puede estar vacía")
        if self.source != "Sofifa":
            raise ValidationError(
                "La fuente del catálogo debe ser Sofifa y una fuente única."
            )

    def _validate_season(self) -> None:
        if not isinstance(self.season, str) or not self.season.strip():
            raise ValidationError("La temporada soportada no puede estar vacía")

    def _validate_page_limit(self) -> None:
        if isinstance(self.max_pages, bool) or not isinstance(self.max_pages, int):
            raise ValidationError("El límite de extracción debe ser un entero positivo")
        if self.max_pages <= 0:
            raise ValidationError("El límite de extracción debe ser un entero positivo")

    def _validate_import_mode(self) -> None:
        valid_modes = {"manual", "scheduled", "manual_or_scheduled"}
        if self.import_mode not in valid_modes:
            raise ValidationError(
                "El modo de importación debe ser manual, programado o manual/programado"
            )

    def _validate_search_scope(self) -> None:
        if not self.search_uses_local_catalog_only:
            raise ValidationError(
                "La búsqueda debe consultar el catálogo local; no se permite la consulta directa a Sofifa."
            )

    def _validate_sources_policy(self) -> None:
        if self.simultaneous_sources_allowed:
            raise ValidationError(
                "No se permiten fuentes simultáneas en la fase Sofifa."
            )

    def _validate_error_handling(self) -> None:
        if self.error_handling != "fail_closed":
            raise ValidationError(
                "La política de errores debe cerrar la operación ante fallos controlados."
            )
