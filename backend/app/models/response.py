from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class AnswerResponse(BaseModel):
    """
    Response model for question answering.
    """
    answer: str
    sources: List[str]


class HealthResponse(BaseModel):
    """
    Response model for health check endpoint.
    """
    status: str
    model: str
    timestamp: str
    dependencies: Optional[Dict[str, Any]] = None


class SelectionResponse(BaseModel):
    """
    Response model for selected text explanations.
    """
    answer: str