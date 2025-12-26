from fastapi import APIRouter
from . import ask, ask_selection, health


def create_api_router() -> APIRouter:
    """
    Create and configure the main API router.

    Returns:
        Configured APIRouter instance
    """
    router = APIRouter()

    # Include all API endpoints
    router.include_router(ask.router, tags=["ask"])
    router.include_router(ask_selection.router, tags=["ask-selection"])
    router.include_router(health.router, tags=["health"])

    return router