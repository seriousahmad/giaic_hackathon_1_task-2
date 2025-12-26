from typing import Optional
from pydantic import ValidationError
import re


def validate_text_length(text: str, min_length: int = 1, max_length: int = 1000) -> bool:
    """
    Validate text length against minimum and maximum constraints.

    Args:
        text: Text to validate
        min_length: Minimum allowed length
        max_length: Maximum allowed length

    Returns:
        True if valid, False otherwise
    """
    if not text:
        return False
    if len(text.strip()) < min_length:
        return False
    if len(text) > max_length:
        return False
    return True


def validate_selection_text(selection: str) -> tuple[bool, Optional[str]]:
    """
    Validate selected text according to requirements.

    Args:
        selection: Text that was selected by user

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not selection or not selection.strip():
        return False, "Selection cannot be empty"

    if len(selection.strip()) < 10:
        return False, "Selection must be at least 10 characters for meaningful context"

    if len(selection) > 5000:
        return False, "Selection is too long (maximum 5000 characters)"

    return True, None


def validate_question_text(question: str) -> tuple[bool, Optional[str]]:
    """
    Validate question text according to requirements.

    Args:
        question: Question text to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not question or not question.strip():
        return False, "Question cannot be empty"

    if len(question.strip()) < 1:
        return False, "Question must be at least 1 character long"

    if len(question) > 1000:
        return False, "Question is too long (maximum 1000 characters)"

    return True, None


def sanitize_text(text: str) -> str:
    """
    Sanitize text input by removing potentially harmful content.

    Args:
        text: Input text to sanitize

    Returns:
        Sanitized text
    """
    # Remove any potential SQL injection patterns
    sanitized = re.sub(r"(?i)(union|select|insert|delete|update|drop|create|alter|exec|execute)", "", text)

    # Remove potentially harmful characters (be careful not to over-sanitize for text content)
    return sanitized.strip()


def validate_token_length(text: str, max_tokens: int = 200) -> bool:
    """
    Validate text length against token count (approximate).
    This is a rough estimation - 1 token is roughly 4 characters.

    Args:
        text: Text to validate
        max_tokens: Maximum allowed tokens

    Returns:
        True if within token limit, False otherwise
    """
    # Rough estimation: 1 token ≈ 4 characters
    estimated_tokens = len(text) // 4
    return estimated_tokens <= max_tokens