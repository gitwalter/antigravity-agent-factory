# Rule: Integrative Memory Retrieval

## Context
Governs how agents utilize the Automated Cognitive Memory system to retrieve previous state, entity linkages, and procedural workflows dynamically during live execution.

## Requirements
- **Situation A (Task Initiation)**: Before bootstrapping an implementation plan or starting a major task, the agent MUST query `search_memory` using `collection: memory_procedural` and `collection: memory_summary` to retrieve related past attempts and valid skills.
- **Situation B (Error Resolution)**: When encountering unexpected behavior or stack traces, agents MUST query `search_memory` in `memory_semantic` to check if a known resolution exists before falling back to generic web search.
- **Situation C (Tool & MCP Usage Continuity)**: Any usage of external state-changing MCP tools (e.g., `mcp_plane_create_issue`, Terraform deployments) constitutes a major state change. Agents should log these semantic markers into memory.

## Protocol
- **search_memory** tool is the primary gateway to `SQL/tool_logs` and `Qdrant` stores. Use the specific `collection` type to narrow down search relevance (e.g., `memory_toolbox` for capabilities, `memory_entity` for known entities/people/systems).
- Never assume knowledge is static; fetch latest procedural guidelines immediately.
