#!/usr/bin/env python3
"""
Script to index book chapters into the Qdrant vector database.
This script reads MDX files from the docs/chapters directory, chunks the content,
creates embeddings, and stores them in the Qdrant collection.
"""
import asyncio
import os
import sys
from pathlib import Path
from typing import List, Dict, Any
import logging

# Add the backend directory to the path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from app.services.qdrant_client import qdrant_service
from app.services.embedding import embedding_service
from app.utils.text_chunking import create_chunks_from_file
from app.config.settings import settings


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def index_chapters_to_qdrant(
    chapters_dir: str = "../docs/chapters",
    chunk_size: int = 1000,
    overlap: int = 200
) -> None:
    """
    Index all MDX chapters from the specified directory into Qdrant.

    Args:
        chapters_dir: Directory containing MDX chapter files
        chunk_size: Size of text chunks
        overlap: Overlap between chunks
    """
    logger.info(f"Starting to index chapters from {chapters_dir}")

    # Verify Qdrant connection
    if not await qdrant_service.health_check():
        logger.error("Cannot connect to Qdrant database")
        return

    logger.info(f"Connected to Qdrant at {settings.qdrant_url}")

    # Get all MDX files from the chapters directory
    chapters_path = Path(chapters_dir)
    if not chapters_path.exists():
        logger.error(f"Chapters directory does not exist: {chapters_dir}")
        return

    mdx_files = list(chapters_path.glob("*.mdx"))
    if not mdx_files:
        logger.warning(f"No MDX files found in {chapters_dir}")
        return

    logger.info(f"Found {len(mdx_files)} MDX files to index")

    # Process each chapter file
    total_chunks = 0
    global_point_id = 0  # Global ID counter to ensure uniqueness across all files

    for mdx_file in mdx_files:
        logger.info(f"Processing {mdx_file.name}")

        try:
            # Create chunks from the file
            chunks = create_chunks_from_file(
                str(mdx_file),
                chunk_size=chunk_size,
                overlap=overlap
            )

            logger.info(f"Created {len(chunks)} chunks from {mdx_file.name}")

            # Prepare points for Qdrant
            points = []
            for i, chunk in enumerate(chunks):
                # Create embedding for the chunk content
                embedding = await embedding_service.create_embedding(chunk['content'])

                # Create a point for Qdrant (Qdrant requires numeric or UUID IDs)
                point = {
                    "id": global_point_id,  # Use global unique numeric IDs
                    "vector": embedding,
                    "payload": {
                        "content": chunk['content'],
                        "metadata": {
                            **chunk['metadata'],
                            "source_file": str(mdx_file),
                            "source_type": "chapter"
                        }
                    }
                }
                points.append(point)
                global_point_id += 1

            # Upload points to Qdrant
            if points:
                try:
                    # Use the correct method signature for uploading points
                    from qdrant_client.models import PointStruct
                    point_structs = []
                    for point in points:
                        point_struct = PointStruct(
                            id=point["id"],
                            vector=point["vector"],
                            payload=point["payload"]
                        )
                        point_structs.append(point_struct)

                    qdrant_service.client.upload_points(
                        collection_name=qdrant_service.collection_name,
                        points=point_structs
                    )
                    logger.info(f"Uploaded {len(points)} chunks to Qdrant for {mdx_file.name}")
                    total_chunks += len(points)
                except Exception as e:
                    logger.error(f"Error uploading chunks for {mdx_file.name}: {str(e)}")
                    continue

        except Exception as e:
            logger.error(f"Error processing file {mdx_file.name}: {str(e)}")
            continue

    logger.info(f"Indexing completed! Total chunks uploaded: {total_chunks}")


async def create_collection_if_not_exists():
    """Create the Qdrant collection if it doesn't exist."""
    try:
        from qdrant_client.http import models

        # Check if collection exists
        collections = qdrant_service.client.get_collections()
        collection_names = [col.name for col in collections.collections]

        if qdrant_service.collection_name not in collection_names:
            logger.info(f"Creating collection '{qdrant_service.collection_name}'")

            # Create collection with appropriate settings for text embeddings
            qdrant_service.client.create_collection(
                collection_name=qdrant_service.collection_name,
                vectors_config=models.VectorParams(
                    size=1024,  # Cohere embed-multilingual-v3.0 produces 1024-dimensional vectors
                    distance=models.Distance.COSINE
                )
            )
            logger.info(f"Collection '{qdrant_service.collection_name}' created successfully")
        else:
            logger.info(f"Collection '{qdrant_service.collection_name}' already exists")

    except Exception as e:
        logger.error(f"Error creating collection: {str(e)}")
        raise


async def main():
    """Main function to run the indexing process."""
    logger.info("Starting the chapter indexing process...")

    # Create collection if it doesn't exist
    await create_collection_if_not_exists()

    # Index the chapters
    await index_chapters_to_qdrant()

    logger.info("Chapter indexing process completed!")


if __name__ == "__main__":
    # Check if required environment variables are set
    if not settings.cohere_api_key or not settings.qdrant_url or not settings.qdrant_api_key:
        logger.error("Missing required environment variables. Please check your .env file.")
        logger.error(f"Cohere API Key set: {bool(settings.cohere_api_key)}")
        logger.error(f"Qdrant URL set: {bool(settings.qdrant_url)}")
        logger.error(f"Qdrant API Key set: {bool(settings.qdrant_api_key)}")
        sys.exit(1)

    # Run the indexing process
    asyncio.run(main())