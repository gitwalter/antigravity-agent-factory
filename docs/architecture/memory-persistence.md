# Memory Persistence & Portability

**Q: Is the memory system exportable to GitHub?**
**A: YES.**

## The Hybrid Architecture

We use a **"Git-Backed, Graph-Indexed"** architecture to ensure both portability and speed.

### 1. The Source of Truth (Portable)
- **Location**: `.agent/knowledge/*.json` (and `SKILL.md`, `workflow.md` files).
- **Format**: Standard JSON/Markdown.
- **Role**: These files are the **Permanent Memory**. They are committed to GitHub.
- **Portability**: If you clone the repo on a new machine, you have 100% of the knowledge.

### 2. The Memory Graph (Local Index)
- **Location**: Local Database (managed by `memory` MCP).
- **Role**: This is the **Active Consciousness**. It indexes the JSON files for millisecond-speed lookups and relationship traversal.
- **Ephemeral**: If the local database is deleted, it can be **"Hydrated"** (rebuilt) completely from the JSON files in `.agent/knowledge`.

## Workflow for Portability

1.  **Commit**: Always commit changes to `.agent/knowledge/`.
2.  **Clone**: Pull the repo on a new machine.
3.  **Hydrate**: The system (or an onboarding script) reads `.agent/knowledge/*.json` and re-injects them into the local Memory Graph.

## Key Artifacts
- `workflow-catalog.json`
- `skill-catalog.json`
- `agent-team-registry.json`
- `pattern-catalog.json`

These files effectively "freeze" the system's understanding into code that version control can manage.
