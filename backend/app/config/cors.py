from fastapi.middleware.cors import CORSMiddleware
from typing import List


def add_cors_middleware(app, frontend_origin: str = "http://localhost:3000"):
    """
    Add CORS middleware to the FastAPI application.

    Args:
        app: FastAPI application instance
        frontend_origin: Origin URL to allow CORS for
    """
    # List of allowed origins - can be extended for production
    origins = [
        frontend_origin,  # Default frontend origin
        "http://localhost:3000",  # Development frontend
        "http://localhost:8000",  # Local backend
        "http://127.0.0.1:3000",  # Alternative localhost
        "http://127.0.0.1:8000",  # Alternative localhost
        "https://your-production-domain.com",  # Production domain placeholder
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        # Expose headers that might be needed by frontend
        expose_headers=["Access-Control-Allow-Origin"]
    )