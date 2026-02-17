---
name: ingesting-rag-content
description: Specialized skill for ingesting rag content
type: skill
version: 1.1.0
category: retrieval
agents: [ai-app-developer]
knowledge: [best-practices.json]
tools: ["antigravity-rag"]
related_skills: [retrieving-rag-context]
templates: ["none"]
---

# Ingesting RAG Content

Automated process for indexing new documents into the factory's Qdrant vector store using standardized Parent-Child retrieval patterns.

## Prerequisites
- Python 3.10+ environment with `cursor-factory` env active.
- Access to `D:/ebooks` or target document path.
- `antigravity-rag` MCP server active (configured in `c:\Users\wpoga\.gemini\antigravity\mcp_config.json`).

## When to Use
- When new reference materials (PDF) are added to the project.
- When an agent discovers new domain knowledge that needs to be persistent.

## Process
1.  **Identify source**: Locate the PDF to be ingested.
2.  **Call tool**: Use `@tool mcp_antigravity-rag_ingest_document` with the absolute path.
3.  **Monitor logs**: Ensure the Parent-Child splitting (chunking) completes successfully.
4.  **Verify**: Call `list_library_sources` to confirm registration.

## Level 3 Resources

### Scripts
- `scripts/validate_ingestion.py`: Runs a health check on the Qdrant `ebook_library` collection.
- `scripts/ai/rag/rag_optimized.py`: The core ingestion engine logic.

### References
- `references/rag-architecture.md`: Explains the Parent-Child chunking strategy and Qdrant storage schema.

## Important Rules
- **PDF Only**: In the current optimized version, only PDF documents are supported for Parent-Child splitting.
- **UTF-8 Only**: Ensure environment variables (`$env:PYTHONIOENCODING="utf-8"`) are set.
- **Incremental indexing**: The system supports adding to existing Qdrant collections.
- **Local Embeddings**: Uses `BAAI/bge-small-en-v1.5` (via FastEmbed) for performance.

## Best Practices
- **Recursive Splitting**: Always use recursive character splitting to maintain paragraph integrity.
- **Absolute Paths**: Store absolute paths in metadata to ensure reliable document opening.
- **Validation**: Run `scripts/validate_ingestion.py` after bulk ingestion.
```
