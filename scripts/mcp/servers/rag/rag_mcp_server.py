import os
import sys
import logging
import warnings
import contextlib
from starlette.responses import JSONResponse
from starlette.types import Scope, Receive, Send
from fastmcp import FastMCP

# =============================================================================
# STDOUT PROTECTION FOR MCP STDIO PROTOCOL
# =============================================================================

# Capture real stdout for the MCP transport
_real_stdout = sys.stdout

# Redirect global stdout to stderr to catch all noise during imports and execution
sys.stdout = sys.stderr

warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.WARNING, stream=sys.stderr)

# Project root setup
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
if project_root not in sys.path:
    sys.path.append(project_root)

# Initialize FastMCP
# Initialize FastMCP
# FastMCP 3.0 handles the server execution and SSE transport
mcp = FastMCP("Antigravity RAG Server")


# Lazy RAG Initialization
_rag_instance = None


def _get_rag():
    global _rag_instance
    if _rag_instance is None:
        from scripts.ai.rag.rag_optimized import get_rag

        _rag_instance = get_rag(warmup=True)
    return _rag_instance


@mcp.tool()
def search_library(query: str) -> str:
    """
    Search the ebook library for relevant technical information.
    Uses Parent-Child retrieval to return full context chunks instead of fragments.
    """
    rag = _get_rag()
    documents = rag.query(query)
    if not documents:
        return "No relevant information found in the ebook library."

    formatted = []
    for i, doc in enumerate(documents, 1):
        source = os.path.basename(doc.metadata.get("source", "Unknown"))
        formatted.append(f"### Result {i} (Source: {source})\n\n{doc.page_content}")

    return "\n\n---\n\n".join(formatted)


@mcp.tool()
def get_ebook_toc(document_name: str) -> str:
    """
    Retrieves the deterministic Table of Contents for a specific document in the library.
    Use this to get an exact outline of an ebook before searching.
    Supply the document name or a fuzzy match of its title (e.g., 'Russell').
    """
    rag = _get_rag()
    toc_content = rag.get_toc(document_name)

    if toc_content:
        return toc_content
    return f"No Table of Contents found for document matching '{document_name}'."


@mcp.tool()
def ingest_document(file_path: str) -> str:
    """Ingest a PDF into the RAG vector store using optimized Parent-Child strategy."""
    rag = _get_rag()
    rag.ingest_ebook(file_path)
    return f"Successfully ingested: {file_path}"


@mcp.tool()
def list_library_sources() -> str:
    """List all unique documents currently indexed in the RAG system."""
    rag = _get_rag()
    sources = {
        os.path.basename(doc.metadata["source"])
        for key in rag.store.yield_keys()
        if (doc := rag.store.mget([key])[0]) and "source" in doc.metadata
    }
    if not sources:
        return "Library is empty."
    return "Indexed Documents:\n- " + "\n- ".join(sorted(sources))


if __name__ == "__main__":
    import os

    transport = os.environ.get("MCP_TRANSPORT", "stdio")

    # Ensure stdout remains protected for pure MCP output
    sys.stdout = _real_stdout

    if transport.lower() == "sse":
        print(
            "Starting Antigravity RAG MCP Server (Native SSE Mode) on port 8000",
            file=sys.stderr,
        )
        # Run using the native FastMCP runner for HTTP/SSE clients
        mcp.run(transport="sse", host="127.0.0.1", port=8000)
    else:
        print(
            "Starting Antigravity RAG MCP Server (Native STDIO Mode)",
            file=sys.stderr,
        )
        # Run using the native FastMCP runner for the IDE/Antigravity
        mcp.run(transport="stdio")
