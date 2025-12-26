import time
from typing import List, Dict, Any, Optional
from ..services.cohere_client import cohere_client
from ..services.qdrant_client import qdrant_service
from ..services.embedding import embedding_service
from ..utils.validation import validate_token_length
from ..config.settings import settings
import logging


class RAGEngine:
    """
    Core RAG (Retrieval Augmented Generation) engine that orchestrates
    the process of retrieving relevant context and generating answers.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    async def generate_answer(self, question: str) -> Dict[str, Any]:
        """
        Generate an answer to a question by retrieving relevant context and using LLM.

        Args:
            question: The question to answer

        Returns:
            Dictionary containing the answer and sources
        """
        start_time = time.time()

        try:
            # Validate the question
            if not question or len(question.strip()) == 0:
                return {
                    "answer": "Question cannot be empty",
                    "sources": []
                }

            if len(question) > settings.max_question_length:
                return {
                    "answer": f"Question is too long (maximum {settings.max_question_length} characters)",
                    "sources": []
                }

            # Create embedding for the question
            question_embedding = await embedding_service.create_embedding(question)

            # Retrieve relevant chunks from vector database
            similar_chunks = await qdrant_service.search_similar_chunks(
                query_vector=question_embedding,
                top_k=5
            )

            if not similar_chunks:
                return {
                    "answer": "No supporting information found in the book.",
                    "sources": []
                }

            # Combine the context from retrieved chunks
            context_parts = []
            sources = []
            for chunk in similar_chunks:
                context_parts.append(chunk["content"])
                # Add source reference (could be chapter, section, or chunk ID)
                source_ref = chunk["metadata"].get("source", f"Chunk {chunk['id']}")
                sources.append(source_ref)

            context = "\n\n".join(context_parts)

            # Generate answer using the LLM
            response = await cohere_client.generate_answer(
                question=question,
                context=context,
                max_tokens=settings.max_tokens
            )

            answer = response["answer"]

            # Validate answer length
            if not validate_token_length(answer, settings.max_tokens):
                self.logger.warning(f"Generated answer exceeds token limit: {len(answer)} characters")

            # Calculate total processing time
            total_time = time.time() - start_time

            # Log performance metrics if exceeding threshold
            if total_time > 1.5:  # 1.5 seconds threshold
                self.logger.warning(f"Response time exceeded threshold: {total_time:.2f}s")

            self.logger.info(f"RAG query processed in {total_time:.2f}s")

            return {
                "answer": answer,
                "sources": sources
            }

        except Exception as e:
            self.logger.error(f"Error in RAG engine generate_answer: {str(e)}")
            raise

    async def generate_answer_for_selection(
        self,
        selection: str,
        question: Optional[str] = None
    ) -> str:
        """
        Generate an answer based on selected text, with optional additional question.

        Args:
            selection: The text that was selected by the user
            question: Optional additional question about the selected text

        Returns:
            Generated answer
        """
        start_time = time.time()

        try:
            # Validate selection length
            if len(selection.strip()) < settings.min_selection_length:
                # If selection is too short, fall back to normal RAG behavior
                if question:
                    result = await self.generate_answer(question)
                    answer = result["answer"]
                else:
                    answer = "Selected text is too short for meaningful context. Please select more text or ask a specific question."
            else:
                # If no additional question is provided, ask for explanation of the selected text
                if not question:
                    question = f"Can you explain this: {selection}"
                else:
                    question = f"Regarding this text: '{selection}', {question.lower() if question[0].isupper() else question}"

                # Create embedding for the combined query
                query_text = f"{selection} {question}"
                selection_embedding = await embedding_service.create_embedding(query_text)

                # Retrieve any additional context that might be relevant
                similar_chunks = await qdrant_service.search_similar_chunks(
                    query_vector=selection_embedding,
                    top_k=3  # Fewer chunks since we already have the selected text as context
                )

                # Combine the selected text with any additional context
                context_parts = [selection]  # Start with the selected text
                for chunk in similar_chunks:
                    # Avoid duplicating the selected content if it's similar to retrieved chunks
                    if chunk["content"] != selection and len(chunk["content"]) > 10:
                        context_parts.append(chunk["content"])

                context = "\n\n".join(context_parts)

                # Generate answer using the LLM
                response = await cohere_client.generate_answer(
                    question=question,
                    context=context,
                    max_tokens=settings.max_tokens
                )

                answer = response["answer"]

            # Validate answer length
            if not validate_token_length(answer, settings.max_tokens):
                self.logger.warning(f"Generated answer exceeds token limit: {len(answer)} characters")

            # Calculate total processing time
            total_time = time.time() - start_time

            # Log performance metrics if exceeding threshold
            if total_time > 1.5:  # 1.5 seconds threshold
                self.logger.warning(f"Response time exceeded threshold: {total_time:.2f}s")

            self.logger.info(f"RAG selection query processed in {total_time:.2f}s")

            return answer

        except Exception as e:
            self.logger.error(f"Error in RAG engine generate_answer_for_selection: {str(e)}")
            raise

    async def health_check(self) -> Dict[str, Any]:
        """
        Perform health check of all RAG components.

        Returns:
            Health status of all components
        """
        cohere_ok = await cohere_client.health_check()
        qdrant_ok = await qdrant_service.health_check()

        return {
            "cohere_api": cohere_ok,
            "qdrant_db": qdrant_ok,
            "overall": cohere_ok and qdrant_ok
        }


# Create a singleton instance
rag_engine = RAGEngine()