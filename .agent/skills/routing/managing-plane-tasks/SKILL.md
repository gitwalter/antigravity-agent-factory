---
name: managing-plane-tasks
description: 'High-performance management of Plane PMS using specialized scripts, persistent context, Jinja2 templates, and memory MCP integration.

  '
type: skill
version: 4.0.0
category: routing
agents:
- python-ai-specialist
- ai-app-developer
- master-system-orchestrator
knowledge:
- plane-integration.json
- api-integration-patterns.json
scripts:
- scripts/sync_project_context.py
- scripts/create_task.py
- scripts/associate_task.py
- scripts/update_status.py
- scripts/list_cycles.py
- scripts/list_modules.py
- scripts/list_labels.py
- scripts/post_solution.py
tools:
- mcp_plane_retrieve_work_item
- mcp_memory_read_graph
- mcp_memory_open_nodes
- mcp_memory_search_nodes
related_skills:
- orchestrating-mcp
- mastering-project-management
references:
- references/project_context.json
- references/task_definition_schema.json
- references/task_definition_guide.md
- references/solution_definition_schema.json
templates:
- templates/work_item.html.j2
- templates/solution_comment.html.j2
settings:
  auto_approve: false
  retry_limit: 3
  timeout_seconds: 300
  safe_to_parallelize: false
  orchestration_pattern: routing
---

# Script-First Plane Management

This skill enables high-performance management of Plane projects and issues using **specialized Python scripts** that utilize a **persistent context layer** and **Jinja2 templates**.

> [!IMPORTANT]
> **Priority Directive**: ALWAYS prioritize using the provided **scripts** over raw MCP tools. Every creation and update MUST be performed via Jinja2 templates to ensure visual consistency and technical fidelity. Raw MCP updates for issue descriptions are forbidden except in emergency discovery scenarios.

This skill enables agents to manage projects, issues, and states in a remote Plane PMS instance using the **Plane MCP server**. Every task created follows a **formal task definition schema** that links the work item to specific factory assets — workflows, agents, skills, scripts, knowledge, patterns, templates, blueprints, and tests.

