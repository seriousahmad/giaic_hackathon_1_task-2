---
id: 2
title: RAG backend specification
stage: spec
date: 2025-12-24
surface: agent
model: claude-sonnet-4-5-20250929
feature: rag-backend
branch: 001-rag-backend
user: claude
command: /sp.specify
labels: [specification, rag, backend, ai, textbook]
links:
  spec: specs/001-rag-backend/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-rag-backend/spec.md
 - specs/001-rag-backend/checklists/requirements.md
tests:
 - null
---

## Prompt

# Backend Specification: Physical AI RAG System

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
-   `NEON_DB_URL`: sdf asdf

## Response snapshot

Created a comprehensive specification for the Physical AI RAG System backend. The specification includes:

1. Three prioritized user stories:
   - P1: Ask Questions about Textbook Content
   - P2: Get Contextual Explanations for Selected Text
   - P3: Verify System Health and Availability

2. Ten functional requirements covering:
   - API endpoints for question answering and health checks
   - RAG functionality with vector database retrieval
   - LLM integration with Google Gemini
   - Query embedding and source citation
   - Performance and error handling

3. Six success criteria with measurable outcomes including:
   - Response time under 1.5 seconds
   - 100% answer grounding with no hallucinations
   - Proper source citations
   - 99% uptime

4. Five identified edge cases covering API availability, input length, database connectivity, and malformed requests.

The specification is ready for the planning phase and includes a quality checklist confirming all requirements are met.

## Outcome

- ✅ Impact: Complete RAG backend specification created with user stories, requirements, and success criteria
- 🧪 Tests: N/A for specification phase
- 📁 Files: Created spec.md and requirements checklist
- 🔁 Next prompts: Ready for planning phase with /sp.plan
- 🧠 Reflection: Specification properly captures RAG system requirements while maintaining focus on textbook content

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - Specification complete and validated
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin planning phase for RAG backend implementation