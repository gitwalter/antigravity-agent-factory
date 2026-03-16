---
agents:
- '@Architect'
blueprints:
- universal
description: Antigravity workflow for sprint-planning. Standardized for IDX Visual
  Editor.
domain: universal
name: sprint-planning
steps:
- actions:
  - '**Tool**: `mcp_plane_list_cycle_issues` for the past cycle.'
  - Review the previous sprint's completion rate.
  agents:
  - '@Architect'
  goal: Determine how much work the team can take on.
  name: Velocity & Capacity Analysis
  skills: []
  tools: []
- actions:
  - '**Tool**: `mcp_plane_list_project_issues` and local filtering.'
  - Select items from the "Todo" state that meet the Definition of Ready (DoR).
  agents:
  - '@Architect'
  goal: Identify "Ready" items for the upcoming sprint.
  name: Backlog Grooming & Selection
  skills: []
  tools: []
- actions:
  - '**Action 1**: Create the new cycle if it doesn''t exist.'
  - '**Action 2**: Define a concise Sprint Goal in the cycle description.'
  - '**Tool**: `mcp_plane_create_cycle`.'
  agents:
  - '@Architect'
  goal: Formalize the new iteration.
  name: Sprint Creation & Goal Setting
  skills: []
  tools: []
- actions:
  - '**Tool**: `associate_task.py` script.'
  - Update the `cycle_id` and `start_date`/`target_date` for each issue.
  agents:
  - '@Architect'
  goal: Move selected items into the new sprint.
  name: Work Association
  skills: []
  tools: []
- actions:
  - '**Tool**: Invoke `/generating-documentation`.'
  - Is the requirement clear?
  - Are the tests passing?
  - '"Execute this workflow."'
  - '**Axiomatic Alignment**: Ensure Truth, Beauty, and Love.'
  - '**Memory First**: Check context before execution.'
  - '**Verifiability**: Document every step.'
  - '[workflow-standard.md](file:///.agent/rules/workflow-standard.md)'
  - Generate a sprint summary report and notify the team.
  agents:
  - '@Architect'
  goal: Ensure the sprint is balanced and understood.
  name: Planning Finalization
  skills: []
  tools: []
tags: []
type: sequential
version: 1.0.0
---

# Sprint Planning Workflow

**Version:** 1.0.0

## Overview
Antigravity workflow for planning and initiating a new development sprint (cycle) in the Plane system. Standardized for IDX Visual Editor.

## Trigger Conditions
- Beginning of a new development iteration or sprint.
- Need to groom the backlog and associate tasks with a new cycle.
- User request: `/sprint-planning`.

**Trigger Examples:**
- "Start the sprint planning for 'Cycle 2024-Q3-W42' in Plane."
- "Execute the sprint planning workflow to groom the backlog and set new goals."

## Phases

### 1. Velocity & Capacity Analysis
- **Goal**: Determine how much work the team can take on.
- **Agents**: `@Architect`
- **Tool**: `mcp_plane_list_cycle_issues` for the past cycle.
- Review the previous sprint's completion rate.

### 2. Backlog Grooming & Selection
- **Goal**: Identify "Ready" items for the upcoming sprint.
- **Agents**: `@Architect`
- **Tool**: `mcp_plane_list_project_issues` and local filtering.
- Select items from the "Todo" state that meet the Definition of Ready (DoR).

### 3. Sprint Creation & Goal Setting
- **Goal**: Formalize the new iteration.
- **Agents**: `@Architect`
- **Action 1**: Create the new cycle if it doesn't exist.
- **Action 2**: Define a concise Sprint Goal in the cycle description.
- **Tool**: `mcp_plane_create_cycle`.

### 4. Work Association
- **Goal**: Move selected items into the new sprint.
- **Agents**: `@Architect`
- **Tool**: `associate_task.py` script.
- Update the `cycle_id` and `start_date`/`target_date` for each issue.

### 5. Planning Finalization
- **Goal**: Ensure the sprint is balanced and understood.
- **Agents**: `@Architect`
- **Tool**: Invoke `/generating-documentation`.
- Is the requirement clear?
- Are the tests passing?
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
- Generate a sprint summary report and notify the team.
