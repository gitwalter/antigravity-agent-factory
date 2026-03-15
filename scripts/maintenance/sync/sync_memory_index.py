#!/usr/bin/env python3
"""
sync_memory_index.py
Bridges system catalogs (RAG, Self-Optimization, Skills) into the Memory MCP.
Ensures the agent has "consciousness" of available capabilities.
"""

import json
import sys
import os
from pathlib import Path

# Mock or actual MCP interaction logic would go here
# For this environment, we'll use the memory MCP tool if available,
# or simulate the "Consciousness Bridge" by creating a consolidated knowledge entity.


def sync_knowledge_to_memory(root_dir):
    knowledge_dir = Path(root_dir) / ".agent" / "knowledge"

    catalogs = {
        "rag": "rag-knowledge-catalog.json",
        "self_optimization": "self-optimization-catalog.json",
        "skills": "skill-catalog.json",
    }

    consciousness_data = {
        "entityName": "System_Consciousness",
        "entityType": "System_Bridge",
        "observations": [],
    }

    print("--- Consciousness Bridge Sync ---")

    for key, filename in catalogs.items():
        catalog_path = knowledge_dir / filename
        if not catalog_path.exists():
            print(f"Warning: Catalog {filename} missing at {catalog_path}")
            continue

        try:
            with open(catalog_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Extract key capabilities for Memory
            desc = data.get("description", "No description")
            version = data.get("version", "unknown")

            consciousness_data["observations"].append(
                f"Catalog [{key.upper()}] (v{version}): {desc}"
            )

            if key == "rag":
                rag_stats = data.get("system_components", {})
                consciousness_data["observations"].append(
                    f"RAG Infrastructure: {list(rag_stats.keys())}"
                )

            if key == "self_optimization":
                phases = data.get("phases", {})
                for phase, details in phases.items():
                    count = len(details.get("scripts", details.get("skills", [])))
                    consciousness_data["observations"].append(
                        f"Maintenance Phase [{phase.upper()}]: {count} mechanisms available."
                    )

            print(f"[+] Processed {filename}")

        except Exception as e:
            print(f"Error processing {filename}: {e}")

    # Final Summary for Agent Consciousness
    consciousness_data["observations"].append(
        "Bridge Status: Active. Agents should query 'System_Consciousness' for operational capabilities."
    )

    # Output for the agent to use with memory MCP
    print("\n--- Consolidated Memory Payload ---")
    print(json.dumps(consciousness_data, indent=2))

    # In a real environment, we'd call mcp_memory_create_entities here.
    return True


if __name__ == "__main__":
    root = Path(__file__).parent.parent.parent
    sync_knowledge_to_memory(root)
    sys.exit(0)
