---
description: Systematic workflow for planning sprints, including backlog review, capacity
  calculation, story selection, and sprint...
version: 1.0.0
tags:
- sprint
- planning
- standardized
---


# Sprint Planning

Systematic workflow for planning sprints, including backlog review, capacity calculation, story selection, and sprint goal definition. Integrates with project management tools to automate repetitive planning tasks.

**Version:** 1.0.0
**Created:** 2026-02-02
**Agent:** system-architecture-specialist

> **Note:** Directory paths referenced in this workflow ({directories.knowledge}/, {directories.skills}/, {directories.patterns}/, etc.) are configurable via `{directories.config}/settings.json`. See **Path Configuration Guide**.

## Trigger Conditions

This workflow is activated when:

- Sprint planning meeting scheduled
- New sprint needs to be created
- User requests sprint setup
- Schedule triggers planning cycle

**Trigger Examples:**
- "Plan the next sprint"
- "Set up Sprint 15"
- "Start sprint planning"
- "Prepare for sprint planning meeting"

## Steps

## Phases

### 1. Velocity & Capacity Analysis
- **Goal**: Determine how much work the team can take on.
- **Action**: Review the previous sprint's completion rate.
- **Tool**: `mcp_plane_list_cycle_issues` for the past cycle.

### 2. Backlog Grooming & Selection
- **Goal**: Identify "Ready" items for the upcoming sprint.
- **Action**: Select items from the "Todo" state that meet the Definition of Ready (DoR).
- **Tool**: `mcp_plane_list_project_issues` and local filtering.

### 3. Sprint Creation & Goal Setting
- **Goal**: Formalize the new iteration.
- **Action 1**: Create the new cycle if it doesn't exist.
- **Action 2**: Define a concise Sprint Goal in the cycle description.
- **Tool**: `mcp_plane_create_cycle`.

### 4. Work Association
- **Goal**: Move selected items into the new sprint.
- **Action**: Update the `cycle_id` and `start_date`/`target_date` for each issue.
- **Tool**: `associate_task.py` script.

### 5. Planning Finalization
- **Goal**: Ensure the sprint is balanced and understood.
- **Action**: Generate a sprint summary report and notify the team.
- **Tool**: Invoke `/generating-documentation`.


## Decision Points

- Is the requirement clear?
- Are the tests passing?


## Example Session

User: Run the workflow
Agent: Initiating workflow steps...


## Trigger Examples
- "Execute this workflow."


## Best Practices
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.


## Related
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
