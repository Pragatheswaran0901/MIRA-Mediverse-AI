"""MIRA Application Factory.

Configures FastAPI instance, middleware, exception handlers, and API routing.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.settings import Settings, get_settings
from src.api.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifecycle events."""
    # Startup logging and initialization
    settings = get_settings()
    app.state.settings = settings
    yield
    # Shutdown cleanup


def create_app(settings: Settings | None = None) -> FastAPI:
    """Builds and configures the MIRA FastAPI application."""
    if settings is None:
        settings = get_settings()

    app = FastAPI(
        title=f"{settings.app_name} - {settings.app_full_name}",
        description=(
            "MIRA (Medical Intelligent Response Assistant) is an interactive AI healthcare companion "
            "and AI Nurse Assistant built as an independent, standalone product."
        ),
        version=settings.version,
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # Enable CORS for external client applications
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Mount central API router
    app.include_router(api_router)

    return app
