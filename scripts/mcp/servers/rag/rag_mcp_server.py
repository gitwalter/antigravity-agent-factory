import os
import sys
from typing import List, Optional
from mcp.server.fastmcp import FastMCP

# Add the project root to sys.path to allow importing from scripts.ai.rag
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
if project_root not in sys.path:
    sys.path.append(project_root)

# Import the AgenticRAG and get_rag functions
from scripts.ai.rag.agentic_rag import AgenticRAG
from scripts.ai.rag.rag_optimized import get_rag

# Initialize FastMCP server
mcp = FastMCP("Antigravity RAG Server")

# Initialize Agentic RAG (singleton logic handled internally or locally)
_agentic_rag = None


def get_agentic_rag():
    global _agentic_rag
    if _agentic_rag is None:
        _agentic_rag = AgenticRAG()
    return _agentic_rag


@mcp.tool()
def search_library(query: str) -> str:
    """
    Search the ebook library using an Agentic RAG strategy.
    The system grades result relevance and can fallback to web search if needed.
    """
    rag = get_agentic_rag()
    result = rag.query(query)

    generation = result.get("generation", "No information found.")

    if result.get("web_search") == "yes":
        return f"NOTE: Local library results were graded as insufficient. Recommending web search for better coverage.\n\n{generation}"

    return generation


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
        rag = get_rag()
        rag.ingest_ebook(file_path)
        return f"Successfully ingested: {file_path}"
    except Exception as e:
        return f"Error during ingestion: {str(e)}"


@mcp.tool()
def list_library_sources() -> str:
    """
    List all unique document sources currently indexed in the library.
    """
    try:
        rag = get_rag()
        client = rag.client

        collections = client.get_collections().collections
        exists = any(c.name == "ebook_library" for c in collections)

        if not exists:
            return "The ebook library collection does not exist yet."

        # Scroll to find unique sources
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
    # Ensure the RAG storage paths exist relative to project root
    # rag_optimized.py uses "data/rag/..." so it should work fine if started from project root
    mcp.run(transport="stdio")
