---
description: Systematic workflow for maintaining a healthy product backlog through prioritization, estimation, story refinement, a...
version: 1.0.0
---

# Backlog Refinement

Systematic workflow for maintaining a healthy product backlog through prioritization, estimation, story refinement, and readiness verification. Ensures the backlog is always ready for sprint planning.

**Version:** 1.0.0
**Created:** 2026-02-02
**Agent:** workflow-architect

## Trigger Conditions

This workflow is activated when:

- Weekly refinement session scheduled
- User requests backlog grooming
- New items need estimation
- Pre-planning preparation needed

**Trigger Examples:**
- "Refine the backlog"
- "Groom user stories"
- "Prepare backlog for planning"
- "Estimate new stories"

## Steps

## Phases

### 1. Inventory & Health Check
- **Goal**: Map the current state of the backlog.
- **Action**: List project issues and categorize by state UUIDs.
- **Tool**: `mcp_plane_list_project_issues`.
- **Filter**: Identify "Backlog" (`294ddb00...`) vs "Todo" (`8e155185...`) items.

### 2. Review & Refinement
- **Goal**: Improve clarity and priority of top items.
- **Action 1**: For unestimated items, apply the Fibonacci scale (1, 2, 3, 5, 8, 13).
- **Action 2**: Verify "Definition of Ready" (DoR) — clear requirements, acceptance criteria, and tagged assets (workflows, skills).
- **Tool**: `mcp_plane_update_work_item` to set `estimate_point` and `priority`.

### 3. Readiness Verification
- **Goal**: Ensure the upcoming sprint is fully covered.
- **Action**: Calculate "Sprint Health" by checking if top items have `acceptance_criteria` and `labels`.

### 4. Status Update & Reporting
- **Goal**: Formalize the refined state.
- **Action**: Move ready items to "Todo".
- **Tool**: `mcp_plane_update_work_item` with `state_id`.
- **Reporting**: Invoke `/documentation-workflow` to summarize the session.


## Decision Points

- Is the requirement clear?
- Are the tests passing?


## Example Session

User: Run the workflow
Agent: Initiating workflow steps...


## Trigger Examples
- "Execute this workflow."
