---
description: Central governance rules for creating and managing Plane PMS tasks.
tags: [rules, plane, pms, task-definition]
---

# Plane Task Governance Rules

**CRITICAL MANDATE:** ALL agents, across ALL phases, MUST adhere strictly to the `task_definition_schema.json` when creating or modifying work items in the Plane PMS.

## 1. Schema Supremacy
You must NEVER create a Plane ticket that lacks the required schema fields. The definition MUST always include:
- `schema_version`
- `requirements`
- `acceptance_criteria`
- `workflows` (Array referencing `.agent/workflows/` or `[NEW]`)
- `agents` (Array referencing `.agent/agents/` or `[NEW]`)
- `skills` (Array referencing `.agent/skills/` or `[NEW]`)
- `scripts` (Array referencing `scripts/` or `[NEW]`)
- `knowledge` (Array defining `.agent/knowledge/` and Memory MCP bounds)
- `tests` (Array with structured test parameters)

**Reference Schema**: `.agent/skills/routing/managing-plane-tasks/references/task_definition_schema.json`

## 2. Authorized Tools Only
Agents MUST NOT bypass the authorized creation path.
All Plane issue generation MUST occur through the templating script:
`.agent/skills/routing/managing-plane-tasks/scripts/create_task.py`

## 3. High-Fidelity Solutions
When transitioning a Plane issue to **Done**, you MUST generate a comprehensive high-fidelity payload using the `solution_definition_schema.json` and post it using `post_solution.py`. Shallow updates or generic "fixed the code" comments are structurally invalid and will be rejected.

*Failure to comply with these rules corrupts the factory's structural memory.*