> [!NOTE]
> Every task is a **hypothesis** about which factory assets best solve the defined problem. The schema formalizes context engineering — giving agents immediate, situation-adequate consciousness of available tools, techniques, and methodologies. See [Task Definition Guide](file:///.agent/skills/routing/managing-plane-tasks/references/task_definition_guide.md) for the full philosophy.

## When to Use
- When you need to create, update, or track tasks in the hosted Plane instance.
- For all standard project lifecycle automation (refinement, updates, reporting).
- When you need professional, Jinja2-rendered issue documentation.
- **Automation**: Use `create_task.py` to maintain visual consistency across all issues, `list_cycles.py` to discover active sprint UUIDs, and `list_modules.py` / `list_labels.py` for context discovery.

## Project State Mapping (UUIDs)

| State | UUID |
| :--- | :--- |
| **Backlog** | `294ddb00-19ce-4ffe-9eac-2fd4e998d7f8` |
| **Todo** | `8e155185-58ad-404b-8458-6a7c9edbf09b` |
| **In Progress** | `d89aabd2-46d4-4f46-8ce4-eb49e06cac03` |
| **Done** | `ef4b2395-3edb-41e9-adcd-7ec77d534f0f` |
| **Cancelled** | `0723fa1c-6935-4661-a873-f5295203e58c` |

## Prerequisites
- **Plane MCP Server**: Must be active and configured in `mcp_config.json`.
  - Use `${env:PLANE_API_TOKEN}` for the API token.
- **Memory MCP Server**: Must be active for knowledge graph queries during task planning.
- **Conda Environment**: All scripts must run in `conda run -p D:\Anaconda\envs\cursor-factory`.

## Process

Follow this script-first workflow for all Plane project management operations.

### 0. Context Synchronization (Persistent Layer)
Before starting any significant work, sync your local project context to ensure you have the latest UUIDs for cycles, modules, and labels.

```bash
conda run -p D:\Anaconda\envs\cursor-factory python .agent/skills/routing/managing-plane-tasks/scripts/sync_project_context.py
```
This script updates `references/project_context.json`, which is used by all other scripts to avoid redundant API discovery.

### 1. Listing & Discovery (Script-Based)
Use the utility scripts to explore the project state. These scripts are faster and more informative than raw MCP tools.

#### A. List Active & Upcoming Cycles
```bash
conda run -p D:\Anaconda\envs\cursor-factory python .agent/skills/routing/managing-plane-tasks/scripts/list_cycles.py
```

#### B. List Modules (Epics & Feature Areas)
```bash
conda run -p D:\Anaconda\envs\cursor-factory python .agent/skills/routing/managing-plane-tasks/scripts/list_modules.py
```

#### C. List Labels
```bash
conda run -p D:\Anaconda\envs\cursor-factory python .agent/skills/routing/managing-plane-tasks/scripts/list_labels.py
```

### 2. Detailed Inspection (MCP Fallback)
If you need the full description or comments of a specific issue, use the MCP tool (Discovery only).

```json
// Tool: mcp_plane_retrieve_work_item
{
  "project_id": "RESOLVED-FROM-CONTEXT",
  "work_item_id": "AGENT-XX"
}
```

### 3. Professional Task Creation (Jinja Enforcement)

Work item creation is strictly regulated. **Direct MCP creation is forbidden.** All tasks must be created via **`create_task.py`** to ensure they adhere to the Jinja2 visual standard and technical schema.

> [!CAUTION]
> Creating a work item without the Jinja-rendered `task.json` structure is a governance violation.

#### Pre-Flight Checklist
Ensure you have run `sync_project_context.py` recently. The scripts will automatically use the resolved UUIDs from `references/project_context.json`.

#### Step A: Generate and Create Task via Jinja Template
Create a `task.json` file. The scripts will handle mapping labels and states from context.

```bash
conda run -p D:\Anaconda\envs\cursor-factory python .agent/skills/routing/managing-plane-tasks/scripts/create_task.py --json task_input.json
```

#### Step B: Associate Module & Cycle
Use `associate_task.py`. You can find active UUIDs via `list_cycles.py` or the context file.

```bash
conda run -p D:\Anaconda\envs\cursor-factory python .agent/skills/routing/managing-plane-tasks/scripts/associate_task.py \
    --issue AGENT-XX \
    --module UUID \
    --cycle UUID
```

#### Step C: Transition Status
Use `update_status.py`.

```bash
conda run -p D:\Anaconda\envs\cursor-factory python .agent/skills/routing/managing-plane-tasks/scripts/update_status.py \
    --issue AGENT-XX \
    --state "In Progress"
```

### 4. High-Fidelity Solution Reporting (Mandatory Closure)

Every issue marked as **Done** MUST be accompanied by a professional solution summary rendered via the `solution_comment.html.j2` template. This ensures technical fidelity and prevents shallow, uninformative closures.

#### Step D: Prepare Solution Data
Follow [solution_definition_schema.json](file:///.agent/skills/routing/managing-plane-tasks/references/solution_definition_schema.json).

#### Step E: Render and Post Solution
Use the `post_solution.py` script. This script also moves the issue to the **Done** state if `--close` is provided.

```bash
conda run -p D:\Anaconda\envs\cursor-factory python .agent/skills/routing/managing-plane-tasks/scripts/post_solution.py \
    --issue AGENT-XX \
    --json solution.json \
    --close
```

## Best Practices
- **Script-First**: ALWAYS use `sync_project_context.py` before work and specialized scripts for all mutations.
- **Jinja-Only**: NEVER update issue descriptions manually or via raw MCP tools. Use `create_task.py` and `post_solution.py`.
- **Context Reuse**: Leverage the UUIDs in `references/project_context.json` to minimize API latency.
- **Hypothesis-Driven**: Treat each task as a hypothesis — declare which assets solve the problem, then validate with tests.
- **High-Fidelity Closure**: A task is only **Done** when `post_solution.py` has rendered the architectural decisions and verification proof.
- **Cycle-Awareness**: Use `list_cycles.py` to ensure you are working on the currently active sprint items.
- **Evolve the knowledge graph**: After completing tasks, update both knowledge files and memory MCP entities with learnings.

---
*Context engineering is the foundation of intelligent agency. Every task refines the system's consciousness.*
