"""MIRA Application Factory.

Configures FastAPI instance, middleware, exception handlers, API routing,
and mounts static assets for the MIRA character foundation.
"""

from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from config.settings import Settings, get_settings
from src.api.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifecycle events."""
    settings = get_settings()
    app.state.settings = settings
    yield


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

    # Base workspace path resolution
    base_dir = Path(__file__).resolve().parent.parent.parent

    # Mount static asset directory for character assets
    assets_dir = base_dir / "assets"
    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")

    # Mount static UI components for character viewer
    character_static_dir = base_dir / "src" / "character" / "static"
    if character_static_dir.exists():
        app.mount("/character-ui", StaticFiles(directory=str(character_static_dir)), name="character-ui")

    # Interactive character showcase routes
    viewer_file = character_static_dir / "viewer.html"

    @app.get("/character", include_in_schema=False)
    async def character_viewer():
        """Serves the interactive MIRA character viewer console."""
        if viewer_file.exists():
            return FileResponse(viewer_file)
        return {"error": "Character viewer interface not found"}

    @app.get("/", include_in_schema=False)
    async def root_redirect():
        """Redirects root or serves character viewer."""
        if viewer_file.exists():
            return FileResponse(viewer_file)
        return {"status": "ok", "app": settings.app_name, "version": settings.version}

    # Canonical root asset route for direct fallback
    root_model_file = base_dir / "MIRA_FACE_MODEL.png"

    @app.get("/MIRA_FACE_MODEL.png", include_in_schema=False)
    async def canonical_root_image():
        """Serves the root canonical MIRA_FACE_MODEL.png directly."""
        if root_model_file.exists():
            return FileResponse(root_model_file, media_type="image/png")
        return {"error": "Canonical reference not found"}

    return app
