---
description: Patterns for using FAISS MCP tools to ingest documents and perform semantic
  retrieval.
name: rag-retrieval
type: skill
---
# RAG Retrieval Skill

Patterns for using the `antigravity-rag` tools to ingest documents into Qdrant and perform semantic retrieval (Parent-Child strategy).

## When to Use
- When the assistant needs to answer questions based on documents that are not part of its base training data.
- To provide source-grounded answers for technical queries.
- When new domain-specific knowledge is added to the project via external files.

## Prerequisites
- `antigravity-rag` server must be running and configured in `mcp_config.json`.
- Documents must be in supported PDF format (standardized for Parent-Child).
- Python environment with `qdrant-client` and `fastembed` installed.

## Tools Used
- `mcp_antigravity-rag_ingest_document`: Adds external documents (PDF) to the Qdrant vector store.
- `mcp_antigravity-rag_search_library`: Performs semantic search and retrieves parent chunks for rich context.
- `mcp_antigravity-rag_list_library_sources`: Lists all unique documents currently indexed.
- `mcp_local-faiss-mcp_search_semantic`: Performs pure semantic search without LLM generation.

## Process

1. **Document Ingestion**
   - Use `ingest_document` to index new knowledge.
   - Example: `mcp_local-faiss-mcp_ingest_document(path="./docs/manual.pdf")`

2. **RAG Workflow**
   - When a user asks a question about indexed content, use `query_rag_store`.
   - The tool will perform the retrieval and return the synthesized answer with sources.
   - Example: `mcp_local-faiss-mcp_query_rag_store(query="How do I configure the server?")`

3. **Pure Semantic Search**
   - If you only need relevant chunks without an LLM-synthesized answer, use `search_semantic`.
   - Example: `mcp_local-faiss-mcp_search_semantic(query="installation steps")`

## Patterns

### Handling New Data
When the user provides new files or links that should be "remembered":
1. Save the file to a local path if it isn't already.
2. Call `ingest_document`.
3. Confirm ingestion to the user.

### Question Answering
When the user asks "How do I..." or "What is..." regarding the project context:
1. Call `search_library` first to see if the answer is in the vector base.
2. If no relevant info is found, fall back to general knowledge or other retrieval tools.

## Best Practices
- **Metadata first**: Ensure documents have clear titles and versions before ingestion.
- **Query refinement**: If retrieval fails, try rephrasing the query to use more specific keywords.
- **Chunk size**: Use the default 1000-character chunk size for balanced retrieval accuracy.
- **Verify ingestion**: Always check the catalog after ingestion to ensure the document was correctly processed.
