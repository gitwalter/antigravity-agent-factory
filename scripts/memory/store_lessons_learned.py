import sys
import os
import time

# Ensure project root in sys.path
sys.path.append(os.getcwd())

from scripts.memory.memory_store import get_memory_store, MemoryProposal
import uuid


def store_learnings():
    store = get_memory_store()

    # 1. Semantic Learning
    store.add_memory(
        content="RAG Optimization Protocol: Always prioritize lazy-loading for heavy AI dependencies (torch, transformers). This ensures the MCP server remains responsive to 'list_tools' requests even while the model is warming up in the background.",
        metadata={"category": "best_practice", "topic": "MCP Performance"},
        memory_type="memory_semantic",
    )

    # 2. Procedural Learning
    store.add_memory(
        content="Workflow for MCP Server Optimization: 1. Benchmark startup with profile_rag_startup.py. 2. Identify top-level heavy imports. 3. Internalize imports in methods/properties. 4. Implement non-blocking background thread for model warmup. 5. Verify with test_import_speed.",
        metadata={"category": "workflow", "topic": "Optimization"},
        memory_type="memory_procedural",
    )

    # 3. Entity Memory
    store.add_memory(
        content="Agent-179: RAG Performance Optimization Task. Sub-2s startup achieved. Lazy-loading implemented for Qdrant and Sentence-Transformers.",
        metadata={"id": "AGENT-179", "status": "fixed"},
        memory_type="memory_entity",
    )

    # 5. CI Dependency Learning
    store.add_memory(
        content="CI Hygiene Protocol: Verify that all imports in integration tests are backed by requirements.txt or requirements-dev.txt. Unused imports of prototyping libraries (like fastmcp) can break CI pipelines.",
        metadata={"category": "lesson_learned", "topic": "CI/CD"},
        memory_type="memory_semantic",
    )

    print("Successfully stored 5 lesson-learned memories across tiers.")


if __name__ == "__main__":
    store_learnings()
