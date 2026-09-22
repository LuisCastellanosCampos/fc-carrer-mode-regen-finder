from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from BACKEND.adapters.inbound.http.catalog import (
	create_catalog_router,
	create_regen_router,
)
from BACKEND.adapters.outbound.in_memory_catalog import InMemoryCatalog
from BACKEND.application.use_cases.find_regens import FindRegensService
from BACKEND.application.use_cases.update_catalog import UpdateCatalogService
from BACKEND.domain.exceptions.errors import (
	CatalogConflictError,
	CatalogUnavailableError,
	ValidationError,
)


def create_app(catalog: InMemoryCatalog | None = None) -> FastAPI:
	catalog_adapter = catalog or InMemoryCatalog()
	app = FastAPI()

	@app.exception_handler(RequestValidationError)
	async def request_validation_error(
		request: Request, exc: RequestValidationError
	) -> JSONResponse:
		fields = {str(error["loc"][-1]) for error in exc.errors()}
		messages = {
			"birth_date": "La fecha de nacimiento es inválida.",
			"nationality": "La nacionalidad es inválida.",
			"position": "La posición es inválida.",
		}
		detail = next(
			(messages[field] for field in messages if field in fields),
			"La petición es inválida.",
		)
		return JSONResponse(status_code=400, content={"detail": detail})

	@app.exception_handler(ValidationError)
	async def domain_validation_error(
		request: Request, exc: ValidationError
	) -> JSONResponse:
		return JSONResponse(status_code=400, content={"detail": str(exc)})

	@app.exception_handler(CatalogConflictError)
	async def catalog_conflict_error(
		request: Request, exc: CatalogConflictError
	) -> JSONResponse:
		return JSONResponse(status_code=409, content={"detail": str(exc)})

	@app.exception_handler(CatalogUnavailableError)
	async def catalog_unavailable_error(
		request: Request, exc: CatalogUnavailableError
	) -> JSONResponse:
		return JSONResponse(status_code=503, content={"detail": str(exc)})

	@app.exception_handler(Exception)
	async def unexpected_error(request: Request, exc: Exception) -> JSONResponse:
		return JSONResponse(
			status_code=500,
			content={"detail": "Error interno del servidor."},
		)

	app.include_router(create_catalog_router(UpdateCatalogService(catalog_adapter)))
	app.include_router(create_regen_router(FindRegensService(catalog_adapter)))
	return app


app = create_app()
