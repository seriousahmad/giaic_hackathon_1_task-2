from fastapi import APIRouter, HTTPException
from ...services.rag_engine import rag_engine
from ...models.request import SelectionRequest
from ...models.response import SelectionResponse
from ...utils.validation import validate_selection_text
from typing import Dict
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/ask-selection", response_model=SelectionResponse)
async def ask_selection(request: SelectionRequest) -> SelectionResponse:
    """
    Contextual explanation of selected text endpoint.
    Accepts selected text and optional question, returns contextual explanation.
    """
    try:
        # Validate selection text using utility function
        is_valid, error_msg = validate_selection_text(request.selection)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)

        # Check if selection is less than 10 characters to trigger fallback
        if len(request.selection.strip()) < 10:
            if request.question:
                # Fall back to normal RAG behavior with the question
                result = await rag_engine.generate_answer(request.question)
                answer = result["answer"]
            else:
                answer = "Selected text is too short for meaningful context. Please select more text or ask a specific question."
        else:
            # Generate answer based on selection and optional question
            answer = await rag_engine.generate_answer_for_selection(
                selection=request.selection,
                question=request.question
            )

        # Create response object
        response = SelectionResponse(
            answer=answer
        )

        return response

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error in /api/ask-selection endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error while processing selection"
        )


# Additional endpoint for testing purposes
@router.get("/ask-selection/test")
async def test_ask_selection() -> Dict[str, str]:
    """
    Test endpoint for the ask-selection functionality.
    """
    return {"message": "Ask-selection endpoint is working"}