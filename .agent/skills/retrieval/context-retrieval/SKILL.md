---
agents:
- system-architecture-specialist
- workflow-quality-specialist
- knowledge-operations-specialist
category: retrieval
description: 'Actively retrieve context from the Dual-Storage Cognitive Memory system (Qdrant & SQLite) for seamless IDE integration.'
knowledge:
- cognitive-memory-patterns.json
name: context-retrieval
related_skills:
- managing-memory
templates:
- none
tools:
- search_memory
type: skill
version: 1.0.0
references:
- none
settings:
  auto_approve: true
  retry_limit: 3
  timeout_seconds: 60
  safe_to_parallelize: true
  orchestration_pattern: standard
---
# Context Retrieval (Antigravity Architecture)

A cognitive agent must not operate in isolation. You have access to the `search_memory` tool provided by the RAG MCP Server. Use this skill to actively recall experiences, procedural knowledge, tools, and entities.

## When to Use
- You are starting a new implementation plan and need to check how similar tasks were resolved.
- You hit a stack-trace or bug and want to check if the error is resolved in `memory_semantic`.
- You interact with Plane MCP tools and need to recall specific task UUIDs from `memory_entity`.
- You are looking for an exact factory workflow to execute in `memory_procedural`.

## Process
1. Decide which memory tier contains the data type you need:
    - **memory_procedural**: Workflows, Skills, Scripts.
    - **memory_toolbox**: Capabilities, MCP actions, script descriptions.
    - **memory_summary**: Post-session logs and high-level conversation synopses.
    - **memory_semantic**: Condensed rules, facts, architectural patterns.
    - **memory_entity**: Proper nouns, system names, file paths, UUIDs.
2. Use the `search_memory` MCP tool to retrieve documents from that specific collection.
3. Inject the retrieved insights into your immediate task logic.

### Example: Error Resolution

```python
# Thought: I hit a ModuleNotFoundError on 'scripts.memory'. Let's check semantic memory.
call:mcp_server:search_memory(query="ModuleNotFoundError scripts.memory PYTHONPATH", collection="memory_semantic")
```

### Example: Finding a Workflow

```python
# Thought: The user told me to do an Alpha Factor Mining run. Let's retrieve the workflow.
call:mcp_server:search_memory(query="alpha factor mining", collection="memory_procedural")
```

## Prerequisites
- The Qdrant Docker memory backend must be running on `localhost:6333`.
- The `qdrant-rag` MCP server must be active (provides `search_memory` tool).
- Access to the Python scripting environment in `/scripts/memory`.

## Best Practices
- **Do not guess paths**: If you need a script, retrieve its location from `memory_procedural` or `memory_toolbox`.
- **Pre-fetch**: Always fetch context *before* proposing architectural designs in `implementation_plan.md`.
- **Tag the Memory**: In the future when triggering tool calls (like creating an issue), ensure the description explicitly mentions the entities so the background `sessionEnd` hook writes it clearly to the cognitive index.
