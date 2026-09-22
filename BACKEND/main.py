from fastapi import FastAPI

from BACKEND.adapters.inbound.http.catalog import (
	create_catalog_router,
	create_regen_router,
)
from BACKEND.adapters.outbound.in_memory_catalog import InMemoryCatalog
from BACKEND.application.use_cases.find_regens import FindRegensService
from BACKEND.application.use_cases.update_catalog import UpdateCatalogService


def create_app(catalog: InMemoryCatalog | None = None) -> FastAPI:
	catalog_adapter = catalog or InMemoryCatalog()
	app = FastAPI()
	app.include_router(create_catalog_router(UpdateCatalogService(catalog_adapter)))
	app.include_router(create_regen_router(FindRegensService(catalog_adapter)))
	return app


app = create_app()
