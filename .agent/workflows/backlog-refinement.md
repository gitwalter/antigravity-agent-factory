---
agents:
- '@Architect'
blueprints:
- universal
description: Antigravity workflow for backlog-refinement. Standardized for IDX Visual
  Editor.
domain: universal
name: backlog-refinement
steps:
- actions:
  - '**Tool**: `mcp_plane_list_project_issues`.'
  - '**Filter**: Identify "Backlog" (`294ddb00...`) vs "Todo" (`8e155185...`) items.'
  - List project issues and categorize by state UUIDs.
  agents:
  - '@Architect'
  goal: Map the current state of the backlog.
  name: Inventory & Health Check
  skills: []
  tools: []
- actions:
  - '**Action 1**: For unestimated items, apply the Fibonacci scale (1, 2, 3, 5, 8,
    13).'
  - "**Action 2**: Verify \"Definition of Ready\" (DoR) \u2014 clear requirements,\
    \ acceptance criteria, and tagged assets (workflows, skills)."
  - '**Tool**: `mcp_plane_update_work_item` to set `estimate_point` and `priority`.'
  agents:
  - '@Architect'
  goal: Improve clarity and priority of top items.
  name: Review & Refinement
  skills: []
  tools: []
- actions:
  - Calculate "Sprint Health" by checking if top items have `acceptance_criteria`
    and `labels`.
  agents:
  - '@Architect'
  goal: Ensure the upcoming sprint is fully covered.
  name: Readiness Verification
  skills: []
  tools: []
- actions:
  - '**Tool**: `mcp_plane_update_work_item` with `state_id`.'
  - '**Reporting**: Invoke `/generating-documentation` to summarize the session.'
  - Is the requirement clear?
  - Are the tests passing?
  - '"Execute this workflow."'
  - '**Axiomatic Alignment**: Ensure Truth, Beauty, and Love.'
  - '**Memory First**: Check context before execution.'
  - '**Verifiability**: Document every step.'
  - '[workflow-standard.md](file:///.agent/rules/workflow-standard.md)'
  - Move ready items to "Todo".
  agents:
  - '@Architect'
  goal: Formalize the refined state.
  name: Status Update & Reporting
  skills: []
  tools: []
tags: []
type: sequential
version: 1.0.0
---

# Backlog Refinement

**Version:** 1.0.0

## Overview
Antigravity workflow for backlog-refinement. Standardized for IDX Visual Editor.

## Trigger Conditions
- Large volume of unrefined tasks in Plane.
- Upcoming sprint planning requires readiness verification.
- User request: `/backlog-refinement`.

**Trigger Examples:**
- "Refine the backlog for Project X."
- "Prepare the next sprint."

## Phases

### 1. Inventory & Health Check
- **Goal**: Map the current state of the backlog.
- **Agents**: `@Architect`
- **Tool**: `mcp_plane_list_project_issues`.
- **Filter**: Identify "Backlog" (`294ddb00...`) vs "Todo" (`8e155185...`) items.
- List project issues and categorize by state UUIDs.

### 2. Review & Refinement
- **Goal**: Improve clarity and priority of top items.
- **Agents**: `@Architect`
- **Action 1**: For unestimated items, apply the Fibonacci scale (1, 2, 3, 5, 8, 13).
- **Action 2**: Verify "Definition of Ready" (DoR) — clear requirements, acceptance criteria, and tagged assets (workflows, skills).
- **Tool**: `mcp_plane_update_work_item` to set `estimate_point` and `priority`.

### 3. Readiness Verification
- **Goal**: Ensure the upcoming sprint is fully covered.
- **Agents**: `@Architect`
- Calculate "Sprint Health" by checking if top items have `acceptance_criteria` and `labels`.

### 4. Status Update & Reporting
- **Goal**: Formalize the refined state.
- **Agents**: `@Architect`
- **Tool**: `mcp_plane_update_work_item` with `state_id`.
- **Reporting**: Invoke `/generating-documentation` to summarize the session.
- Is the requirement clear?
- Are the tests passing?
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
- Move ready items to "Todo".
