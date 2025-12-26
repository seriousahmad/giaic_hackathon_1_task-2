import cohere
from typing import List
from ..config.settings import settings
import logging


class EmbeddingService:
    """
    Service for generating embeddings using Cohere's embedding model.
    """

    def __init__(self):
        self.client = cohere.Client(
            api_key=settings.cohere_api_key
        )
        self.model = "embed-multilingual-v3.0"  # Cohere's recommended embedding model
        self.logger = logging.getLogger(__name__)

    async def create_embedding(self, text: str) -> List[float]:
        """
        Create an embedding for the given text using Cohere's embedding model.

        Args:
            text: Text to create embedding for

        Returns:
            List of floats representing the embedding vector
        """
        try:
            # Prepare the text for embedding (truncate if too long)
            # Cohere's embedding models have input limits, so we'll truncate if necessary
            max_length = 5120  # Typical limit for Cohere embeddings
            if len(text) > max_length:
                text = text[:max_length]
                self.logger.warning(f"Text truncated for embedding: original length {len(text)}")

            # Create the embedding using Cohere's embed method
            response = self.client.embed(
                texts=[text],
                model=self.model,
                input_type="search_document"  # Using search_document for RAG context
            )

            # Extract and return the embedding vector
            embedding = response.embeddings[0]
            return embedding

        except Exception as e:
            self.logger.error(f"Error creating embedding: {str(e)}")
            raise

    async def create_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Create embeddings for a batch of texts.

        Args:
            texts: List of texts to create embeddings for

        Returns:
            List of embedding vectors
        """
        try:
            # Process the texts in batches if needed (Cohere has limits)
            max_batch_size = 96  # Cohere's max batch size
            all_embeddings = []

            for i in range(0, len(texts), max_batch_size):
                batch = texts[i:i + max_batch_size]

                # Prepare texts in the batch (truncate if needed)
                processed_batch = []
                for text in batch:
                    max_length = 5120
                    if len(text) > max_length:
                        text = text[:max_length]
                        self.logger.warning(f"Text truncated for embedding: original length {len(text)}")
                    processed_batch.append(text)

                # Create embeddings for the batch
                response = self.client.embed(
                    texts=processed_batch,
                    model=self.model,
                    input_type="search_document"  # Using search_document for RAG context
                )

                # Add embeddings to the result
                batch_embeddings = response.embeddings
                all_embeddings.extend(batch_embeddings)

            return all_embeddings
        except Exception as e:
            self.logger.error(f"Error creating batch embeddings: {str(e)}")
            raise

    async def similarity_search(self, query: str, candidate_embeddings: List[List[float]]) -> List[float]:
        """
        Perform a simple similarity search by calculating cosine similarity.

        Args:
            query: Query text
            candidate_embeddings: List of candidate embeddings to compare against

        Returns:
            List of similarity scores
        """
        try:
            # Create embedding for the query text
            query_embedding = await self.create_embedding(query)

            # Calculate cosine similarity
            import numpy as np
            query_array = np.array(query_embedding)

            similarities = []
            for candidate in candidate_embeddings:
                candidate_array = np.array(candidate)
                # Cosine similarity calculation
                dot_product = np.dot(query_array, candidate_array)
                norm_query = np.linalg.norm(query_array)
                norm_candidate = np.linalg.norm(candidate_array)
                similarity = dot_product / (norm_query * norm_candidate)
                similarities.append(float(similarity))

            return similarities

        except Exception as e:
            self.logger.error(f"Error in similarity search: {str(e)}")
            raise


# Create a singleton instance
embedding_service = EmbeddingService()