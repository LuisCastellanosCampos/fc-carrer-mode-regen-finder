from fastapi import FastAPI

from BACKEND.adapters.inbound.http.catalog import create_catalog_router
from BACKEND.adapters.outbound.in_memory_catalog import InMemoryCatalog
from BACKEND.application.use_cases.update_catalog import UpdateCatalogService


def create_app(catalog: InMemoryCatalog | None = None) -> FastAPI:
	catalog_adapter = catalog or InMemoryCatalog()
	app = FastAPI()
	app.include_router(create_catalog_router(UpdateCatalogService(catalog_adapter)))
	return app


app = create_app()
