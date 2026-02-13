---
description: Systematic workflow for debugging CI/CD pipeline failures. This workflow demonstrates the Cursor Agent Factory workfl...
---

# Debug Pipeline

Systematic workflow for debugging CI/CD pipeline failures. This workflow demonstrates the Cursor Agent Factory workflow system architecture with phases, decision points, escalation paths, and learning hooks.

**Version:** 1.0.0  
**Created:** 2026-01-31  
**Agent:** debug-conductor

> **Note:** Directory paths referenced in this workflow ({directories.knowledge}/, {directories.skills}/, {directories.patterns}/, etc.) are configurable via `{directories.config}/settings.json`. See [Path Configuration Guide](../docs/reference/path-configuration.md).

## Trigger Conditions

This workflow is activated when:

- CI/CD pipeline reports failure
- Test suite fails locally or in CI
- User mentions "pipeline failing", "tests broken", "CI red"
- GitHub Actions workflow fails
- Pre-commit hook reports errors

**Trigger Examples:**
- "The CI is failing, can you fix it?"
- "Debug the pipeline failure"
- "Tests are broken after my last commit"
- "Fix the GitHub Actions error"

## Steps

### Gather Error Information

### Classify Error Type

### Trace Error Origin

### Identify Recent Changes

### Form Hypothesis

### Evaluate Fix Options

### Implement Fix

### Local Verification

### Run Full Test Suite

### Validate Fix

### Capture Pattern

### Update Knowledge
