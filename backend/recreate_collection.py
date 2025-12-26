#!/usr/bin/env python3
"""
Script to delete and recreate the Qdrant collection with the correct vector dimensions for Cohere embeddings.
"""
import sys
import os
from pathlib import Path

# Add the backend directory to the path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from app.config.settings import settings
from qdrant_client import QdrantClient
from qdrant_client.http import models
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def recreate_collection():
    """Delete and recreate the Qdrant collection with correct dimensions."""
    try:
        # Initialize Qdrant client
        if settings.qdrant_api_key:
            client = QdrantClient(
                url=settings.qdrant_url,
                api_key=settings.qdrant_api_key,
                prefer_grpc=False
            )
        else:
            client = QdrantClient(url=settings.qdrant_url)

        collection_name = "physical_ai_textbook"

        # Check if collection exists
        collections = client.get_collections()
        collection_names = [col.name for col in collections.collections]

        if collection_name in collection_names:
            logger.info(f"Deleting existing collection '{collection_name}'...")
            client.delete_collection(collection_name)
            logger.info(f"Collection '{collection_name}' deleted successfully")
        else:
            logger.info(f"Collection '{collection_name}' does not exist, will create new one")

        # Create collection with correct dimensions for Cohere embeddings (1024)
        logger.info(f"Creating collection '{collection_name}' with 1024 dimensions...")
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=1024,  # Cohere embed-multilingual-v3.0 produces 1024-dimensional vectors
                distance=models.Distance.COSINE
            )
        )
        logger.info(f"Collection '{collection_name}' created successfully with 1024 dimensions")

        # Verify the collection was created correctly
        collection_info = client.get_collection(collection_name)
        logger.info(f"Collection info: {collection_info}")
        logger.info(f"Vector size: {collection_info.config.params.vectors.size}")

    except Exception as e:
        logger.error(f"Error recreating collection: {str(e)}")
        raise


if __name__ == "__main__":
    # Check if required environment variables are set
    if not settings.cohere_api_key or not settings.qdrant_url or not settings.qdrant_api_key:
        logger.error("Missing required environment variables. Please check your .env file.")
        logger.error(f"Cohere API Key set: {bool(settings.cohere_api_key)}")
        logger.error(f"Qdrant URL set: {bool(settings.qdrant_url)}")
        logger.error(f"Qdrant API Key set: {bool(settings.qdrant_api_key)}")
        sys.exit(1)

    # Recreate the collection
    recreate_collection()
    logger.info("Collection recreation completed successfully!")