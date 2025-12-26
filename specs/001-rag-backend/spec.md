# Feature Specification: Physical AI RAG System Backend

**Feature Branch**: `001-rag-backend`
**Created**: 2025-12-24
**Status**: Draft
**Input**: User description: "# Backend Specification: Physical AI RAG System

## 1. System Overview
The backend serves as the intelligence layer for the Physical AI Textbook. It intercepts user queries, retrieves context from vector storage, and synthesizes answers using Google's Gemini models.

## 2. Architecture

### 2.1 Tech Stack
-   **Runtime**: Python 3.11+
-   **Web Server**: FastAPI + Uvicorn
-   **LLM**: Google Gemini 2.0 Flash (via `openai` SDK)
-   **Embeddings**: Google `text-embedding-004` (768d)
-   **Vector DB**: Qdrant Cloud

### 2.2 Data Flow
1.  **Request**: Frontend sends JSON payload to `POST /api/ask`.
2.  **Embedding**: Backend embeds query using `text-embedding-004`.
3.  **Retrieval**: Qdrant searches `physical_ai_textbook` collection for top-k similar chunks.
4.  **Synthesis**: Gemini 2.0 Flash receives `(System Prompt + Context + Question)`.
5.  **Response**: JSON containing the answer is sent back.

## 3. API Reference

### 3.1 `POST /api/ask`
**Summary**: Main RAG question answering endpoint.

**Request Body**:
```json
{
  "question": "string"
}
```

**Response**:
```json
{
  "answer": "string",
  "sources": ["string"]
}
```

### 3.2 `POST /api/ask-selection`
**Summary**: Contextual explanation of selected text.

**Request Body**:
```json
{
  "selection": "string",
  "question": "string (optional)"
}
```

**Response**:
```json
{
  "answer": "string"
}
```

### 3.3 `GET /api/health`
**Summary**: Service health check.
**Response**: `{"status": "ok", "model": "gemini-2.0-flash"}`

## 4. Configuration
Required Environment Variables:
-   `GEMINI_API_KEY`: API Key for Google AI Studio.
-   `QDRANT_URL`: URL of Qdrant instance.
-   `QDRANT_API_KEY`: API Key for Qdrant.
-   `NEON_DB_URL`: sdf asdf"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ask Questions about Textbook Content (Priority: P1)

As a student reading the Physical AI textbook, I want to ask questions about specific concepts so that I can get immediate, accurate answers based on the textbook content.

**Why this priority**: This is the core functionality that delivers the primary value of the RAG system - providing intelligent answers from the textbook.

**Independent Test**: Can be fully tested by sending a question to the `/api/ask` endpoint and receiving a response with an answer and sources that are grounded in the textbook content.

**Acceptance Scenarios**:

1. **Given** a valid question about textbook content, **When** user sends POST request to `/api/ask`, **Then** system returns an answer with relevant sources from the textbook
2. **Given** a question with no relevant textbook content, **When** user sends POST request to `/api/ask`, **Then** system returns "No supporting information found in the book"

---

### User Story 2 - Get Contextual Explanations for Selected Text (Priority: P2)

As a student reading the textbook, I want to select text and get contextual explanations so that I can better understand complex concepts.

**Why this priority**: This enhances the learning experience by providing on-demand explanations for specific content the user is currently reading.

**Independent Test**: Can be fully tested by sending selected text to the `/api/ask-selection` endpoint and receiving a contextual explanation.

**Acceptance Scenarios**:

1. **Given** selected text from the textbook and an optional question, **When** user sends POST request to `/api/ask-selection`, **Then** system returns a contextual explanation based on the selected text
2. **Given** selected text less than 10 characters, **When** user sends POST request to `/api/ask-selection`, **Then** system falls back to normal RAG behavior

---

### User Story 3 - Verify System Health and Availability (Priority: P3)

As a system administrator, I want to check the health status of the RAG system so that I can ensure it's running properly and using the correct model.

**Why this priority**: This ensures operational visibility and allows for monitoring of the system's availability.

**Independent Test**: Can be fully tested by sending a GET request to `/api/health` and receiving a status response.

**Acceptance Scenarios**:

1. **Given** the RAG system is running, **When** user sends GET request to `/api/health`, **Then** system returns status "ok" and the model identifier

---

### Edge Cases

- What happens when the LLM API is temporarily unavailable?
- How does the system handle extremely long questions or selected text?
- What if the vector database is temporarily unreachable?
- How does the system handle malformed JSON requests?
- What happens when there are no relevant results from vector search?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST accept user questions via POST `/api/ask` endpoint and return answers with sources
- **FR-002**: System MUST accept selected text via POST `/api/ask-selection` endpoint and return contextual explanations
- **FR-003**: System MUST provide health check via GET `/api/health` endpoint
- **FR-004**: System MUST retrieve relevant textbook content from vector database to answer questions
- **FR-005**: System MUST synthesize answers using Google Gemini 2.0 Flash model
- **FR-006**: System MUST embed user queries using Google `text-embedding-004` model
- **FR-007**: System MUST ensure all answers are grounded in textbook content with no hallucinations
- **FR-008**: System MUST return source citations with each answer
- **FR-009**: System MUST respond to queries within 1.5 seconds for acceptable performance
- **FR-010**: System MUST handle requests with proper error handling and return appropriate HTTP status codes

### Key Entities

- **Question**: A user's query about textbook content, represented as a string
- **Answer**: A response generated by the LLM, including the answer text and source citations
- **Text Selection**: A portion of text selected by the user from the textbook, used for contextual explanations
- **Source Citation**: Reference to specific textbook content that supports the answer

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users receive answers to textbook-related questions within 1.5 seconds 95% of the time
- **SC-002**: 100% of answers are grounded in actual textbook content with no hallucinations during testing
- **SC-003**: All answers include proper source citations that can be traced back to specific textbook content
- **SC-004**: System achieves 99% uptime during operational hours
- **SC-005**: Health check endpoint returns status information within 100ms
- **SC-006**: 95% of user questions receive relevant, accurate answers based on textbook content
