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

## 4. Grounding & Memory
- **Add Observations**: Proactively add key decisions and architectural shifts to the Memory graph.
- **Read First**: Always perform `mcp_memory_read_graph` or key entity lookup before starting sub-tasks.
