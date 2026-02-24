---
## Overview

description: Systematic workflow for resolving bugs from ticket analysis through implementation and verification. This workflow en...
---

# Bugfix Resolution

Systematic workflow for resolving bugs from ticket analysis through implementation and verification. This workflow ensures thorough root cause analysis, proper fix implementation, and comprehensive testing.

**Version:** 1.0.0
**Created:** 2026-02-02
**Agent:** debug-conductor

> **Note:** Directory paths referenced in this workflow ({directories.knowledge}/, {directories.skills}/, {directories.patterns}/, etc.) are configurable via `{directories.config}/settings.json`. See **Path Configuration Guide**.

## Trigger Conditions

This workflow is activated when:

- Jira, GitHub, GitLab, or Plane issue is mentioned
- User reports a bug or defect
- Error report requires investigation
- Test failure needs resolution

**Trigger Examples:**
- "Fix bug PROJ-123"
- "Resolve issue #456"
- "Fix Plane task AGENT-12"
- "The login page is throwing an error"
- "Users are reporting data not saving"

## Steps

### Fetch Ticket Details
If a Plane issue is provided, use the native `pms-management` skill:
`conda run -p D:\Anaconda\envs\cursor-factory python scripts/pms/manager.py list`

### Classify Bug Severity

### Ground Data Model

### Gather Code Context

### Reproduce the Bug

### Trace Error Origin

### Identify Recent Changes

### Form Hypothesis

### Create Implementation Plan

### Write Regression Test

### Implement Fix

### Verify Fix Locally

### Run Full Test Suite

### Code Review

### Update Ticket
Update the status in Plane using:
`conda run -p D:\Anaconda\envs\cursor-factory python scripts/pms/manager.py update --id <SEQ_ID> --state "Done"`

### Capture Lessons


## Decision Points

- Is the requirement clear?
- Are the tests passing?


## Example Session

User: Run the workflow
Agent: Initiating workflow steps...
