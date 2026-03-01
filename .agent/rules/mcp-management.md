# Rule: MCP Ecosystem Management

## Context
Governs the strategic orchestration of the Model Context Protocol (MCP) ecosystem to ensure reliable, discoverable, and efficient agentic operations.

## 1. Orchestration Strategy
- **Master Skill**: Use `mcp-orchestration` as the primary guide for selecting tools.
- **Fall-through Logic**:
    1. **Local Context**: First, check the immediate filesystem and environment.
    2. **Grounding (RAG/Memory)**: Use RAG for long-term docs and Memory for dynamic project state.
    3. **External Discovery**: Use Tavily for web-fresh data or missing internal info.

## 2. Server Utilization
- **Memory MCP (P0)**: Mandatory for tracking long-term observations and entity relationships.
- **RAG MCP (P1)**: Mandatory for all document-heavy research (PDFs, Wikis).
- **Research MCP (Tavily) (P2)**: Use for real-time web search and content extraction.
- **Reasoning MCP (SequentialThinking)**: Trigger for complex logic involving more than three dependent steps.
- **Native Plane PMS (P1)**: Mandatory for project tracking. Use the `pms-management` skill for direct backend access (bypasses MCP).

## 3. Implementation Standards
- **Client Pattern**: All factory scripts MUST use the standardized `MultiServerMCPClient` for connection resilience.
- **Resource Cleanup**: Always use `async with` context managers to ensure socket/SSE connection termination.
- **Safety**: Verify all tool arguments against the server's `inputSchema` before invocation.

## 4. Memory MCP — Orientation & Grounding

Memory MCP is the system's **live index** for fast agent orientation. Use it before file-reading for quick context.

### Key Entities (query by name)

| Entity | Type | Use When |
|--------|------|----------|
| `RAG_Library` | system_component | Working with RAG system |
| `RAG_CLI_Commands` | script_usage | Need exact CLI syntax for rag_cli.py |
| `RAG_Skills` | capability_index | Finding which RAG skill to use |
| `System_Self_Optimization` | capability_index | Running maintenance/validation |
| `Agent_Rules_Index` | system_rule | Need rule orientation |

### When to Query Memory MCP

- **Before running any script** → query `<Script>_CLI_Commands` for current syntax
- **Starting a maintenance task** → query `System_Self_Optimization` for available tools
- **Before creating knowledge/skills** → query existing entities for duplicates
- **After modifying a script's CLI** → run `sync_script_registry.py` to update entities

### Convention: WHAT / WHEN / HOW

| Layer | Stores | Who Maintains |
|-------|--------|---------------|
| **Skill** (WHAT/WHEN) | Intent and triggers | Updated manually when purpose changes |
| **Memory MCP** (HOW) | Exact syntax, parameters | Updated by `sync_script_registry.py` or manually |
| **Knowledge** (WHY) | Context, patterns, best practices | Updated during research/learning |

### Mandatory Practices

- **Read First**: Search `mcp_memory_search_nodes` with relevant keywords before sub-tasks.
- **Write Back**: Add key decisions, architectural shifts, and new entity relationships.
- **Keep Current**: After modifying scripts, run the Script Change Protocol (`.agent/rules/script-change-protocol.md`).
