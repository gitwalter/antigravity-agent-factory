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
- `antigravity-rag` MCP server active (configured in `c:\Users\wpoga\.gemini\antigravity\mcp_config.json`).
- Active Qdrant vector store with at least one indexed document.

## Process
1. **Call catalog tool**: Use `@tool mcp_antigravity-rag_list_library_sources`.
2. **Present results**: Display the list of unique PDF sources with their paths.
3. **Summarize**: Report the total count and topic areas covered.

## Important Rules
- **No semantic search needed**: This is a metadata-only operation, not a vector search.
- **Exact tool**: Always use `list_library_sources`, never `search_library` for catalog queries.

## Best Practices
- Run this before ingesting new content to check for duplicates.
- Use the source list to inform which topics are queryable via `retrieving-rag-context`.
