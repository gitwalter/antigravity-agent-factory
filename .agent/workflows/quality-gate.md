---
## Overview

description: Automated quality gate workflow that enforces code quality standards before merge. Runs comprehensive checks includin...
---

# Quality Gate

Automated quality gate workflow that enforces code quality standards before merge. Runs comprehensive checks including linting, testing, coverage, security scanning, and code review to ensure only high-quality code enters the codebase.

**Version:** 1.0.0  
**Created:** 2026-02-02  
**Agent:** code-reviewer

## Trigger Conditions

This workflow is activated when:

- Pull request is opened or updated
- Pre-merge check is requested
- CI/CD pipeline runs quality checks
- User requests quality validation

**Trigger Examples:**
- "Run quality checks on this PR"
- "Check if PR #123 is ready to merge"
- "Validate code quality"
- "Pre-merge check"

## Steps

### Lint Check

### Type Check

### Format Check

### Unit Tests

### Integration Tests

### Coverage Analysis

### Dependency Scan

### Secret Scan

### SAST (Static Application Security Testing)

### Complexity Analysis

### Design Pattern Check

### Documentation Integrity Check
- **Agent**: `system-steward`
- **Skill**: `repository-governance`
- **Action**: Run `python scripts/maintenance/link_checker.py` to ensure the PR doesn't introduce broken links or misplace files.

### Aggregate Results

### Render Decision


## Decision Points

- Is the requirement clear?
- Are the tests passing?


## Example Session

User: Run the workflow
Agent: Initiating workflow steps...
