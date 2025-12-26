#!/usr/bin/env python3
"""
Test script to verify the RAG backend is working properly.
"""
import asyncio
import sys
import os
from pathlib import Path

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.services.qdrant_client import qdrant_service
from app.services.rag_engine import rag_engine
from app.config.settings import settings


async def test_backend():
    print("Testing RAG backend components...")

    # Test 1: Check Qdrant connection and collection
    print("\n1. Testing Qdrant connection...")
    try:
        is_connected = await qdrant_service.health_check()
        print(f"   Qdrant connection: {'✓' if is_connected else '✗'}")

        if is_connected:
            # Check if collection exists and count points
            try:
                collection_info = qdrant_service.client.get_collection(qdrant_service.collection_name)
                point_count = collection_info.points_count
                print(f"   Collection '{qdrant_service.collection_name}' exists with {point_count} points")

                # Try to get a sample of points
                if point_count > 0:
                    sample_points = qdrant_service.client.scroll(
                        collection_name=qdrant_service.collection_name,
                        limit=1
                    )
                    if sample_points[0]:
                        print(f"   Sample point ID: {sample_points[0][0].id}")
                        print(f"   Sample point content preview: {sample_points[0][0].payload['content'][:100]}...")
            except Exception as e:
                print(f"   Error getting collection info: {e}")
    except Exception as e:
        print(f"   Qdrant connection failed: {e}")

    # Test 2: Check if embeddings service is accessible
    print("\n2. Testing embedding service...")
    try:
        from app.services.embedding import embedding_service
        sample_embedding = await embedding_service.create_embedding("test")
        print(f"   Embedding service: ✓ (vector size: {len(sample_embedding)})")
    except Exception as e:
        print(f"   Embedding service failed: {e}")

    # Test 3: Check RAG engine health
    print("\n3. Testing RAG engine health...")
    try:
        health_status = await rag_engine.health_check()
        print(f"   RAG health check: {health_status}")
    except Exception as e:
        print(f"   RAG health check failed: {e}")

    # Test 4: Try a sample query
    print("\n4. Testing sample query...")
    try:
        result = await rag_engine.generate_answer("What is this book about?")
        print(f"   Sample query result: {result}")
    except Exception as e:
        print(f"   Sample query failed: {e}")


if __name__ == "__main__":
    asyncio.run(test_backend())