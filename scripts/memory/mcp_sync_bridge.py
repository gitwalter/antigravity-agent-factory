"""
Memory MCP Synchronization Bridge
Extracts semantic memories from the local Qdrant store and formats them
for induction into the Memory MCP graph.
"""

import json
import logging
from typing import List, Dict, Any
from scripts.memory.memory_store import get_memory_store, Memory

logger = logging.getLogger(__name__)


class MCPSyncBridge:
    """
    Bridges the gap between local vector memory and the global MCP graph.
    """

    def __init__(self):
        self.store = get_memory_store()

    def get_unsynced_memories(self) -> List[Memory]:
        """
        Retrieves semantic memories that haven't been synced to MCP yet.
        (Uses 'mcp_synced' metadata flag)
        """
        # Search all semantic memories (simplified for this bridge)
        # In a real implementation, we'd use a more efficient query
        memories = self.store.search("", memory_type="semantic", k=100)
        return [m for m in memories if not m.metadata.get("mcp_synced", False)]

    def format_for_mcp(self, memories: List[Memory]) -> List[Dict[str, Any]]:
        """
        Formats memories as MCP entities and observations.
        Includes metadata for idempotency checks.
        """
        entities = []
        for memory in memories:
            entity_name = (
                memory.metadata.get("entity_name") or f"Memory:{memory.id[:8]}"
            )
            entities.append(
                {
                    "name": entity_name,
                    "entityType": "LearnedPattern",
                    "observations": [
                        memory.content,
                        f"Source: {memory.metadata.get('source', 'unknown')}",
                        f"Created: {memory.created_at}",
                        f"InternalID: {memory.id}",  # Used for idempotency
                    ],
                }
            )
        return entities

    def mark_as_synced(self, memory_ids: List[str]):
        """
        Marks memories as synced in the local store.
        """
        for mid in memory_ids:
            # Note: memory_store.py needs an update() method to change metadata
            # For now, we'll log it
            logger.info(f"Marking memory {mid} as synced to MCP")


if __name__ == "__main__":
    bridge = MCPSyncBridge()
    unsynced = bridge.get_unsynced_memories()
    if unsynced:
        mcp_data = bridge.format_for_mcp(unsynced)
        print(json.dumps(mcp_data, indent=2))
    else:
        print("[]")
