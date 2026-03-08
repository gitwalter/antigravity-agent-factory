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

### Inventory Backlog
Fetch current issues from Plane using the `mcp-plane` server:
Use the `mcp_plane_list_project_issues` tool to fetch current project issues.
```json
{
  "project_id": "e71eb003-87d4-4b0c-a765-a044ac5affbe"
}
```
*Tip: Analyze returned state identifiers to recognize Backlog vs. Todo items.*

### Assess Backlog Health

### Review Top Items

### Apply Priority Changes

### Review Acceptance Criteria

### Clarify Story Details

### Split Large Stories

### Identify Unestimated Items

### Conduct Estimation

### Apply Definition of Ready

### Calculate Ready Sprint Coverage

### Update Backlog Status
Update issue states in Plane (e.g., set to "Todo" after refinement).

### Generate Refinement Report
Summarize Plane tasks refined.


## Decision Points

- Is the requirement clear?
- Are the tests passing?


## Example Session

User: Run the workflow
Agent: Initiating workflow steps...


## Trigger Examples
- "Execute this workflow."
