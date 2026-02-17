---
name: ingesting-rag-content
description: Specialized skill for ingesting rag content
type: skill
version: 1.0.0
category: retrieval
agents: [ai-app-developer]
knowledge: [best-practices.json]
tools: ["none"]
related_skills: [skill-generation]
templates: ["none"]
---
# Ingesting Rag Content

Automated process for indexing new documents into the factory's Qdrant vector store using standardized Parent-Child retrieval patterns.

## Prerequisites
- Python 3.10+ environment with `cursor-factory` env active.
- Access to `D:/ebooks` or target document path.
- `antigravity-rag` MCP server active.

## When to Use
- When new reference materials (PDF) are added to the project.
- When an agent discovers new domain knowledge that needs to be persistent.

## Process
1.  **Identify source**: Locate the PDF to be ingested.
2.  **Call tool**: Use `@tool mcp_antigravity-rag_ingest_document` with the absolute path.
3.  **Monitor logs**: Ensure the Parent-Child splitting (chunking) completes successfully.
4.  **Verify**: Call `list_library_sources` to confirm registration.

## Important Rules
- **PDF Only**: In the current optimized version, only PDF documents are supported for Parent-Child splitting.
- **UTF-8 Only**: Ensure environment variables (`$env:PYTHONIOENCODING="utf-8"`) are set.
- **Incremental indexing**: The system supports adding to existing Qdrant collections.
- **Local Embeddings**: Uses `BAAI/bge-small-en-v1.5` (via FastEmbed) for performance.

## Best Practices
- **Recursive Splitting**: Always use recursive character splitting to maintain paragraph integrity.
- **Absolute Paths**: Store absolute paths in metadata to ensure reliable document opening.
- **Validation**: Run `python scripts/ai/rag/validate_index.py` after bulk ingestion.
```
