---
## Overview

description: Systematic workflow for maintaining a healthy product backlog through prioritization, estimation, story refinement, a...
---

# Backlog Refinement

Systematic workflow for maintaining a healthy product backlog through prioritization, estimation, story refinement, and readiness verification. Ensures the backlog is always ready for sprint planning.

**Version:** 1.0.0
**Created:** 2026-02-02
**Agent:** product-owner

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
Fetch current issues from Plane:
`conda run -p D:\Anaconda\envs\cursor-factory python scripts/pms/manager.py list`

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

### Generate Refinement Report


## Decision Points

- Is the requirement clear?
- Are the tests passing?


## Example Session

User: Run the workflow
Agent: Initiating workflow steps...
