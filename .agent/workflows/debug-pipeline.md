---
description: Systematic workflow for analyzing-code CI/CD pipeline failures. This workflow
  demonstrates the Antigravity Agent Factory workfl...
version: 1.0.0
tags:
- debug
- pipeline
- standardized
---


# Debug Pipeline

Systematic workflow for analyzing-code CI/CD pipeline failures. This workflow demonstrates the Antigravity Agent Factory workflow system architecture with phases, decision points, escalation paths, and learning hooks.

**Version:** 1.0.0
**Created:** 2026-01-31
**Agent:** workflow-quality-specialist

> **Note:** Directory paths referenced in this workflow ({directories.knowledge}/, {directories.skills}/, {directories.patterns}/, etc.) are configurable via `{directories.config}/settings.json`. See **Path Configuration Guide**.

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
