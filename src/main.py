"""MIRA Main Application Server Entrypoint.

Starts the MIRA standalone healthcare assistant service.
"""

import uvicorn
from config.settings import get_settings
from src.api.app import create_app

app = create_app()

if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(
        "src.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
