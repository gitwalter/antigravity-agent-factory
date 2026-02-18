import os
import sys
import logging
import warnings

# =============================================================================
# STDOUT PROTECTION FOR MCP STDIO PROTOCOL
# =============================================================================
# MCP communicates via stdout/stdin. Stray print()/warnings to stdout corrupt
# the protocol. We redirect Python's stdout to stderr for all non-MCP output,
# then let FastMCP use the real stdout internally for protocol messages.
# =============================================================================

# Save real stdout before any redirection
_real_stdout = sys.stdout

# Redirect print() to stderr and suppress noisy warnings
sys.stdout = sys.stderr
warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.WARNING, stream=sys.stderr)
logger = logging.getLogger("rag_mcp_server")

# Suppress 3rd party logs that might leak or spam stderr
logging.getLogger("mcp").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("qdrant_client").setLevel(logging.WARNING)

# Restore real stdout for FastMCP protocol communication
sys.stdout = _real_stdout

from mcp.server.fastmcp import FastMCP

# Project root is set via PYTHONPATH in mcp_config.json
# But ensure it's also on sys.path for safety
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
if project_root not in sys.path:
    sys.path.append(project_root)

# Initialize FastMCP server
mcp = FastMCP("Antigravity RAG Server")

# Lazy singletons — RAG backend loads only on first tool call
_agentic_rag = None
_rag_instance = None


def _protect_stdout(fn):
    """Decorator that redirects stdout to stderr during RAG operations."""

    def wrapper(*args, **kwargs):
        _saved = sys.stdout
        sys.stdout = sys.stderr
        try:
            return fn(*args, **kwargs)
        finally:
            sys.stdout = _saved

    return wrapper


@_protect_stdout
def _init_rag():
    global _rag_instance
    if _rag_instance is None:
        from scripts.ai.rag.rag_optimized import get_rag

        _rag_instance = get_rag(warmup=True)
    return _rag_instance


@mcp.tool()
def search_library(query: str) -> str:
    """
    Search the ebook library.
    Returns the most relevant document snippets found in the vector store.
    """
    rag = _init_rag()

    _saved = sys.stdout
    sys.stdout = sys.stderr
    try:
        # Direct query to OptimizedRAG (returns List[Document])
        documents = rag.query(query)
    finally:
        sys.stdout = _saved

    if not documents:
        return "No information found in the library."

    # Format results
    formatted_results = []
    for i, doc in enumerate(documents, 1):
        source = doc.metadata.get("source", "Unknown")
        content = doc.page_content
        formatted_results.append(
            f"### Result {i} (Source: {os.path.basename(source)})\n{content}\n"
        )

    return "\n".join(formatted_results)


@mcp.tool()
def ingest_document(file_path: str) -> str:
    """
    Ingest a new PDF document into the ebook library.
    This will process the document using Parent-Child splitting and store
    it in the local vector database.
    """
    if not os.path.exists(file_path):
        return f"Error: File not found at {file_path}"

    if not file_path.lower().endswith(".pdf"):
        return "Error: Only PDF documents are currently supported."

    try:
        rag = _init_rag()
        _saved = sys.stdout
        sys.stdout = sys.stderr
        try:
            rag.ingest_ebook(file_path)
        finally:
            sys.stdout = _saved
        return f"Successfully ingested: {file_path}"
    except Exception as e:
        return f"Error during ingestion: {str(e)}"


@mcp.tool()
def list_library_sources() -> str:
    """
    List all unique document sources currently indexed in the library.
    """
    try:
        rag = _init_rag()
        client = rag.client

        collections = client.get_collections().collections
        exists = any(c.name == "ebook_library" for c in collections)

        if not exists:
            return "The ebook library collection does not exist yet."

        points = client.scroll(
            collection_name="ebook_library", limit=1000, with_payload=True
        )[0]
        sources = {
            p.payload.get("metadata", {}).get("source") for p in points if p.payload
        }
        clean_sources = sorted([s for s in sources if s])

        if not clean_sources:
            return "The library is currently empty."

        return "Current library sources:\n- " + "\n- ".join(clean_sources)
    except Exception as e:
        return f"Error listing sources: {str(e)}"


if __name__ == "__main__":
    # Run as SSE server on port 8000
    # SSE allows the server to be persistent and running outside the IDE's process tree
    # This solves the dispatch/encoding issues seen with STDIO
    print(
        "Starting Antigravity RAG MCP Server on http://localhost:8000/sse",
        file=sys.stderr,
    )
    try:
        mcp.run(transport="sse")
    except Exception as e:
        print(f"Server failed: {e}", file=sys.stderr)
        sys.exit(1)
