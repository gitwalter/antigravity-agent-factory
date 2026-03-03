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

---

## Consent-Driven Workflow Integration (AGENT-50)

To ensure this Memory Graph is actively used and carefully curated, the factory strictly enforces a Consent-Driven Workflow loop across all structural agents (`feature-development`, `bugfix-resolution`, `research`).

### Phase 0: Context Engineering & Active Memory Building
Before an agent begins deep-diving into code or initiating broad web searches, they **MUST** query the Tier 0 Active Consciousness.
- **Action**: Use `mcp_memory_search_nodes` (via the `managing-memory-bank` skill).
- **Goal**: Establish the structural topography. Understand existing architectural rules and relations to prevent duplicating work or violating established Layer 3/4 methodologies.
- **Zero-Context Fallback**: If the memory graph returns no results for a domain (or if the existing information is clearly outdated), the agent MUST NOT invent context. The agent MUST actively "build the memory" by suspending the task and directly asking the human operator (`notify_user`). The agent then takes the human's verbatim answers, verifies they don't break Axioms 0-2, and proposes them as new Tier 1 Semantic Memory. Outdated nodes discovered during this process must be explicitly flagged for deletion or overwriting.

### Phase Final: Memory Induction & Consent
At the conclusion of a workflow, agents must analyze their Tier 3 Episodic session data for "Significant Patterns" (new structural rules, recurring logic, architectural definitions).
- **Action**: Propose the pattern to the human operator using the `architectural_decisions` array during a Plane Task Closure (`managing-plane-tasks`).
- **Goal**: This acts as a Tier 4 Memory Proposal. If the user approves the Pull Request/Task Closure, the knowledge is permanently written to the Tier 1 `.json` layer and Hydrated back into Tier 0. **The factory mathematically requires this Human-In-The-Loop gate to evolve its permanent memory.**
