---
name: inspecting-rag-catalog
description: Inspect and list the contents of the Qdrant RAG ebook library
type: skill
version: 1.0.0
category: retrieval
agents: [python-ai-specialist, ai-app-developer]
knowledge: []
tools: ["antigravity-rag"]
related_skills: [retrieving-rag-context, ingesting-rag-content]
templates: ["none"]
---

# Inspecting RAG Catalog

Deterministic process for answering "What's in our RAG?" by listing all indexed sources.

## When to Use
- When asked what documents are in the RAG system.
- When verifying ingestion success.
- When planning which sources to query.
- Before ingesting new content (to avoid duplicates).

## Prerequisites
- Active Qdrant vector store with at least one indexed document (running via Docker).
- FastMCP RAG Server must be actively running via `scripts/mcp/servers/rag/start_rag_server.bat` (exposing SSE on port 8000).

## Process
1. **Fetch Catalog Data**:
   - Execute the native catalog script: `python "scripts/list_ebooks.py"` locally from this skill directory.
   - Wait for the JSON response containing the list of sources.
2. **Present results**: Parse the JSON string and display the list of unique PDF sources with their paths.
3. **Summarize**: Report the total count and topic areas covered.

## Important Rules
- **No semantic search needed**: This is a metadata-only operation, not a vector search.
- **Exact tool**: Always use `list_library_sources`, never `search_library` for catalog queries.

## Best Practices
- Run this before ingesting new content to check for duplicates.
- Use the source list to inform which topics are queryable via `retrieving-rag-context`.
