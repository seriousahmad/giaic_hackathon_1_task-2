from pydantic import BaseModel, validator
from typing import Optional


class QuestionRequest(BaseModel):
    """
    Request model for asking questions about textbook content.
    """
    question: str

    @validator('question')
    def validate_question(cls, v):
        if not v or not v.strip():
            raise ValueError('Question cannot be empty or whitespace only')
        if len(v.strip()) < 1:
            raise ValueError('Question must be at least 1 character long')
        if len(v) > 1000:
            raise ValueError('Question must be no more than 1000 characters')
        return v.strip()


class SelectionRequest(BaseModel):
    """
    Request model for getting contextual explanations for selected text.
    """
    selection: str
    question: Optional[str] = None

    @validator('selection')
    def validate_selection(cls, v):
        if not v or not v.strip():
            raise ValueError('Selection cannot be empty or whitespace only')
        if len(v.strip()) < 1:
            raise ValueError('Selection must be at least 1 character long')
        if len(v) > 5000:
            raise ValueError('Selection must be no more than 5000 characters')
        return v.strip()

    @validator('question')
    def validate_question_optional(cls, v):
        if v is not None:
            v = v.strip()
            if len(v) > 1000:
                raise ValueError('Question must be no more than 1000 characters')
        return v