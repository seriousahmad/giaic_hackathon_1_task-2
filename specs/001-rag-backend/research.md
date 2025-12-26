# Research: Physical AI RAG Backend

## Decision: Gemini API Access via OpenAI SDK
**Rationale**: Using Google's Gemini models through the OpenAI SDK provides a familiar interface and allows for potential multi-provider flexibility. The configuration uses `base_url="https://generativelanguage.googleapis.com/v1beta/openai"` with the GEMINI_API_KEY.

**Alternatives considered**:
- Direct Google AI SDK: More native but less flexible for potential future multi-provider support
- OpenAI SDK with OpenAI models: Would not meet requirement to use Gemini 2.0 Flash
- Custom HTTP client: More complex implementation with less error handling

## Decision: Qdrant Vector Database
**Rationale**: Qdrant is a high-performance vector database with good Python client support. It's designed for similarity search which is essential for RAG systems. Cloud deployment option provides scalability.

**Alternatives considered**:
- Pinecone: Commercial option but less control over data
- Weaviate: Good alternative but Qdrant has better performance benchmarks for this use case
- FAISS: Good for local use but lacks built-in API layer

## Decision: FastAPI Framework
**Rationale**: FastAPI provides automatic API documentation (OpenAPI/Swagger), built-in validation, async support, and excellent performance for API services. It's well-suited for ML/AI backend services.

**Alternatives considered**:
- Flask: More familiar but lacks automatic documentation and async support
- Django: Overkill for simple API service, more suited for full web applications
- Express.js: Would require switching to Node.js ecosystem

## Decision: Text Embedding Model
**Rationale**: Google's `text-embedding-004` model provides good quality embeddings with 768 dimensions, which is efficient for similarity search. It integrates well with the Gemini model ecosystem.

**Alternatives considered**:
- OpenAI embeddings: Would require additional API key and wouldn't align with Gemini usage
- Sentence transformers: Self-hosted option but requires additional infrastructure
- Other Google embeddings: text-embedding-004 is the latest and most efficient

## Decision: Docker Containerization
**Rationale**: Docker provides consistent deployment across environments and is required for Hugging Face Spaces deployment as specified in the plan. Port 7860 is standard for Gradio apps but will be configured for FastAPI.

**Alternatives considered**:
- Direct deployment: Less consistent and harder to manage dependencies
- Other containerization: Docker has the best ecosystem support