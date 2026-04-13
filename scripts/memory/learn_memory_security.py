"""
Synthesis Script: Memory Security & Test Isolation
Captures the architecture-critical lesson of isolating Qdrant during test runs
to prevent production data loss.
"""

import sys
import os
from datetime import datetime

# Ensure project root in sys.path
sys.path.append(os.getcwd())

from scripts.memory.memory_store import get_memory_store
from scripts.memory.memory_config import COLLECTION_SEMANTIC


def learn_security():
    store = get_memory_store()

    # 1. Semantic Lesson (The Truth)
    store.add_memory(
        content="Production Memory Isolation Protocol: All Qdrant-related test fixtures must be centralized in the root 'tests/conftest.py' and utilize 'QDRANT_PATH' or 'RAG_COLLECTION_PREFIX' environment variables to ensure strict isolation from production data. Local 'conftest.py' files with hardcoded 'localhost:6333' connections are strictly forbidden to prevent accidental data erasure.",
        metadata={
            "category": "security",
            "topic": "Test Isolation",
            "type": "best_practice",
            "impact": "CRITICAL",
        },
        memory_type=COLLECTION_SEMANTIC,
    )

    # 2. Procedural Lesson (The How-To)
    store.add_memory(
        content="How to verify Test Isolation in Antigravity: 1. Insert a 'Production Sentinel' memory in the production Qdrant collection. 2. Run the full test suite. 3. Query the production collection for the sentinel ID. 4. If the sentinel remains, the isolation is functional.",
        metadata={"category": "workflow", "topic": "Verification", "type": "protocol"},
        memory_type="memory_procedural",
    )

    print(
        f"[{datetime.now().isoformat()}] Successfully synthesized Memory Security lessons."
    )


if __name__ == "__main__":
    try:
        learn_security()
    except Exception as e:
        print(f"Failed to store learnings: {e}")
        sys.exit(1)
