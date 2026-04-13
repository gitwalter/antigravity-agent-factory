# Rule: Memory & RAG Usage

## Context
Governs how agents interact with the Automated Cognitive Memory system (Qdrant) and the graph-based Relational memory, specifically during cooperative vector searches with the operator.

## Requirements
- **Cooperative Vector Search**: When the operator asks questions like "what is in our memory_summary?", "what do we know about X?", or requests a vector search, you MUST use the correct granular tool provided by the custom `rag` MCP server (`search_memory_summary`, `search_memory_semantic`, `search_memory_procedural`, `search_memory_entity`).
- **Context Preparation**: Before starting complex system designs or bug fixes, you MUST use the `prepare_context` tool to query all three primary cognitive schemas (Semantic, Procedural, Entity) simultaneously.
- **Active Learning Loop**: Every time you identify a new architectural rule, solve a complex bug, or verify a new procedural pattern, you MUST use the `propose_memory` tool to ship a draft of that insight into the SSGM `pending` tier for the operator to approve.
- **Do not bypass the MCP**: Under no circumstances should you write raw Python scripts (e.g., `python -c ...`) to query Qdrant if an MCP server tool is intended. Always prioritize the available MCP wrapper.
- **Fallback**: If the `rag` MCP server is not currently mapping its tools into your context window, you must inform the operator that the MCP Server is disconnected or needs to be registered in `settings.json`, and invoke `memory_cli.py` strictly as a fallback.

## Lifecycle
- **Trigger**: Operator queries the memory database natively, or a workflow explicitly requires `prepare_context`.
- **Action**: Invoke the correct function, e.g., `search_memory_summary(query="")`.
- **Completion**: At the completion of an implementation phase, ALWAYS use `propose_memory(content="[New Knowledge Draft]")`.
- **Presentation**: Extract the `id`, `content`, and `metadata` from the results and present them cleanly to the user.
