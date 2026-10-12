"""MIRA Central API Router."""

from fastapi import APIRouter
from src.api.routes.character import router as character_router
from src.api.routes.health import router as health_router
from src.api.routes.info import router as info_router
from src.api.routes.verify import router as verify_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(info_router)
api_router.include_router(verify_router)
api_router.include_router(character_router)
