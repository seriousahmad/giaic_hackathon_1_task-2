# Physical AI RAG Backend

This is the backend service for the Physical AI Textbook RAG system, providing intelligent question answering based on textbook content.

## Setup

### Prerequisites

- Python 3.11+
- pip package manager

### Installation

1. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment**:
   ```bash
   # On Linux/Mac:
   source venv/bin/activate

   # On Windows:
   venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your actual values
   ```

## Environment Variables

- `GEMINI_API_KEY`: Your Google AI Studio API key
- `QDRANT_URL`: URL to your Qdrant instance
- `QDRANT_API_KEY`: API key for Qdrant (if required)
- `NEON_DB_URL`: Connection string for Neon Postgres (metadata storage)

## Running the Application

```bash
uvicorn app.main:app --reload --port 8000
```

## Docker Deployment

To build and run with Docker:

```bash
# Build the Docker image
docker build -t rag-backend .

# Run the container
docker run -p 7860:7860 --env-file .env rag-backend
```

For Hugging Face Spaces deployment, the application runs on port 7860 as configured in the Dockerfile.

## API Documentation

Once running, API documentation is available at `http://localhost:8000/docs`