---
title: Memory-First Orientation
scope: all agents, all tasks
axioms: [A1, A3, A5]
priority: P0
---

# Memory-First Orientation Protocol

**This is a P0 rule. It applies to EVERY task before any action is taken.**

## The Rule

Before executing any non-trivial action, query Memory MCP for relevant context:

```
mcp_memory_search_nodes(query="<topic keywords>")
```

## When to Query (Mandatory)

| Trigger | Query | Why |
|---------|-------|-----|
| **Before running a script** | `<script_name> commands` | Get current syntax (may have changed) |
| **Starting maintenance** | `Self_Optimization` | Know which tools exist |
| **Working with RAG** | `RAG` | Get library info, commands, skills |
| **Creating knowledge/skills** | `<topic>` | Avoid duplicates |
| **Working with Plane PMS** | `PMS` | Get correct CLI syntax |
| **Unsure which rule applies** | `Rules_Index` | Find the right rule |

## Key Entities Available

- `RAG_Library` — system component info
- `RAG_CLI_Commands` — exact CLI syntax for rag_cli.py
- `System_Self_Optimization` — 76 maintenance scripts by OODA phase
- `Agent_Rules_Index` — quick rule orientation

## Convention Reminder

| Layer | Responsibility | Update Trigger |
|-------|---------------|----------------|
| **Skill** | WHAT to do, WHEN | Purpose/intent changes |
| **Memory MCP** | HOW (exact syntax) | Script CLI changes → run `sync_script_registry.py` |
| **Knowledge** | WHY (context) | Research/learning |

## Why This Matters

Memory MCP queries take <100ms. Reading a file takes >500ms. Stale syntax causes failures.
**Memory MCP is the fast path to correct action.**
