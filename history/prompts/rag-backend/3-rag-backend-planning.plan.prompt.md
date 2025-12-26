---
id: 3
title: RAG backend planning
stage: plan
date: 2025-12-24
surface: agent
model: claude-sonnet-4-5-20250929
feature: rag-backend
branch: 001-rag-backend
user: claude
command: /sp.plan
labels: [planning, rag, backend, ai, textbook, architecture]
links:
  spec: specs/001-rag-backend/spec.md
  plan: specs/001-rag-backend/plan.md
  adr: null
  pr: null
files:
 - specs/001-rag-backend/plan.md
 - specs/001-rag-backend/research.md
 - specs/001-rag-backend/data-model.md
 - specs/001-rag-backend/quickstart.md
 - specs/001-rag-backend/contracts/ask-api.yaml
 - specs/001-rag-backend/contracts/ask-selection-api.yaml
 - specs/001-rag-backend/contracts/health-api.yaml
tests:
 - null
---

## Prompt

# Implementation Plan: Physical AI RAG Backend

## Goal
Build a pure RAG backend using FastAPI and Gemini 2.0 Flash to power the Physical AI Textbook chatbot.

## Phase 1: Foundation & Configuration
- [ ] **Project Structure**: Set up `backend/app` directory.
- [ ] **Dependencies**: Install `fastapi`, `uvicorn`, `openai`, `qdrant-client`, `python-dotenv`.
- [ ] **Environment**: Configure `.env` with `GEMINI_API_KEY` and `QDRANT_URL`.
- [ ] **Git**: Configure `.gitignore`.

## Phase 2: RAG Engine Implementation
- [ ] **Gemini Client**: Configure `AsyncOpenAI` with `base_url="https://generativelanguage.googleapis.com/v1beta/openai"`.
- [ ] **Vector Store**: basic Qdrant client setup for searching `physical_ai_textbook` collection.
- [ ] **Logic**: Implement `embed_query` (using `text-embedding-004`) and `generate_answer` (using `gemini-2.0-flash`).

## Phase 3: API Development
- [ ] **Setup**: Initialize `FastAPI` app in `main.py`.
- [ ] **CORS**: Allow frontend origin (`localhost:3000`, deployed URL).
- [ ] **Endpoint**: `POST /api/ask` (Standard RAG).
- [ ] **Endpoint**: `POST /api/ask-selection` (Selection Context).
- [ ] **Endpoint**: `GET /api/health` (Status check).

## Phase 4: Cleanup & Deployment
- [ ] **Refactor**: Remove legacy auth/db code from previous iterations.
- [ ] **Docker**: Create `Dockerfile` for Hugging Face Spaces (Port 7860).
- [ ] **Verification**: Verify endpoints with `verification.py`.

## Response snapshot

Completed the implementation plan for the Physical AI RAG Backend. The plan includes:

1. **Technical Context**: Defined Python 3.11, FastAPI, Qdrant, and Gemini 2.0 Flash integration
2. **Constitution Check**: Verified alignment with all constitutional principles including source-bound accuracy and performance requirements
3. **Project Structure**: Detailed directory structure with modular organization (models, services, API endpoints)
4. **Research**: Resolved technology choices including Gemini API access via OpenAI SDK, Qdrant vector database, and FastAPI framework
5. **Data Model**: Defined entities (Question, Answer, TextSelection, VectorChunk, HealthStatus) with validation rules
6. **API Contracts**: Created OpenAPI specifications for all three endpoints (ask, ask-selection, health)
7. **Quickstart Guide**: Provided comprehensive setup and usage instructions

All Phase 0 and Phase 1 planning artifacts have been created successfully, with all constitutional requirements satisfied. The plan is ready for the task generation phase.

## Outcome

- ✅ Impact: Complete implementation plan with all required artifacts created
- 🧪 Tests: N/A for planning phase
- 📁 Files: Created plan.md, research.md, data-model.md, quickstart.md, and API contracts
- 🔁 Next prompts: Ready for task generation with /sp.tasks
- 🧠 Reflection: Plan aligns with constitutional requirements and provides clear implementation roadmap

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - All constitutional requirements verified
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Generate tasks for implementation