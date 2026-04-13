"""
Antigravity RAG MCP Server — Diagnostic Build
-------------------------------------------------
Logs every step to a file so we can see what the IDE's subprocess is doing.
"""

import os
import sys
import logging
import warnings
import asyncio
import threading
import time

LOG_FILE = r"C:\Users\wpoga\.gemini\antigravity\rag_server_debug.log"


def log(msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{time.strftime('%H:%M:%S')}] {msg}\n")
        f.flush()


log("=== SERVER STARTING ===")
log(f"Python: {sys.executable}")
log(f"CWD: {os.getcwd()}")
log(f"sys.path[:3]: {sys.path[:3]}")

# Ensure the project root is in sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
if project_root not in sys.path:
    sys.path.append(project_root)
    log(f"Added project root: {project_root}")

log("Importing mcp...")
from mcp.server import Server
from mcp.server.stdio import stdio_server
import mcp.types as types

log("mcp imported OK")

# Setup silent logging to stderr only
logging.basicConfig(level=logging.ERROR, stream=sys.stderr)
warnings.filterwarnings("ignore")

server = Server("Antigravity RAG Server")
log("Server object created")

# ---------------------------------------------------------------------------
# Global store with background warmup
# ---------------------------------------------------------------------------
_store = None
_store_lock = threading.Lock()
_store_ready = threading.Event()


def _warmup_worker():
    global _store
    log("Warmup thread starting...")
    try:
        t0 = time.time()
        # With lazy loading, these imports and get_memory_store() are near-instant
        from scripts.memory.memory_store import get_memory_store

        store = get_memory_store()
        log(f"  MemoryStore initialized lazily ({time.time()-t0:.2f}s)")

        # Trigger model loading in background
        log("  Triggering background model load (warmup search)...")
        # This will block the thread for 10-20s, but not the MCP server responder
        try:
            store.search("warmup", memory_type="memory_semantic", k=1)
            log(f"  Warmup search COMPLETE ({time.time()-t0:.2f}s)")
        except Exception as e:
            log(f"  Warmup search failed (expected if DB empty): {e}")

        _store = store
        log(f"Warmup thread finished in {time.time()-t0:.2f}s")
    except Exception as e:
        import traceback

        log(f"Warmup CRITICAL ERROR: {e}\n{traceback.format_exc()}")
    finally:
        _store_ready.set()
        log("_store_ready event SET")


def get_store(wait: bool = True):
    """Get the store, optionally waiting for it to be fully ready (model loaded)."""
    if _store is not None:
        return _store

    if wait:
        log("get_store() called - waiting for store readiness...")
        ready = _store_ready.wait(timeout=30)  # 30 second timeout for model loading
        if not ready:
            log("WARNING: Store warmup timeout. Proceeding with lazy instance.")

    from scripts.memory.memory_store import get_memory_store

    return get_memory_store()


# ---------------------------------------------------------------------------
# Tool Definitions
# ---------------------------------------------------------------------------


@server.list_tools()
async def handle_list_tools():
    log("list_tools() called")
    return [
        types.Tool(
            name="search_memory_entity",
            description="Search entity tier for Agent Personas, system integrations, user profiles.",
            inputSchema={
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        ),
        types.Tool(
            name="search_memory_semantic",
            description="Search semantic tier for rules, idioms, expert knowledge.",
            inputSchema={
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        ),
        types.Tool(
            name="search_memory_procedural",
            description="Search procedural tier for workflows, blueprints, SOPs.",
            inputSchema={
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        ),
        types.Tool(
            name="search_memory_summary",
            description="Search summary tier for distilled session logs.",
            inputSchema={
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        ),
        types.Tool(
            name="prepare_context",
            description="Fuses Semantic, Procedural, and Entity memory for a query.",
            inputSchema={
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        ),
        types.Tool(
            name="add_memory_entity",
            description="Store direct facts or properties about an entity into memory_entity.",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string"},
                    "metadata": {"type": "object"},
                },
                "required": ["content"],
            },
        ),
        types.Tool(
            name="add_memory_summary",
            description="Store high-level session or phase summaries into memory_summary.",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string"},
                    "metadata": {"type": "object"},
                },
                "required": ["content"],
            },
        ),
        types.Tool(
            name="add_memory_episodic",
            description="Store direct observations and logs into episodic memory.",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string"},
                    "metadata": {"type": "object"},
                },
                "required": ["content"],
            },
        ),
        # New Enriched Tools
        types.Tool(
            name="add_memory_semantic",
            description="Store a verified rule or distilled knowledge into memory_semantic.",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string"},
                    "metadata": {"type": "object"},
                },
                "required": ["content"],
            },
        ),
        types.Tool(
            name="add_memory_procedural",
            description="Store a workflow, blueprint, or tactical procedure into memory_procedural.",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string"},
                    "metadata": {"type": "object"},
                },
                "required": ["content"],
            },
        ),
        types.Tool(
            name="add_memory_toolbox",
            description="Store a capability or script usage pattern into memory_toolbox.",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string"},
                    "metadata": {"type": "object"},
                },
                "required": ["content"],
            },
        ),
        # Proposals (Safety Layer)
        types.Tool(
            name="propose_memory_semantic",
            description="Propose a new rule or generalized insight to memory_semantic (Requires User Approval).",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string"},
                    "reasoning": {"type": "string"},
                },
                "required": ["content", "reasoning"],
            },
        ),
        types.Tool(
            name="propose_memory_procedural",
            description="Propose a new workflow or step-by-step logic to memory_procedural (Requires User Approval).",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string"},
                    "reasoning": {"type": "string"},
                },
                "required": ["content", "reasoning"],
            },
        ),
        types.Tool(
            name="propose_memory_toolbox",
            description="Propose a new script usage or capability to memory_toolbox (Requires User Approval).",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string"},
                    "reasoning": {"type": "string"},
                },
                "required": ["content", "reasoning"],
            },
        ),
    ]


