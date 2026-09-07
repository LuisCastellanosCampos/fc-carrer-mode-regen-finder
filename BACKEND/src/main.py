"""
FastAPI Application Factory
Creates and configures the main FastAPI app with all routers.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.infrastructure.http.routers.player_router import router as player_router
from src.infrastructure.http.routers.regen_router import router as regen_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="FC Career Mode Regen Finder",
        description=(
            "API to detect regen players in EA FC Career Mode "
            "by crossing birth date and nationality data."
        ),
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # CORS – adjust origins for production
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register routers
    app.include_router(player_router, prefix="/api/v1")
    app.include_router(regen_router, prefix="/api/v1")

    @app.get("/health", tags=["health"])
    async def health_check():
        """Basic liveness probe."""
        return {"status": "ok"}

    return app


app = create_app()
