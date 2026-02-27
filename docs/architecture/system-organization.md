# System Organization & Architecture

**Goal**: Define the structural hierarchy and the "Live Architecture" represented by the Memory Graph.

## 1. Architectural Hierarchy

The Antigravity system follows a strict command-and-control hierarchy to ensure deterministic execution.

### Tier 0: Workflows (Orchestration - includes **75** workflows)
- **Location**: `.agent/workflows/`
- **Role**: The "SOP" (Standard Operating Procedure).
- **Function**: Defines the high-level steps of a process. It DOES NOT execute code directly; it orchestrates Agents.
- **Example**: `/research` workflow dictates *when* to check the catalog and *when* to search the web.

### Tier 1: Agents (Specialists - includes **10** agents)
- **Location**: Defined in `task.md` context or `.agent/agents/` (conceptual).
- **Role**: The "Persona".
- **Function**: Executes steps from a Workflow. An Agent is bound to specific Skills.
- **Example**: The `Knowledge Operations Specialist` is the only agent authorized to modify the Knowledge Graph.

### Tier 2: Skills (Capabilities - includes **198** skills)
- **Location**: `.agent/skills/`
- **Role**: The "Atomic Capability".
- **Function**: A specific, reusable procedure that an Agent performs.
- **Structure**:
    - **SKILL.md**: The instruction set (Prompt).
    - **Tools**: Bindings to MCP servers or Scripts.
- **Example**: `retrieving-rag-context` is a skill that uses the `antigravity-rag` MCP.

### Tier 3: Tools (Execution)
- **Components**:
    - **MCP Servers**: External services (Memory, RAG, FileSystem).
    - **Scripts**: Local Python scripts in `scripts/`.
- **Role**: The "Hands".
- **Function**: The actual code that performs the operation.
- **Example**: `mcp_antigravity-rag_search_library` or `scripts/validation/dependency_validator.py`.

## 2. The Memory Graph (Live Architecture)

The filesystem is the *static* representation of the architecture. The **Memory Graph** (managed by the `memory` MCP) is the *live* source of truth.

### Principles
1.  **Reflection**: Every architectural component (Workflow, Agent, Skill) must exist as an Entity in the Memory Graph.
2.  **Relation**: The graph must explicitly define the relationships (e.g., `Workflow --orchestrates--> Agent`, `Agent --uses--> Skill`).
3.  **Grounding**: Agents must query the Memory Graph to understand their authorized tools and authorized scope before acting.

### Dependency Graph
The Memory Graph acts as a high-level dependency graph.
- **Query**: "What skills are required for the `/research` workflow?"
- **Answer**: The graph traversal `Workflow -> Agent -> Skill` provides the authoritative answer.

## 3. Directory Structure Map

```text
antigravity-agent-factory/
├── .agent/
│   ├── workflows/       # Tier 0: Orchestration logic
│   ├── skills/          # Tier 2: Atomic capabilities
│   ├── rules/           # Governance: Enforces the hierarchy
│   └── knowledge/       # Evidence: Distilled truths (KIs)
├── docs/
│   └── architecture/    # Static documentation (this file)
└── scripts/             # Tier 3: Local execution logic
```

## 4. Traceability Rules

1.  **No Orphan Scripts**: Every script in `scripts/` MUST be used by at least one Skill or Workflow (or be a recognized maintenance utility).
2.  **No Orphan Skills**: Every Skill MUST be mappable to a Specialist Agent.
3.  **Explicit Bindings**: `SKILL.md` must list its `tools` (MCP or Script) in the frontmatter.
