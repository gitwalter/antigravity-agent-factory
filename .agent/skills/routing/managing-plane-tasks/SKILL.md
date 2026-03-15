---
name: managing-plane-tasks
description: 'Remote management of Plane PMS issues and states using the Plane MCP
  server, with formal task definition schema and memory MCP integration.

  '
type: skill
version: 3.0.0
category: routing
agents:
- python-ai-specialist
- ai-app-developer
- master-system-orchestrator
knowledge:
- plane-integration.json
- api-integration-patterns.json
tools:
- mcp_plane_list_project_issues
- mcp_plane_list_cycle_issues
- mcp_plane_list_module_issues
- mcp_plane_create_work_item
- mcp_plane_update_work_item
- mcp_plane_retrieve_work_item
- mcp_plane_list_labels
- mcp_plane_create_label
- mcp_plane_list_states
- mcp_plane_list_cycles
- mcp_plane_list_modules
- mcp_plane_get_me
- mcp_plane_create_work_item_comment
- mcp_plane_add_work_items_to_module
- mcp_plane_add_work_items_to_cycle
- mcp_plane_get_issue_using_readable_identifier
- mcp_plane_list_project_issues_with_filters
- mcp_plane_search_work_items (Verify availability - noted as missing in some instances)
- mcp_memory_read_graph
- mcp_memory_open_nodes
- mcp_memory_search_nodes
related_skills:
- orchestrating-mcp
- mastering-project-management
references:
- references/task_definition_schema.json
- references/task_definition_guide.md
- references/solution_definition_schema.json
templates:
- none
settings:
  auto_approve: false
  retry_limit: 3
  timeout_seconds: 300
  safe_to_parallelize: false
  orchestration_pattern: routing
---

# Remote Plane Management (MCP)

This skill enables agents to manage projects, issues, and states in a remote Plane PMS instance using the **Plane MCP server**. Every task created follows a **formal task definition schema** that links the work item to specific factory assets — workflows, agents, skills, scripts, knowledge, patterns, templates, blueprints, and tests.

