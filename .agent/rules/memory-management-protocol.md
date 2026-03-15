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

## 2. Deterministic Identifiers (The Prefix System)
To eliminate failed reads and "useless access", all nodes in the Memory MCP MUST use strict prefixes. Agents MUST use `mcp_memory_open_nodes` for these identifiers instead of broad keyword searches.

| Entity Type | Prefix | Example |
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
3.  **Discovery**: Use `mcp_memory_add_observations` immediately upon discovering new syntax or relationships.
4.  **Induction**: Upon task completion, synthesize learnings into a `KI:` node.

## 5. Proactive Memory Creation
If a query for a specific configuration or entity returns no results:
1. **Do NOT guess or hallucinate.**
2. **Collect**: Ask the user for missing context/parameters.
3. **Verify**: Confirm understanding with the user.
4. **Create**: Use `mcp_memory_create_entities` to persist the new knowledge.

## 6. Relation Governance
- `[SOP] --requires--> [SKILL]`
- `[AGENT] --orchestrates--> [SOP]`
- `[TASK] --implements--> [SOP]`
- `[TASK] --learned_from--> [KI]`

## 7. Failure Protocol
If a deterministic identifier read fails:
1. Search local file system (`.agent/workflows/`, `.agent/knowledge/`).
2. Register the missing node in Memory MCP immediately.
3. Proceed and flag the discrepancy for `repository-maintenance`.

## 8. Convention Reminder
| Layer | Responsibility | Update Trigger |
| :--- | :--- | :--- |
| **Skill** | WHAT to do, WHEN | Purpose/intent changes |
| **Memory MCP** | HOW (exact syntax) | Script CLI changes |
| **Knowledge** | WHY (context) | Research/learning |