def _search_tier(query: str, collection: str, k: int = 5) -> str:
    log(f"_search_tier({collection}, q={query[:40]})")
    store = get_store()
    results = store.search(query, memory_type=collection, k=k, threshold=0.1)
    log(f"  -> {len(results)} results")
    if not results:
        return f"No matches in {collection}."
    return "\n\n".join([f"**ID**: {r.id}\n{r.content}" for r in results])


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict):
    log(f"call_tool({name}) called")
    query = arguments.get("query", "*")

    if name == "search_memory_semantic":
        return [
            types.TextContent(type="text", text=_search_tier(query, "memory_semantic"))
        ]
    elif name == "search_memory_procedural":
        return [
            types.TextContent(
                type="text", text=_search_tier(query, "memory_procedural")
            )
        ]
    elif name == "search_memory_entity":
        return [
            types.TextContent(type="text", text=_search_tier(query, "memory_entity"))
        ]
    elif name == "search_memory_summary":
        return [
            types.TextContent(type="text", text=_search_tier(query, "memory_summary"))
        ]
    elif name == "prepare_context":
        sections = []
        for tier in ["memory_semantic", "memory_procedural", "memory_entity"]:
            results = get_store().search(query, memory_type=tier, k=3, threshold=0.1)
            tier_label = tier.replace("memory_", "").upper()
            content = "\n".join([r.content for r in results]) or "No matches."
            sections.append(f"== {tier_label} ==\n{content}")
        return [
            types.TextContent(
                type="text", text="\n\n=========================\n\n".join(sections)
            )
        ]
    elif name.startswith("add_memory_"):
        collection = name.replace("add_", "")
        if collection == "memory_episodic":
            collection = "episodic"  # Map alias just in case

        content = arguments.get("content")
        metadata = arguments.get("metadata", {})
        memory_id = get_store().add_memory(content, metadata, memory_type=collection)
        return [
            types.TextContent(
                type="text",
                text=f"Successfully added memory to {collection}. ID: {memory_id}",
            )
        ]

    elif name.startswith("propose_memory_"):
        collection = name.replace("propose_", "")
        content = arguments.get("content")
        reasoning = arguments.get("reasoning", "")

        # We store the intended target collection in the proposal metadata or reasoning so the user sees it
        full_reasoning = f"Target Tier: {collection}\n{reasoning}"
        from scripts.memory.memory_store import MemoryProposal
        import uuid

        try:
            full_content = f"{content}\n\n[Context/Reasoning]:\n{full_reasoning}"
            proposal = MemoryProposal(
                id=str(uuid.uuid4()), content=full_content, source="agent"
            )
            proposal_id = get_store().add_pending_proposal(proposal)
            return [
                types.TextContent(
                    type="text",
                    text=f"Proposed memory for user review to {collection}. Proposal ID: {proposal_id}",
                )
            ]
        except Exception as e:
            return [types.TextContent(type="text", text=f"ERROR: {str(e)}")]
    else:
        raise ValueError(f"Unknown tool: {name}")


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------
async def main():
    log("asyncio main() starting, launching stdio_server...")
    async with stdio_server() as (read_stream, write_stream):
        log("stdio_server ready — entering server.run()")
        await server.run(
            read_stream, write_stream, server.create_initialization_options()
        )
    log("server.run() exited")


if __name__ == "__main__":
    log("Starting warmup background thread...")
    warmup_thread = threading.Thread(target=_warmup_worker, daemon=True)
    warmup_thread.start()
    log("Warmup thread started. Starting asyncio event loop...")
    asyncio.run(main())
    log("=== SERVER EXITED ===")
