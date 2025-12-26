from fastapi import APIRouter
from typing import Dict
from ...models.response import HealthResponse
from ...services.rag_engine import rag_engine
from ...config.settings import settings
from datetime import datetime
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Service health check endpoint.
    Returns the health status of the RAG system and the active model.
    """
    try:
        # Perform health checks on all components
        health_status = await rag_engine.health_check()

        # Create dependencies status report
        dependencies = {
            "gemini_api": health_status["gemini_api"],
            "qdrant_db": health_status["qdrant_db"],
            "overall_status": health_status["overall"]
        }

        # Create response object
        response = HealthResponse(
            status="ok" if health_status["overall"] else "degraded",
            model="gemini-2.0-flash",
            timestamp=datetime.now().isoformat(),
            dependencies=dependencies
        )

        return response

    except Exception as e:
        logger.error(f"Error in /api/health endpoint: {str(e)}")

        # Return degraded status if there's an error
        response = HealthResponse(
            status="error",
            model="gemini-2.0-flash",
            timestamp=datetime.now().isoformat(),
            dependencies={
                "gemini_api": False,
                "qdrant_db": False,
                "overall_status": False,
                "error": str(e)
            }
        )

        return response


# Simple ping endpoint for basic connectivity check
@router.get("/ping")
async def ping() -> Dict[str, str]:
    """
    Simple ping endpoint for basic connectivity check.
    """
    return {"status": "ok", "message": "pong"}