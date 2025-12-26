"""
Simple test script to verify the API endpoints are working correctly.
This is not a comprehensive test suite but a basic verification.
"""
import asyncio
from app.main import app
from fastapi.testclient import TestClient


def test_api_endpoints():
    """
    Test that all API endpoints are accessible.
    """
    client = TestClient(app)

    # Test root endpoint
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "Physical AI RAG Backend"

    # Test health endpoint
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "model" in data

    # Test ask endpoint (should return 422 for missing/invalid request body)
    response = client.post("/api/ask")
    assert response.status_code in [422, 400]  # Validation error expected

    # Test ask-selection endpoint (should return 422 for missing/invalid request body)
    response = client.post("/api/ask-selection")
    assert response.status_code in [422, 400]  # Validation error expected

    # Test ping endpoint
    response = client.get("/api/ping")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"

    print("All endpoint tests passed!")


if __name__ == "__main__":
    test_api_endpoints()