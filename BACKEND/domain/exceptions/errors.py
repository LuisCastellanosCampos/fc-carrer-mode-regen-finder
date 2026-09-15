class DomainError(Exception):
    """Base para errores controlados del dominio."""


class ValidationError(DomainError, ValueError):
    """Datos de entrada inválidos para una operación de dominio."""


class CatalogUnavailableError(DomainError, RuntimeError):
    """El catálogo no está disponible para una consulta."""
