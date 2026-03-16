---
description: Comprehensive workflow for managing continuous integration and deployment
  pipelines. Covers build, test, security sca...
version: 1.0.0
tags:
- cicd
- pipeline
- standardized
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

## Phases

### Phase 1: Build & Dependency Management
- **Goal**: Install dependencies and compile the source code.
- **Agents**: `project-operations-specialist`
- **Skills**: cicd-pipeline
- **Tools**: npm, maven, gradle
- **Actions**:
    - Install dependencies and build artifacts.

### Phase 2: Automated Testing
- **Goal**: Execute unit and integration tests to ensure code quality.
- **Agents**: `workflow-quality-specialist`
- **Skills**: testing-agents
- **Tools**: jest, pytest, junit
- **Actions**:
    - Run the test suite and verify coverage.

### Phase 3: Security & Quality Scans
- **Goal**: Perform static analysis and dependency scanning.
- **Agents**: `workflow-quality-specialist`
- **Skills**: securing-ai-systems, verifying-artifact-structures
- **Tools**: sonarqube, snyk
- **Actions**:
    - Execute SAST and dependency vulnerability scans.

### Phase 4: Staging Deployment & Verification
- **Goal**: Deploy to staging and perform smoke tests.
- **Agents**: `project-operations-specialist`
- **Skills**: committing-releases
- **Tools**: kubectl, cf-push
- **Actions**:
    - Deploy to the staging environment and verify health.

### Phase 5: Production Release
- **Goal**: Deploy to production after approval and verify.
- **Agents**: `project-operations-specialist`
- **Skills**: committing-releases, logging-and-monitoring
- **Tools**: safety-gate, grafana
- **Actions**:
    - Execute production deployment and logging-and-monitoring post-release.


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
