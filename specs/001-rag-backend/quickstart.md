# Quickstart Guide: Physical AI RAG Backend

## Prerequisites

- Python 3.11+
- Access to Google AI Studio for Gemini API key
- Qdrant Cloud account or local instance
- Git

## Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your actual values:
   GEMINI_API_KEY=your_gemini_api_key_here
   QDRANT_URL=your_qdrant_url_here
   QDRANT_API_KEY=your_qdrant_api_key_here
   ```

## Running the Application

1. **Start the development server**:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

2. **Access the API**:
   - Documentation: `http://localhost:8000/docs`
   - Health check: `http://localhost:8000/api/health`

## API Endpoints

### 1. Ask Questions (`POST /api/ask`)
Ask questions about textbook content:
```bash
curl -X POST http://localhost:8000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is forward kinematics?"}'
```

### 2. Selected Text Explanation (`POST /api/ask-selection`)
Get explanations for selected text:
```bash
curl -X POST http://localhost:8000/api/ask-selection \
  -H "Content-Type: application/json" \
  -d '{"selection": "Forward kinematics calculates the end-effector position from joint angles", "question": "Can you explain this further?"}'
```

### 3. Health Check (`GET /api/health`)
Check system status:
```bash
curl http://localhost:8000/api/health
```

## Configuration

The application uses the following environment variables:

- `GEMINI_API_KEY`: Your Google AI Studio API key
- `QDRANT_URL`: URL to your Qdrant instance
- `QDRANT_API_KEY`: API key for Qdrant (if required)
- `NEON_DB_URL`: Connection string for Neon Postgres (metadata storage)

## Docker Deployment

To run with Docker:

```bash
docker build -t rag-backend .
docker run -p 8000:8000 rag-backend
```

## Testing

Run the test suite:
```bash
pytest tests/
```

## Troubleshooting

- **API Connection Errors**: Verify your `GEMINI_API_KEY` is valid and has sufficient quota
- **Qdrant Connection Errors**: Check that `QDRANT_URL` is accessible and `QDRANT_API_KEY` is correct
- **Slow Responses**: Ensure your Qdrant instance has sufficient resources for vector search