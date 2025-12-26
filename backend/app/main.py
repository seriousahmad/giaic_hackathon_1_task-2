from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config.cors import add_cors_middleware
from .config.settings import settings
from .api.v1.router import create_api_router
import logging
import sys


# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        Configured FastAPI application instance
    """
    # Create FastAPI app with metadata
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="RAG backend for Physical AI Textbook",
        debug=settings.debug
    )

    # Add CORS middleware
    add_cors_middleware(app, settings.frontend_origin)

    # Create and include API router
    api_router = create_api_router()
    app.include_router(api_router, prefix="/api", tags=["api"])

    # Add a basic root endpoint
    @app.get("/")
    async def root():
        return {
            "message": "Physical AI RAG Backend",
            "version": settings.app_version,
            "status": "running"
        }

    return app


# Create the application instance
app = create_app()


# Include this so that endpoints get registered when the app is imported
# Import API endpoints after app creation to avoid circular imports
from .api.v1 import ask, ask_selection, health