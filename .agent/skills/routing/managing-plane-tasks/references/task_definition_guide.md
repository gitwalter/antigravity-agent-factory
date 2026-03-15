# Task Definition Guide — Antigravity Agent Factory

> *Every task is a hypothesis. Every completion is evidence. Every factory asset created is evolution.*

## Philosophy

Defining a task in the agent-factory is an act of **context engineering**. When you create a Plane issue and populate its schema fields, you are:

1. **Forming a hypothesis** about which factory assets (workflows, agents, skills, scripts, knowledge, patterns, templates, blueprints) are best suited to solve the problem.
2. **Engineering context** so that agents executing the task have immediate, situation-adequate consciousness of the tools, techniques, and methodologies available.
3. **Creating a feedback loop** — completed tasks become evidence of what works, improving future task definitions and growing the factory's capabilities.

### The Two Modes of Asset Reference

Every asset field supports two modes:

| Mode | Syntax | Meaning |
|:---|:---|:---|
| **Existing** | `"managing-plane-tasks"` | Use an asset that already exists in the factory |
| **New** | `"[NEW] task-schema-validation"` | Create this asset as a deliverable of the task |

When a task requires a capability the factory doesn't yet possess, you **declare the gap** and **build the specialist** during execution. This turns every task into a potential factory evolution event.

---

## The Knowledge Layer: Memory MCP ↔ Knowledge Files

The knowledge layer has two synchronized representations:

| Source | Location | Purpose |
|:---|:---|:---|
| **Knowledge Files** | `.agent/knowledge/*.json` | Persisted evidence layer — schemas, patterns, best practices |
| **Memory MCP Graph** | `mcp_memory_*` tools | Live operational index — fast entity lookup, relationships, observations |

**These MUST be kept in sync.** The memory graph is the fast-access consciousness; the knowledge files are the durable ground truth. When you add knowledge to one, update the other.

### Key Memory MCP Entities for Task Planning

| Entity | What it provides |
|:---|:---|
| `System_Consciousness` | Bridge to all catalogs — query this first for orientation |
| `Skill Catalog` | Index of all ~190 skills with locations and metadata |
| `Agent Team Registry` | All agents with capabilities, DIDs, and protocols |
| `Pattern Catalog` | All patterns in `.agent/patterns/` |
| `Template Catalog` | All templates in `.agent/templates/` |
| `Blueprint Catalog` | All blueprints in `.agent/blueprints/` |
| `Agent_Rules_Index` | All agent rules in `.agent/rules/` |
| `Workflows (SOPs)` | Operational workflows in `.agent/workflows/` |

**Before creating any task**, query these entities to discover which assets are available and relevant.

---

## Estimate Points (Fibonacci Scale)

The project uses Fibonacci-based estimation. No MCP tool exists to list estimate point UUIDs — they must be referenced from this table.

| Fibonacci Points | UUID (`estimate_point`) |
|:---|:---|
| 1 | `a1f66f54-0f4b-4ca1-9979-a34087b4594a` |
| 2 | *(verify in Plane UI and update)* |
| 3 | `3b88eecb-e4ad-4d67-b557-adbeb97e590d` *(needs verification)* |
| 5 | `bd9e29aa-b4e8-4525-b16d-893c8324f7c7` |
| 8 | `8399793b-12e0-4d3d-9d9c-3cb43c1a51b4` *(needs verification)* |
| 13 | *(verify in Plane UI and update)* |
| 21 | *(verify in Plane UI and update)* |

> **NOTE**: There is no `mcp_plane_list_estimate_points` or equivalent tool. UUIDs were discovered by inspecting existing work items. Verify and complete this table from the Plane UI.

---

## Known Active Epics

Epics are parent work items that group related tasks. Set the `parent` field to the epic UUID.

| Epic Name | UUID (`parent` field) |
|:---|:---|
| **Agent System** | `e18df34b-2da0-46a7-bca2-594ca70757c0` |
| **Statistical Dashboard** | `600ac6d6-fc68-45a2-b207-322f6dfe70aa` |
| **RAG System** | `867a5341-0b55-4862-9b01-bee535bf29ed` |

---

## Complete Task Example

Here is AGENT-31 itself, expressed as a schema-compliant task definition:

```json
{
  "schema_version": "1.0.0",
  "requirements": "Define a formal, machine-readable schema for every Plane work item...",
  "acceptance_criteria": "1. JSON Schema file exists 2. SKILL.md updated 3. Guide created...",
  "workflows": [
    "feature-development",
    "code-review"
  ],
  "agents": [
    "master-system-orchestrator",
    "python-ai-specialist"
  ],
  "skills": [
    "managing-plane-tasks",
    "mastering-project-management",
    "orchestrating-mcp"
  ],
  "scripts": [
    "scripts/validation/sync_manifest_versions.py",
    "scripts/maintenance/sync/sync_script_registry.py"
  ],
  "knowledge": [
    { "name": "plane-integration.json", "source": "knowledge_file" },
    { "name": "api-integration-patterns.json", "source": "knowledge_file" },
    { "name": "System_Consciousness", "source": "memory_mcp" }
  ],

  "patterns": [
    "json-schema-validation"
  ],
  "templates": [],
  "blueprints": [],
  "tests": [
    {
      "type": "unit",
      "script": "tests/test_task_schema.py",
      "command": "conda run -p D:\\Anaconda\\envs\\cursor-factory python -m pytest tests/test_task_schema.py -v",
      "expected": "Schema validates correctly against sample tasks"
    },
    {
      "type": "manual",
      "expected": "Create a Plane task using the schema and verify it renders correctly"
    }
  ],
  "rules": [
    "workflow-execution.md",
    "memory-first.md",
    "knowledge-management.md"
  ],
  "memory_queries": [
    "System_Consciousness",
    "Skill Catalog",
    "Agent Team Registry",
    "Agent_Rules_Index"
  ]
}
```

---

## Task Creation Workflow (with Schema)

1. **Query Memory MCP** — `mcp_memory_open_nodes(["System_Consciousness"])` for orientation
2. **Form Hypothesis** — Select workflows, agents, skills, scripts, knowledge based on problem analysis
3. **Check for Gaps** — If a needed asset doesn't exist, mark it `[NEW]` — it becomes a deliverable
4. **Create the Issue** — Follow SKILL.md Steps A–E with all mandatory metadata. Use `mcp_plane_list_project_issues` to verify creation (note: filtering by status is client-side).
5. **Embed Schema** — Include the task schema JSON in the description under `## Task Schema`
6. **Execute** — Agents use the schema fields as their context — workflows guide process, skills provide tactics, knowledge provides evidence
7. **Validate** — Run the declared tests to confirm or refute the hypothesis
8. **Evolve** — Update memory MCP and knowledge files with learnings from completed tasks
