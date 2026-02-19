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
mcp = FastMCP(
    "Antigravity RAG Server",
    description="Intelligent Parent-Child RAG for Ebooks",
    sse_path="/sse",
    message_path="/messages/",
)

# Shared session state
_session_storage = {"id": None}
base_app = mcp.sse_app()


async def app(scope: Scope, receive: Receive, send: Send):
    """
    Enhanced ASGI Proxy.
    Captures the session_id from GET /sse and forwards POST /sse to /messages/
    """
    if scope["type"] == "http":
        path = scope.get("path", "")
        method = scope.get("method", "")

        # 1. Capture Session ID from GET /sse
        if path == "/sse" and method == "GET":
            from urllib.parse import parse_qs

            qs = parse_qs(scope.get("query_string", b"").decode())
            session_id = qs.get("session_id", [None])[0]
            if session_id:
                _session_storage["id"] = session_id
                print(f"DEBUG: Session Linked: {session_id}", file=sys.stderr)
            await base_app(scope, receive, send)
            return

        # 2. Proxy POST /sse to /messages/ with session persistence
        if path == "/sse" and method == "POST":
            session_id = _session_storage["id"]

            if session_id:
                # Transparently teleport to /messages/
                new_scope = dict(scope)
                new_scope["path"] = "/messages/"
                new_scope["raw_path"] = b"/messages/"

                # Ensure session_id is in query string
                qs_str = scope.get("query_string", b"").decode()
                if f"session_id={session_id}" not in qs_str:
                    new_qs = (
                        f"{qs_str}&session_id={session_id}"
                        if qs_str
                        else f"session_id={session_id}"
                    )
                    new_scope["query_string"] = new_qs.encode()

                print(
                    f"DEBUG: Proxying message to session {session_id}", file=sys.stderr
                )
                await base_app(new_scope, receive, send)
                return
            else:
                # Cold-boot probe: Satisfy initialization handshake
                import json

                body = b""
                # Note: We must be careful not to consume 'receive' if we forward,
                # but here we ARE the terminal handler for this specific probe.
                while True:
                    msg = await receive()
                    if msg["type"] == "http.request":
                        body += msg.get("body", b"")
                        if not msg.get("more_body", False):
                            break

                req_id = None
                try:
                    data = json.loads(body)
                    req_id = data.get("id")
                except Exception:
                    pass

                print(f"DEBUG: Cold-start probe (ID: {req_id})", file=sys.stderr)
                content = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "logging": {},
                            "prompts": {"listChanged": False},
                            "resources": {"listChanged": False, "subscribe": False},
                            "tools": {"listChanged": False},
                        },
                        "serverInfo": {
                            "name": "Antigravity RAG Server",
                            "version": "1.0.0",
                        },
                    },
                }
                res = JSONResponse(content)
                await res(scope, receive, send)
                return

    await base_app(scope, receive, send)


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
    import uvicorn

    sys.stdout = _real_stdout
    print(
        "Starting Antigravity RAG MCP Server (Hybrid SSE Mode) on port 8000",
        file=sys.stderr,
    )
    uvicorn.run(app, host="127.0.0.1", port=8000)
