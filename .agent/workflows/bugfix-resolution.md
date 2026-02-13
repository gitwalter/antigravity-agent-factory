---
description: Systematic workflow for resolving bugs from ticket analysis through implementation and verification. This workflow en...
---

# Bugfix Resolution

Systematic workflow for resolving bugs from ticket analysis through implementation and verification. This workflow ensures thorough root cause analysis, proper fix implementation, and comprehensive testing.

**Version:** 1.0.0  
**Created:** 2026-02-02  
**Agent:** debug-conductor

> **Note:** Directory paths referenced in this workflow ({directories.knowledge}/, {directories.skills}/, {directories.patterns}/, etc.) are configurable via `{directories.config}/settings.json`. See [Path Configuration Guide](../docs/reference/path-configuration.md).

## Trigger Conditions

This workflow is activated when:

- Jira, GitHub, or GitLab bug ticket is mentioned
- User reports a bug or defect
- Error report requires investigation
- Test failure needs resolution

**Trigger Examples:**
- "Fix bug PROJ-123"
- "Resolve issue #456"
- "The login page is throwing an error"
- "Users are reporting data not saving"

## Steps

### Fetch Ticket Details

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

### Capture Lessons
