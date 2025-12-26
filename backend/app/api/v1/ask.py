from fastapi import APIRouter, HTTPException
from ...services.rag_engine import rag_engine
from ...models.request import QuestionRequest
from ...models.response import AnswerResponse
from ...utils.validation import validate_question_text
from typing import Dict, Any
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest) -> AnswerResponse:
    """
    Main RAG question answering endpoint.
    Accepts user questions and returns answers with sources from textbook content.
    """
    try:
        # Validate question using utility function
        is_valid, error_msg = validate_question_text(request.question)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)

        # Generate answer using RAG engine
        result = await rag_engine.generate_answer(request.question)

        # Create response object
        response = AnswerResponse(
            answer=result["answer"],
            sources=result["sources"]
        )

        return response

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error in /api/ask endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error while processing question"
        )


# Additional endpoint for testing purposes
@router.get("/ask/test")
async def test_ask() -> Dict[str, str]:
    """
    Test endpoint for the ask functionality.
    """
    return {"message": "Ask endpoint is working"}