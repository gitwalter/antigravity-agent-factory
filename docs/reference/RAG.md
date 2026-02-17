# Antigravity RAG System

The Antigravity Agent Factory uses a reasoning-driven **Agentic RAG** architecture powered by **Qdrant**, **LangGraph**, and **HuggingFace Embeddings**.

## Architecture Overview

Our system avoids the pitfalls of naive semantic search by using a multi-level **Parent-Child** strategy combined with an **Agentic Loop**:

1.  **Parent Chunks (2000 chars)**: Large, narrative-rich segments stored in a local key-value docstore.
2.  **Child Chunks (400 chars)**: Granular segments embedded into the Qdrant vector store.
3.  **Retrieve**: When a query is received, the system retrieves child matches and resolves them to their parent context.
4.  **Grade (LangGraph)**: The system evaluates retrieved chunks for relevance. If insufficient, it triggers an adaptive fallback.
5.  **Adapt**: If the local library doesn't contain the answer, the system generates a web search query (Tavily) to fill the knowledge gap.

## Technology Stack

- **Vector Database**: [Qdrant](https://qdrant.tech/) (Local instance in `data/rag/qdrant_workspace`)
- **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2` (via HuggingFace)
- **Workflow Orchestration**: [LangGraph](https://langchain-ai.github.io/langgraph/)
- **Framework**: LangChain (ParentDocumentRetriever)
- **MCP Server**: `antigravity-rag` (Python-based stdio server)

## MCP Tools

The `antigravity-rag` server provides the following tools:

### `search_library(query: str)`
Performs semantic search across the ebook library. Returns parent chunks containing the answer and source metadata.

### `ingest_document(file_path: str)`
Processes a PDF document using Parent-Child splitting and adds it to the vector store.
> [!IMPORTANT]
> Currently, only PDF format is supported for the optimized Parent-Child workflow.

### `list_library_sources()`
Lists all unique documents currently indexed in the system.

## Performance
By using local embeddings (`FastEmbed`) and a local Qdrant instance, the system eliminates network latency and ensures data privacy. Typical retrieval time is <100ms on standard CPU hardware.

## Maintenance
- **Validation**: Run `python scripts/validation/sync_artifacts.py` to ensure counts are in sync.
- **Storage**: Data is stored in `data/rag/`. This directory is git-ignored but persistent across sessions.
