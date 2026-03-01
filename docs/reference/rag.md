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

## Deduplication

Documents are deduplicated using two strategies:
- **SHA-256 file hash**: Catches identical content regardless of file path
- **Normalized path check**: Prevents re-ingestion of the same file
- **Override**: `ingest --force` bypasses both checks

## TOC Extraction

Multi-strategy extraction with 3-tier fallback:
1. **PyMuPDF native** (`doc.get_toc()`) — fastest, most reliable
2. **Regex heuristic** (Chapter/Part/Section patterns) — fallback
3. **LLM extraction** (Gemini 2.5 Flash) — last resort

## CLI Commands

```bash
rag_cli.py search <query> [--top-k N]    # Semantic search
rag_cli.py list [--detailed]              # List documents
rag_cli.py ingest <file> [--force]        # Ingest PDF
rag_cli.py delete <name> [--force]        # Delete document
rag_cli.py stats                          # Library statistics
rag_cli.py info <name>                    # Document details
rag_cli.py check-duplicates               # Find duplicates
rag_cli.py scan <dir> [-r]                # Compare dir vs index
rag_cli.py get-source <name>              # Retrieve raw chunks
```

All commands: `conda run -p D:\Anaconda\envs\cursor-factory python scripts/ai/rag/rag_cli.py <cmd>`

## MCP Tools

The `antigravity-rag` server provides:

### `search_library(query: str)`
Performs semantic search across the ebook library. Returns parent chunks containing the answer and source metadata.

### `ingest_document(file_path: str)`
Processes a PDF document using Parent-Child splitting and adds it to the vector store.

### `list_library_sources()`
Lists all unique documents currently indexed in the system.

### `get_ebook_toc(document_name: str)`
Retrieves the Table of Contents for a specific document via fuzzy name matching.

## Performance
Local embeddings and Qdrant eliminate network latency and ensure data privacy. Typical retrieval: <100ms on standard CPU.

## Maintenance
- **Validation**: Run `python scripts/validation/sync_artifacts.py` to ensure counts are in sync.
- **Storage**: Data is stored in `data/rag/`. This directory is git-ignored but persistent across sessions.
