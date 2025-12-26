from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Any, Optional
from ..config.settings import settings
import logging


class QdrantService:
    """
    Service for interacting with Qdrant vector database.
    """

    def __init__(self):
        # Initialize Qdrant client with configuration from settings
        if settings.qdrant_api_key:
            self.client = QdrantClient(
                url=settings.qdrant_url,
                api_key=settings.qdrant_api_key,
                prefer_grpc=False  # Using HTTP for better compatibility
            )
        else:
            self.client = QdrantClient(url=settings.qdrant_url)

        self.collection_name = "physical_ai_textbook"
        self.logger = logging.getLogger(__name__)

        # Verify connection and collection existence
        self._verify_collection()

    def _verify_collection(self):
        """
        Verify that the required collection exists in Qdrant.
        """
        try:
            collections = self.client.get_collections()
            collection_names = [col.name for col in collections.collections]

            if self.collection_name not in collection_names:
                self.logger.warning(
                    f"Collection '{self.collection_name}' does not exist. "
                    f"You may need to upload textbook content to this collection."
                )
            else:
                self.logger.info(f"Collection '{self.collection_name}' exists.")
        except Exception as e:
            self.logger.error(f"Error checking collections: {str(e)}")

    async def search_similar_chunks(
        self,
        query_vector: List[float],
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search for similar chunks in the vector database.

        Args:
            query_vector: Vector representation of the query
            top_k: Number of top similar chunks to return

        Returns:
            List of similar chunks with their content and metadata
        """
        try:
            # Perform the search in Qdrant
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=top_k,
                with_payload=True,
                with_vectors=False
            )

            # Format results
            results = []
            for hit in search_results:
                chunk_data = {
                    "id": str(hit.id),
                    "content": hit.payload.get("content", ""),
                    "metadata": hit.payload.get("metadata", {}),
                    "score": hit.score
                }
                results.append(chunk_data)

            return results

        except Exception as e:
            self.logger.error(f"Error searching similar chunks: {str(e)}")
            raise

    async def get_chunk_by_id(self, chunk_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific chunk by its ID.

        Args:
            chunk_id: ID of the chunk to retrieve

        Returns:
            Chunk data if found, None otherwise
        """
        try:
            points = self.client.retrieve(
                collection_name=self.collection_name,
                ids=[chunk_id],
                with_payload=True,
                with_vectors=False
            )

            if points and len(points) > 0:
                point = points[0]
                return {
                    "id": str(point.id),
                    "content": point.payload.get("content", ""),
                    "metadata": point.payload.get("metadata", {})
                }

            return None

        except Exception as e:
            self.logger.error(f"Error retrieving chunk by ID: {str(e)}")
            return None

    async def health_check(self) -> bool:
        """
        Check if the Qdrant database is accessible.

        Returns:
            True if accessible, False otherwise
        """
        try:
            # Try to get collection info as a basic health check
            collection_info = self.client.get_collection(self.collection_name)
            return collection_info is not None
        except Exception:
            try:
                # If specific collection check fails, try general info
                self.client.get_collections()
                return True
            except Exception as e:
                self.logger.error(f"Qdrant health check failed: {str(e)}")
                return False


# Create a singleton instance
qdrant_service = QdrantService()