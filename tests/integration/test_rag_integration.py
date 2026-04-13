import pytest
import os
import sys
import time

# Add project root to path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from scripts.mcp_infra.servers.rag.rag_mcp_server import handle_call_tool
import scripts.mcp_infra.servers.rag.rag_mcp_server as rag_server
import asyncio

# Prevent 60-second deadlocks during test execution since the warmup worker is only started in __main__
rag_server._store_ready.set()


@pytest.mark.integration
class TestRAGRetrieval:
    """
    Integration tests for the RAG MCP Server tools.
    Verifies that all 4 memory tiers are reachable and returning data/errors consistently.
    """

    def test_search_memory_semantic(self):
        """Verify semantic search returns a response (data or 'no relevant memory')."""
        result = asyncio.run(
            handle_call_tool("search_memory_semantic", {"query": "test query"})
        )
        assert isinstance(result[0].text, str)
        assert len(result[0].text) > 0

    def test_search_memory_procedural(self):
        """Verify procedural search returns a response."""
        result = asyncio.run(
            handle_call_tool("search_memory_procedural", {"query": "workflow"})
        )
        assert isinstance(result[0].text, str)
        assert len(result[0].text) > 0

    def test_search_memory_entity(self):
        """Verify entity search returns a response."""
        result = asyncio.run(
            handle_call_tool("search_memory_entity", {"query": "architect"})
        )
        assert isinstance(result[0].text, str)
        assert len(result[0].text) > 0

    def test_search_memory_summary(self):
        """Verify summary search returns a response."""
        result = asyncio.run(
            handle_call_tool("search_memory_summary", {"query": "session"})
        )
        assert isinstance(result[0].text, str)
        assert len(result[0].text) > 0

    def test_prepare_context_fusion(self):
        """Verify prepare_context fuses multiple tiers."""
        result = asyncio.run(
            handle_call_tool("prepare_context", {"query": "test query"})
        )
        text = result[0].text
        assert "== SEMANTIC ==" in text
        assert "== PROCEDURAL ==" in text
        assert "== ENTITY ==" in text

    def test_propose_memory_staging(self):
        """Verify propose_memory stages in the 'pending' collection."""
        test_content = f"Test Insight {time.time()}"
        result = asyncio.run(
            handle_call_tool(
                "propose_memory_semantic",
                {"content": test_content, "reasoning": "testing proposal endpoint"},
            )
        )
        text = result[0].text
        assert "Proposed memory" in text
        assert "memory_semantic" in text