> [!NOTE]
> Every task is a **hypothesis** about which factory assets best solve the defined problem. The schema formalizes context engineering — giving agents immediate, situation-adequate consciousness of available tools, techniques, and methodologies. See [Task Definition Guide](file:///d:/Users/wpoga/Documents/Python%20Scripts/antigravity-agent-factory/.agent/skills/routing/managing-plane-tasks/references/task_definition_guide.md) for the full philosophy.

## When to Use
- When you need to create, update, or track tasks in the hosted Plane instance.
- For all standard project lifecycle automation (refinement, updates, reporting).
- When a pure, standardized, and- **Automation**: Use `create_task.py` to maintain visual consistency across all issues, `list_cycles.py` to discover active sprint UUIDs, and `list_modules.py` / `list_labels.py` for context discovery.

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
  - Set `PLANE_WORKSPACE_SLUG` to `agent-factory`.
- **Memory MCP Server**: Must be active for knowledge graph queries during task planning.
- **Project Context**: Project ID `e71eb003-87d4-4b0c-a765-a044ac5affbe` | Identifier `AGENT`.
- **Label Governance**: Always use exactly one or more of these approved label strings in your JSON payload: `BUG`, `DATA`, `DOCU`, `FEATURE`, `GROUNDING`, `INFRA`, `INTEGRATION`, `ORCHESTRATION`, `SKILL`, `TEST`, `UI`. (The `create_task.py` script will automatically map these strings to their Plane UUIDs).

## Process

Follow this end-to-end workflow for all Plane project management operations.

### 1. Listing & Discovery
Choose the specific listing tool based on your needs. Note that **server-side filtering by status (state) is not supported**; you must fetch the issues and filter the JSON results locally.

#### A. List Active Cycle Issues (Preferred for Daily Work)
```json
// Tool: mcp_plane_list_cycle_issues
{
  "project_id": "e71eb003-87d4-4b0c-a765-a044ac5affbe",
  "cycle_id": "RESOLVED-CYCLE-UUID"
}
```

#### B. List all Project Issues (Backlog Exploration)
```json
// Tool: mcp_plane_list_project_issues
{
  "project_id": "e71eb003-87d4-4b0c-a765-a044ac5affbe"
}
```

#### C. Filtering by Status (Client-Side)
Since the API does not support a `state` filter in the list tools, follow this pattern:
1. Fetch issues using `mcp_plane_list_cycle_issues` (for daily work) or `mcp_plane_list_project_issues` (for backlog).
2. Iterate through the `results` array.
3. Check `item["state"]["id"]` or `item["state"]["name"]` against your target status.
4. Filter matching items locally.

#### D. Discovering Metadata (Scripts)
Use these scripts to find valid UUIDs for your task definition:
```bash
# List all labels
conda run -p D:\Anaconda\envs\cursor-factory python .agent/skills/routing/managing-plane-tasks/scripts/list_labels.py

# List all modules
conda run -p D:\Anaconda\envs\cursor-factory python .agent/skills/routing/managing-plane-tasks/scripts/list_modules.py
```

### 2. Detailed Inspection
Retrieve the full details of a specific item, including description and comments.

```json
// Tool: mcp_plane_retrieve_work_item
{
  "project_id": "e71eb003-87d4-4b0c-a765-a044ac5affbe",
  "work_item_id": "UUID-OR-IDENTIFIER"
}
```

### 3. Professional Task Creation (Mandatory Workflow)

A work item is **NOT considered created** until ALL mandatory steps (A through C) are complete. **No exceptions.**

> [!CAUTION]
> Creating a work item without start_date, target_date, estimate, labels, module, cycle, and task schema is a governance violation. Always complete the full workflow.

#### Step 0: Context Engineering (Memory-First Navigation)

**MANDATORY**: Before defining a task, query the memory MCP knowledge graph. This is the **Factory Standard** for building situational awareness. Establish the "Memory-First" pattern to ensure your task hypothesis is grounded in actual factory capabilities.

```json
// Tool: mcp_memory_open_nodes — Start with system orientation
{ "names": ["System_Consciousness"] }
```

Use this information to **form your hypothesis**: which workflows, agents, skills, scripts, knowledge, and patterns will best solve the problem?

#### Pre-Flight Checklist
Before calling `create_task.py`, resolve ALL of the following UUIDs via MCP:

| Property | How to Resolve | Required |
| :--- | :--- | :---: |
| `labels` | Select directly from the approved list above (e.g., `["FEATURE", "UI"]`). The Python script auto-resolves UUIDs. | ✅ |
| `start_date` / `target_date` | Determine accurate ISO 8601 dates (e.g., `"2026-03-03"`) | ✅ |
| `estimate_point` | Use Fibonacci scale UUID from [Estimate Points](#estimate-points-fibonacci-scale) | ✅ |
| `parent` | If item belongs to an Epic, use UUID from [Known Active Epics](#known-active-epics) | ⚠️ If applicable |
| `module_id` | Use UUID from [Known Active Modules](#known-active-modules) | ✅ |
| `cycle_id` | `mcp_plane_list_cycles` → find the currently active sprint | ✅ |

#### Step A: Generate and Create Task via Jinja Template
Create a `task.json` definition file on disk. Include the core requirements, factory assets (the task schema), AND the execution context.

> [!IMPORTANT]
> **Strict Asset Comprehensiveness Rule:** You MUST ALWAYS be absolutely comprehensive when filling out `workflows`, `agents`, `skills`, and `templates` in the `task.json`. Do not just include 1 or 2 skills if 5 are relevant. If a template is used, list it. The visual representation in Plane acts as the definitive routing map for agents, so it must be exhaustive.

> [!IMPORTANT]
> **Mandatory Epic Rule:** You MUST ALWAYS provide a `parent` (Epic) UUID. No task should ever be orphaned in the backlog without an Epic. If you do not know the Epic, scan existing tickets in the same domain to find the UUID.

> [!WARNING]
> **HTML Formatting Rule:** The `requirements` and `acceptance_criteria` fields in your JSON MUST be formatted as single, continuous HTML strings (e.g., `"<ul><li>Item 1</li></ul>"`), NOT JSON arrays of strings. Passing an array will cause the Jinja renderer to iterate character by character, creating unreadable 1-letter bullet points.

The execution context fields (`start_date`, `target_date`, `estimate_point`, `parent`) are sent directly to the Plane API so they appear natively in the UI.

**Example `task.json`:**
```json
{
  "name": "FEATURE: Implement Analyst Society",
  "type": "feature",
  "priority": "high",
  "labels": ["FEATURE", "CORE"],

  "start_date": "2026-03-03",
  "target_date": "2026-03-09",
  "estimate_point": "bd9e29aa-b4e8-4525-b16d-893c8324f7c7",
  "parent": "e18df34b-2da0-46a7-bca2-594ca70757c0",

  "requirements": "<ul><li>Must support nested loops</li></ul>",
  "acceptance_criteria": "<ul><li>Nested loops work to depth 3</li></ul>",
  "workflows": ["feature-development"],
  "agents": ["python-ai-specialist"],
  "skills": ["managing-plane-tasks"],
  "tests": [
    { "type": "unit", "script": "test_loops.py", "expected": "Pass" }
  ]
}
```

Run the creation script to render the HTML and apply the task natively:
```bash
conda run -p D:\Anaconda\envs\cursor-factory python .agent/skills/routing/managing-plane-tasks/scripts/create_task.py --json task.json
```
*Note: The script outputs the new `UUID` of the created task. You will need this for Steps B and C.*

#### Step B: Mandatory Module & Cycle Association

Use the `associate_task.py` script to assign the created task to its context module and cycle.

```bash
conda run -p D:\Anaconda\envs\cursor-factory python .agent/skills/routing/managing-plane-tasks/scripts/associate_task.py \
    --issue AGENT-126 \
    --module 4071283a-7135-4ef8-a61b-020cdef79a02 \
    --cycle RESOLVED-CYCLE-UUID
```

> [!TIP]
> Always use `list_cycles.py` to find the currently active sprint. Do not hardcode cycle UUIDs — they change every sprint.

```bash
conda run -p D:\Anaconda\envs\cursor-factory python .agent/skills/routing/managing-plane-tasks/scripts/list_cycles.py
```

#### Step C: Status Management

Transition issues through their lifecycle using `update_status.py`.

```bash
conda run -p D:\Anaconda\envs\cursor-factory python .agent/skills/routing/managing-plane-tasks/scripts/update_status.py \
    --issue AGENT-126 \
    --state "In Progress"
```

### 4. High-Fidelity Solution Reporting (Mandatory Closure)

Every issue marked as **Done** MUST be accompanied by a professional solution summary rendered via the `solution_comment.html.j2` template. This ensures technical fidelity and prevents shallow, uninformative closures.

**MANDATORY SCHEMA**: See [solution_definition_schema.json](file:///d:/Users/wpoga/Documents/Python%20Scripts/antigravity-agent-factory/.agent/skills/routing/managing-plane-tasks/references/solution_definition_schema.json).

#### Step D: Prepare High-Fidelity Solution Data
You must separate *what* you did (mechanics) from *why* you did it (architecture).

⚠️ **CRITERIA FOR A GOOD SOLUTION DEFINITION**
- **Poor (The "Alibi Blablabla")**: "Updated script. Fixed whitespace. Ran tests."
- **Excellent (Architectural Insight)**: "Introduced a `post_solution.py` script bridging the Plane API with Jinja2 rendering. Decided to filter empty whitespace natively inside the Jinja template using `-set` blocks to offload cleaning logic from Python, ensuring clean HTML payloads."

**Example `solution.json` (Working Reference):**
```json
{
  "summary": "Resolved the 3 critical failures identified in the previous system audit and modernized Plane compliance.",
  "architectural_decisions": [
    "Adopted dictionary-based pattern storage to align with system-structure schema validation requirements.",
    "Shifted from array-based to key-value pairs for O(1) lookups and explicit metadata mapping.",
    "Standardized Task Schema usage for all Plane issues to ensure machine-readable context engineering."
  ],
  "files_affected": [
    ".agent/knowledge/hierarchical-memory-patterns.json",
    ".agent/knowledge/atomic-skill-patterns.json",
    ".agent/patterns/practices/reflection-gate.json",
    ".agent/patterns/practices/multi-agent-debate.json",
    ".agent/workflows/bugfix-resolution.md",
    ".agent/workflows/feature-development.md",
    ".agent/workflows/agent-development.md"
  ],
  "verification": [
    {
      "type": "unit",
      "result": "PASS",
      "details": "72 passed, 0 failed in 61s"
    }
  ],
  "evolution": [
    "Modernized core workflows with mandatory Plane/Jinja2 reporting gates.",
    "Standardized knowledge patterns as dictionary-based structures.",
    "Established high-fidelity reporting mandates for all factory tasks."
  ],
  "notes": "Continued work on AGENT-123 (Modular Agent Architecture & Coordination Framework) to complete the persona-specialist harmonization."
}
```

> [!CAUTION]
> The `post_solution.py` script contains strict minimum-length validations. If your descriptions are too short or lack architectural depth, the script will crash and block the task closure. Provide extreme technical depth.

#### Step E: Render and Post Solution
Use the `post_solution.py` script to automate the rendering and posting to Plane. This script also moves the issue to the **Done** state.

```bash
conda run -p D:\Anaconda\envs\cursor-factory python .agent/skills/routing/managing-plane-tasks/scripts/post_solution.py \
    --issue AGENT-48 \
    --json solution.json \
    --close
```

## Best Practices
- **Cycle-First Navigation**: ALWAYS use `mcp_plane_list_cycle_issues` for daily status checks. Only use `mcp_plane_list_project_issues` for cross-cycle backlog grooming.
- **Memory-First**: Always query memory MCP (Step 0) before creating tasks to build situational awareness.
- **Hypothesis-Driven**: Treat each task as a hypothesis — declare which assets solve the problem, then validate with tests.
- **Always resolve metadata first**: Use `mcp_plane_list_labels`, `mcp_plane_list_states`, `mcp_plane_get_me` before creating work items.
- **Complete all five steps**: A work item is not finished until Steps A–E are complete (creation, module, cycle, epic, schema, and solution reporting).
- **Use expand for context**: When listing or retrieving items, use `expand: "labels,state,assignees"` for full metadata.
- **Never hardcode cycle UUIDs**: Always query `mcp_plane_list_cycles` — cycles change every sprint.
- **Document closures professionally**: Use `post_solution.py` to provide a technical summary, files affected, and verification proof.
- **Respect formal identifiers**: Use the project's formal prefix (e.g., `AGENT-XX`) even if scripts allow numeric resolution.
- **Respect label governance**: Only use labels from the synchronized set.
- **Create missing assets**: If a task needs a skill, agent, or workflow that doesn't exist, use the `[NEW]` prefix and build it during execution.
- **Evolve the knowledge graph**: After completing tasks, update both knowledge files and memory MCP entities with learnings.

---
*Context engineering is the foundation of intelligent agency. Every task refines the system's consciousness.*
