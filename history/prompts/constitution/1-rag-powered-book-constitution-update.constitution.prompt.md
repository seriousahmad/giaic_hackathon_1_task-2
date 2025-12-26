---
id: 1
title: RAG-powered book constitution update
stage: constitution
date: 2025-12-24
surface: agent
model: claude-sonnet-4-5-20250929
feature: rag-backend
branch: master
user: claude
command: /sp.constitution
labels: [constitution, rag, backend, book-chatbot]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - null
---

## Prompt

# Interactive RAG-Powered Book (OpenAI SDK Agents (Gemini API) + SpecifyKit + Claude CLI) Constitution

## Core Principles

### I. Source-bound accuracy
Answers must be grounded strictly in book text or user-selected text.

### II. Transparency of reasoning
RAG citations must be clear and traceable.

### III. Reliability
No hallucinations; no invented information.

### IV. User-centric clarity
Answers must be clear for general readers, not technical experts.

### V. Safety-first
No harmful, political, or biased interpretations beyond the text.

### VI. Deterministic behavior
Same input → consistent answer.

## Key Standards

### Retrieval Discipline
- If user highlights text: ONLY answer from highlighted text.
- If user asks general question: answer from full book corpus embedded in Qdrant.
- If no relevant text retrieved: say "No supporting information found in the book."

### RAG Response Structure
- Short summary answer (max 6 lines)
- Supporting evidence (quoted from book)
- Citation ID (Qdrant vector reference key)

### Allowed Knowledge
- Only content present in the book.
- No external facts, no guessing, no assumptions.

### Data Governance
- All chunks must map to Neon Postgres metadata rows.
- Every AI output must reference correct chunk_id(s).

### Writing Style Guidelines
- Grade level: Flesch-Kincaid 8–10 (simple, clear)
- Tone: Neutral, educational, supportive
- Format: short paragraphs, bullet points when possible

## Constraints

- Chatbot must refuse to answer anything outside the book scope.
- Maximum answer length: 200 tokens unless user explicitly requests a longer explanation.
- No hallucinated citations; if retrieval fails, respond safely.
- All internal reasoning must follow SpecifyKit Task → Agent → Contract structure.

## Operational Rules

- Always perform RAG first before answering.
- If user selects text, bypass full retrieval and use ONLY that text.
- If selected text is < 10 characters, fallback to normal RAG.

## Success Criteria

- 100% answers grounded in book's actual text
- Zero hallucinations in testing
- Latency under 1.5 seconds per query (FastAPI + Qdrant hybrid search)
- All answers include book-based citations
- Smooth integration with SpecifyKit + Claude CLI workflows

## Output Quality Benchmarks

- Accuracy: Must match source text exactly
- Relevance: Only content that answers the user's question
- Clarity: Understandable by non-technical readers
- Consistency: Identical input → identical answer every time

## Governance

All PRs/reviews must verify compliance; Complexity must be justified; Use [GUIDANCE_FILE] for runtime development guidance

## Response snapshot

Updated the project constitution to version 1.1.0, replacing the previous frontend-focused constitution with RAG-specific requirements for the book chatbot backend. The new constitution maintains the Spec-Driven Development principle while adding RAG-specific principles around source-bound accuracy, transparency, reliability, and performance. The constitution now governs the RAG backend development with strict requirements for grounding responses in book text, proper citation, and deterministic behavior.

## Outcome

- ✅ Impact: Updated constitution to govern RAG backend development with version 1.1.0
- 🧪 Tests: N/A for constitution update
- 📁 Files: Modified .specify/memory/constitution.md with new RAG-focused principles
- 🔁 Next prompts: Ready for specification phase
- 🧠 Reflection: Constitution successfully updated to focus on RAG backend requirements while maintaining Spec-Driven Development principles

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - Constitution updated successfully
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin specification phase for RAG backend