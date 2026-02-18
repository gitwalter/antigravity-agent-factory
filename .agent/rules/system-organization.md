# Rule: System Organization & Hierarchy

## Context
Enforces the structural integrity of the Antigravity architecture and the authority of the Memory Graph.

## 1. Hierarchy Enforcement
- **Workflows (Tier 0)**:
    - MUST NOT call scripts directly (unless marked `// turbo` for simple ops).
    - MUST delegate complex tasks to Agents/Skills.
- **Agents (Tier 1)**:
    - MUST operate within their defined "Authorized Tools" (see Memory Graph).
- **Skills (Tier 2)**:
    - MUST explicitly declare their `tools` in YAML frontmatter.
    - MUST NOT depend on other Skills (no circular dependencies); use Workflows to chain Skills.
- **Tools (Tier 3)**:
    - Scripts MUST be located in `scripts/` and organized by domain (e.g., `scripts/ai/rag/`).

## 2. Memory Graph Authority
- **Reflection**: Any modification to the system architecture (adding a Workflow, Agent, or Skill) MUST be reflected in the Memory Graph.
- **Verification**: Before using a new tool or skill, verify its status in the Memory Graph (conceptually).
- **Grounding**: Decisions on "who does what" are derived from the Memory Graph relations (`orchestrates`, `utilizes`, `governed_by`).

## 3. Traceability
- **Script Usage**: Ideally, all functional code resides in `scripts/` or MCP servers.
- **Orphan Check**: Do not create scripts that are not bound to a Skill or Workflow.
- **Link Integrity**: `SKILL.md` files must point to EXISTING scripts or MCP tools.

## 4. MCP vs. Script (The "Local-First" Axiom Exception)
- While "Local-First" prefers `git/gh` over MCP, for **Core Cognitive Functions** (Memory, RAG), the MCP is the **Primary** interface.
- **RAG**: ALWAYS use `antigravity-rag` MCP. Do not use local `pdf_ingest.py` scripts unless debugging the MCP itself.
- **Memory**: ALWAYS use `memory` MCP. Do not directly edit the graph database files.
