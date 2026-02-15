---
## Overview

description: Comprehensive workflow for managing continuous integration and deployment pipelines. Covers build, test, security sca...
---

# Cicd Pipeline

Comprehensive workflow for managing continuous integration and deployment pipelines. Covers build, test, security scanning, and deployment across multiple environments.

**Version:** 1.0.0
**Created:** 2026-02-02
**Applies To:** All stacks

> **Note:** Directory paths referenced in this workflow ({directories.knowledge}/, {directories.skills}/, {directories.patterns}/, etc.) are configurable via `{directories.config}/settings.json`. See **Path Configuration Guide**.

## Trigger Conditions

This workflow is activated when:

- Push to main/develop branch
- Pull request created/updated
- Scheduled build
- Manual deployment request

**Trigger Examples:**
- "Deploy to staging"
- "Run the CI pipeline"
- "Build and test"
- "Release to production"

## Steps

### Install Dependencies

### Compile/Build

### Unit Tests

### Integration Tests

### SAST

### Dependency Scan

### Deploy

### Smoke Test

### Request Approval

### Production Deploy

### Verify Production


## Decision Points

- Is the requirement clear?
- Are the tests passing?


## Example Session

User: Run the workflow
Agent: Initiating workflow steps...
