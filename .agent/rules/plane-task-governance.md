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

## 4. Idempotency & Duplicate Prevention
Agents MUST maintain "Conscious Action" to avoid workspace clutter. Before creating any NEW Plane issue:
1.  **Search First**: Query the Plane API (or use `list_issues.py`) to check if an issue with the same name or primary objective already exists.
2.  **Parent Context**: Verify if the intended sub-task already exists under the target parent.
3.  **No Redundancy**: If a duplicate is found, the agent MUST skip creation and instead update or refer to the existing issue.

*Failure to comply with these rules corrupts the factory's structural memory.*
