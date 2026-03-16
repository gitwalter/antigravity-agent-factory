---
agents:
- '@Architect'
blueprints:
- universal
description: Antigravity workflow for plane-task-management. Standardized for IDX
  Visual Editor.
domain: universal
name: plane-task-management
steps:
- actions:
  - Check `mcp_memory_search_nodes` for existing workflows or epics.
  agents:
  - '@Architect'
  goal: ''
  name: Context Sourcing
  skills: []
  tools: []
- actions:
  - '**Lead Agent**: `system-architecture-specialist` or `template-creator`'
  - '**Skill**: `managing-plane-tasks`'
  - Run `mcp_plane_list_labels`, `mcp_plane_list_states`, and `mcp_plane_list_cycles`.
  agents:
  - '@Architect'
  goal: ''
  name: Discovery and State Sync
  skills: []
  tools: []
- actions:
  - Create a `task.json` file with all schema requirements (start_date, target_date,
    estimate_point, workflows, agents, skills, etc.).
  - Use `python .agent/skills/routing/managing-plane-tasks/scripts/create_task.py
    --json task.json` to generate the task.
  agents:
  - '@Architect'
  goal: ''
  name: Task Instantiation
  skills: []
  tools: []
- actions:
  - Use `mcp_plane_add_work_items_to_module` to attach the issue to its domain.
  - Use `mcp_plane_add_work_items_to_cycle` to attach the issue to the active sprint.
  agents:
  - '@Architect'
  goal: ''
  name: Module and Cycle Assignment
  skills: []
  tools: []
- actions:
  - Throughout implementation, use `mcp_plane_create_work_item_comment` to push implementation
    plans and updates directly to the issue.
  agents:
  - '@Architect'
  goal: ''
  name: Execution and Continuous Documentation
  skills: []
  tools: []
- actions:
  - '**Axiomatic Alignment**: Ensure Truth, Beauty, and Love.'
  - '**Memory First**: Check context before execution.'
  - '**Verifiability**: Document every step.'
  - '[workflow-standard.md](file:///.agent/rules/workflow-standard.md)'
  - Prepare `solution.json` with technical depth separating mechanics from architecture.
  - Run `python .agent/skills/routing/managing-plane-tasks/scripts/managing-plane-tasks.py`
    to finalize and transition the state to Done.
  agents:
  - '@Architect'
  goal: ''
  name: High-Fidelity Solution Closure
  skills: []
  tools: []
tags: []
type: sequential
version: 1.0.0
---

# Plane Issue Management

**Version:** 1.0.0

## Overview
Antigravity workflow for managing project tasks and issues within the Plane system. Standardized for IDX Visual Editor.

## Trigger Conditions
- Need to create, update, or close a task in the Plane project management system.
- Requirement for tracking work items against cycles or modules.
- User request: `/plane-task-management`.

**Trigger Examples:**
- "Create a new Plane issue for the 'User Authentication' feature."
- "Update the status of task AGENT-141 to 'Done' and post the resolution."

## Phases

### 1. Context Sourcing
- **Agents**: `@Architect`
- Check `mcp_memory_search_nodes` for existing workflows or epics.

### 2. Discovery and State Sync
- **Agents**: `@Architect`
- **Lead Agent**: `system-architecture-specialist` or `template-creator`
- **Skill**: `managing-plane-tasks`
- Run `mcp_plane_list_labels`, `mcp_plane_list_states`, and `mcp_plane_list_cycles`.

### 3. Task Instantiation
- **Agents**: `@Architect`
- Create a `task.json` file with all schema requirements (start_date, target_date, estimate_point, workflows, agents, skills, etc.).
- Use `python .agent/skills/routing/managing-plane-tasks/scripts/create_task.py --json task.json` to generate the task.

### 4. Module and Cycle Assignment
- **Agents**: `@Architect`
- Use `mcp_plane_add_work_items_to_module` to attach the issue to its domain.
- Use `mcp_plane_add_work_items_to_cycle` to attach the issue to the active sprint.

### 5. Execution and Continuous Documentation
- **Agents**: `@Architect`
- Throughout implementation, use `mcp_plane_create_work_item_comment` to push implementation plans and updates directly to the issue.

### 6. High-Fidelity Solution Closure
- **Agents**: `@Architect`
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
- Prepare `solution.json` with technical depth separating mechanics from architecture.
- Run `python .agent/skills/routing/managing-plane-tasks/scripts/managing-plane-tasks.py` to finalize and transition the state to Done.
