---
description: Systematic workflow for managing Plane PMS issues and states
agents:
- template-creator
version: 1.0.0
tags:
- plane
- task
- management
- standardized
---


# Plane Issue Management Workflow

**Version:** 1.0.0


This workflow orchestrates the remote management of Plane PMS issues and states using the Plane MCP server and the `managing-plane-tasks` skill.

## Trigger Conditions
- When transitioning tasks between backlog, todo, in progress, and done.
- When formalizing new feature requests or bug reports into Plane tasks.
- When closing sprints, finalizing solutions, or updating epic context.

## Trigger Examples:
- "Update AGENT-102 to Done"
- "Create a new issue in Plane for the missing IDE workflows"

## Steps
### 0. Context Sourcing
Before creating or updating tasks, query the Memory MCP graph to understand existing architectures and related initiatives.
- **Action**: Check `mcp_memory_search_nodes` for existing workflows or epics.

## 1. Discovery and State Sync
Always fetch current labels, states, and cycles to ensure you use valid UUIDs.
- **Lead Agent**: `system-architecture-specialist` or `template-creator`
- **Skill**: `managing-plane-tasks`
- **Action**: Run `mcp_plane_list_labels`, `mcp_plane_list_states`, and `mcp_plane_list_cycles`.

## 2. Task Instantiation
Convert unstructured requests into formal Plane issues following the strict factory schema.
- **Action**: Create a `task.json` file with all schema requirements (start_date, target_date, estimate_point, workflows, agents, skills, etc.).
- **Action**: Use `python .agent/skills/routing/managing-plane-tasks/scripts/create_task.py --json task.json` to generate the task.

## 3. Module and Cycle Assignment
- **Action**: Use `mcp_plane_add_work_items_to_module` to attach the issue to its domain.
- **Action**: Use `mcp_plane_add_work_items_to_cycle` to attach the issue to the active sprint.

## 4. Execution and Continuous Documentation
- **Action**: Throughout implementation, use `mcp_plane_create_work_item_comment` to push implementation plans and updates directly to the issue.

## 5. High-Fidelity Solution Closure
- **Action**: Prepare `solution.json` with technical depth separating mechanics from architecture.
- **Action**: Run `python .agent/skills/routing/managing-plane-tasks/scripts/managing-plane-tasks.py` to finalize and transition the state to Done.


## Best Practices
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.


## Related
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
