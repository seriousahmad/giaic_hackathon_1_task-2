import cohere
from typing import List, Dict, Any, Optional
from ..config.settings import settings
import logging


class CohereClient:
    """
    Client for interacting with Cohere's API.
    """

    def __init__(self):
        self.client = cohere.AsyncClient(
            api_key=settings.cohere_api_key
        )
        self.model = "command-r-08-2024"  # Using Cohere's available model for RAG tasks
        self.logger = logging.getLogger(__name__)

    async def generate_answer(
        self,
        question: str,
        context: Optional[str] = None,
        max_tokens: int = 200
    ) -> Dict[str, Any]:
        """
        Generate an answer to a question using the provided context.

        Args:
            question: The question to answer
            context: Relevant context to base the answer on
            max_tokens: Maximum number of tokens for the response

        Returns:
            Dictionary containing the answer and metadata
        """
        try:
            # Construct the prompt to ensure source-bound accuracy
            preamble = (
                "You are an educational assistant for the Physical AI Textbook. "
                "You must answer questions based ONLY on the provided context from the textbook. "
                "Do not invent or hallucinate any information. "
                "If the context does not contain relevant information to answer the question, "
                "respond with: 'No supporting information found in the book.'\n\n"
                "Keep answers concise and under 200 tokens. "
                "Always provide clear, educational responses appropriate for students."
            )

            # Prepare the chat history for the API call
            chat_history = []

            if context:
                # Add context as a message in the chat history
                chat_history.append({
                    "role": "USER",
                    "message": f"Context: {context}"
                })
                chat_history.append({
                    "role": "CHATBOT",
                    "message": "I understand. I have the context and will use it to answer your question."
                })
                # The current question becomes the final user message
                message = question
            else:
                message = question

            # Make the API call using Cohere's chat endpoint
            response = await self.client.chat(
                model=self.model,
                message=message,
                chat_history=chat_history,
                preamble=preamble,
                max_tokens=max_tokens,
                temperature=0.3  # Lower temperature for more consistent, factual responses
            )

            answer = response.text.strip()

            # Note: Cohere's response format is different from OpenAI
            # Usage information might not be available in all Cohere responses
            return {
                "answer": answer,
                "model": self.model,
                "usage": {
                    "prompt_tokens": 0,  # Cohere doesn't always provide detailed token usage
                    "completion_tokens": 0,
                    "total_tokens": 0
                }
            }

        except Exception as e:
            self.logger.error(f"Error generating answer with Cohere: {str(e)}")
            raise

    async def health_check(self) -> bool:
        """
        Check if the Cohere API is accessible.

        Returns:
            True if API is accessible, False otherwise
        """
        try:
            # Make a simple test call to check API connectivity
            response = await self.client.chat(
                model=self.model,
                message="Hello",
                max_tokens=10,
                temperature=0.3
            )
            return response is not None
        except Exception as e:
            self.logger.error(f"Cohere API health check failed: {str(e)}")
            return False


# Create a singleton instance
cohere_client = CohereClient()