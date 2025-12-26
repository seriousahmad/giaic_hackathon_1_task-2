"""
Simple test to verify the basic API functionality works without external dependencies.
"""
from app.main import app
from fastapi.testclient import TestClient


def test_basic_endpoints():
    """
    Test that basic API endpoints are accessible.
    """
    client = TestClient(app)

    # Test root endpoint
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "Physical AI RAG Backend"
    print("✓ Root endpoint works")

    # Test ping endpoint (part of health API)
    response = client.get("/api/ping")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    print("✓ Ping endpoint works")

    # Test that endpoints exist (will return 422 for missing body, which is expected)
    response = client.post("/api/ask", json={})
    assert response.status_code == 422  # Validation error expected
    print("✓ Ask endpoint exists (validation error as expected)")

    response = client.post("/api/ask-selection", json={})
    assert response.status_code == 422  # Validation error expected
    print("✓ Ask-selection endpoint exists (validation error as expected)")

    print("\nAll basic endpoint tests passed!")
    print("Note: External service dependencies (Gemini API, Qdrant) will be tested when properly configured.")


if __name__ == "__main__":
    test_basic_endpoints()