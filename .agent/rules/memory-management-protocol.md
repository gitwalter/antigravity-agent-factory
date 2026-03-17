# Rule: Memory Management Protocol (MMP)

## Purpose
Establishes a systematic, deterministic, and performance-enhancing protocol for all Memory MCP interactions within the Antigravity Agent Factory. This represents the **Memory-First Orientation** required for all non-trivial tasks.

## 1. The Memory-First Protocol (Mandatory Orientation)
Before executing any non-trivial action, agents MUST query the Memory MCP for context. Memory queries take <100ms, whereas file lookups take >500ms. **Memory is the fast path to correct action.**

### When to Query
| Trigger | Query | Why |
| :--- | :--- | :--- |
| **Before running a script** | `<script_name> commands` | Get current syntax (may have changed) |
| **Starting maintenance** | `Self_Optimization` | Know which tools exist |
| **Selecting a workflow** | `workflow` or `<task_intent> workflow` | Find the correct orchestration path |
| **Discovering capabilities** | `catalog` or `Human_Readable_Catalog` | Read `docs/reference/catalog.md` for assets |
| **Creating knowledge/skills** | `<topic>` | Avoid duplicates |
| **Unsure which rule applies** | `Rules_Index` | Find the right rule |

## 2. Deterministic Identifiers & Search Strategy
To eliminate failed reads and "useless access", agents MUST adopt a **Search-then-Open** strategy:
1. **Search First**: Use `mcp_memory_search_nodes` with broad keywords (e.g., "plane task creation", "rag cli").
2. **Deterministic Open**: Once candidates are found, use `mcp_memory_open_nodes` for the exact identifiers using the prefix system.

| Entity Type | Prefix | Range |
| :--- | :--- | :--- |
| **Workflow (SOP)** | `SOP:` | `SOP:Feature-Development` |
| **Agent Persona** | `AGENT:` | `AGENT:Architect` |
| **Tactical Skill** | `SKILL:` | `SKILL:Managing-Plane-Tasks` |
| **Knowledge Item** | `KI:` | `KI:Memory-Patterns` |
| **Active Task** | `TASK:` | `TASK:AGENT-136` |
| **System Root** | `SYS:` | `SYS:Consciousness` |

## 3. Tri-Tier Organization
Memory is organized by volatility and scope:
- **Tier 0: Core (Static)**: Axioms, Rules, Root Catalogs. (Permanent)
- **Tier 1: Capability (Evolving)**: Workflow SOPs, Specialist definitions, Skill details. (Long-term)
- **Tier 2: Operational State (Transient)**: Active Plane tasks, session-specific observations. (Ephemeral)

## 4. The Memory execution loop
Every workflow MUST adhere to these memory hooks:
1.  **Orientation**: Call `mcp_memory_open_nodes` using `TASK:[IssueKey]` and `SOP:[CurrentWorkflow]` at the start of every phase.
2.  **Registration**: Update `TASK` node observations with current intent upon entering a new phase.
3.  **Discovery**: Use `mcp_memory_add_observations` immediately upon discovering new syntax, relationships, or missing deterministic nodes.
4.  **Save-on-Discover**: If a search/open call fails but the asset is found in the filesystem, the agent **MUST** immediately call `mcp_memory_create_entities`.
    - **Requirement**: Observations MUST include: `Path`, `Description`, `Goal`, and `Keywords`.
5.  **Induction**: Upon task completion, synthesize learnings into a `KI:` node and link it to the `TASK:`.

## 5. Proactive Memory Creation
If a query for a specific configuration or entity returns no results:
1. **Do NOT guess or hallucinate.**
2. **Search filesystem**: Check `.agent/workflows/`, `.agent/skills/`, or `scripts/`.
3. **Save-on-Discover**: If found, register the node using the correct prefix (`SOP:`, `SKILL:`, `AGENT:`, `KI:`, `TASK:`, `SYS:`).
4. **Collect**: If NOT found, ask the user for missing context/parameters.
5. **Verify**: Confirm understanding with the user.
6. **Create**: Use `mcp_memory_create_entities` to persist the new knowledge.

## 6. Relation Governance
- `[SOP] --requires--> [SKILL]`
- `[AGENT] --orchestrates--> [SOP]`
- `[TASK] --implements--> [SOP]`
- `[TASK] --learned_from--> [KI]`

## 7. Failure Protocol
If a deterministic identifier read fails:
1. **Discover**: Search local file system (`.agent/workflows/`, `.agent/knowledge/`, `scripts/`).
2. **Register**: Register the missing node in Memory MCP immediately using the prefix system.
3. **Verify**: Ensure the node is accessible via `mcp_memory_open_nodes`.
4. **Proceed**: Flag any complex discrepancies for `repository-maintenance`.

## 8. Convention Reminder
| Layer | Responsibility | Update Trigger |
| :--- | :--- | :--- |
| **Skill** | WHAT to do, WHEN | Purpose/intent changes |
| **Memory MCP** | HOW (exact syntax) | Script CLI changes |
| **Knowledge** | WHY (context) | Research/learning |
