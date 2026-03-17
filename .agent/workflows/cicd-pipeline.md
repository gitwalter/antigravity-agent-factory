---
agents:
- workflow-quality-specialist
- project-operations-specialist
blueprints:
- universal
description: Antigravity workflow for cicd-pipeline. Standardized for IDX Visual Editor.
domain: universal
name: cicd-pipeline
steps:
- actions:
  - '**Agents**: `project-operations-specialist`'
  - '**Actions**:'
  - Install dependencies and build artifacts.
  agents:
  - project-operations-specialist
  goal: Install dependencies and compile the source code.
  name: Build & Dependency Management
  skills:
  - cicd-pipeline
  tools:
  - npm
  - maven
  - gradle
- actions:
  - '**Agents**: `workflow-quality-specialist`'
  - '**Actions**:'
  - Run the test suite and verify coverage.
  agents:
  - workflow-quality-specialist
  goal: Execute unit and integration tests to ensure code quality.
  name: Automated Testing
  skills:
  - testing-agents
  tools:
  - jest
  - pytest
  - junit
- actions:
  - '**Agents**: `workflow-quality-specialist`'
  - '**Actions**:'
  - Execute SAST and dependency vulnerability scans.
  agents:
  - workflow-quality-specialist
  goal: Perform static analysis and dependency scanning.
  name: Security & Quality Scans
  skills:
  - securing-ai-systems
  - verifying-artifact-structures
  tools:
  - sonarqube
  - snyk
- actions:
  - '**Agents**: `project-operations-specialist`'
  - '**Actions**:'
  - Deploy to the staging environment and verify health.
  agents:
  - project-operations-specialist
  goal: Deploy to staging and perform smoke tests.
  name: Staging Deployment & Verification
  skills:
  - committing-releases
  tools:
  - kubectl
  - cf-push
- actions:
  - '**Agents**: `project-operations-specialist`'
  - '**Actions**:'
  - Execute production deployment and logging-and-monitoring post-release.
  - Is the requirement clear?
  - Are the tests passing?
  - '"Execute this workflow."'
  - '**Axiomatic Alignment**: Ensure Truth, Beauty, and Love.'
  - '**Memory First**: Check context before execution.'
  - '**Verifiability**: Document every step.'
  - '[workflow-standard.md](file:///.agent/rules/workflow-standard.md)'
  agents:
  - project-operations-specialist
  goal: Deploy to production after approval and verify.
  name: Production Release
  skills:
  - committing-releases
  - logging-and-monitoring
  tools:
  - safety-gate
  - grafana
tags: []
type: sequential
version: 2.0.0
---
# CI/CD Pipeline

**Version:** 1.0.0

## Overview
Antigravity workflow for CI/CD pipeline execution. Standardized for IDX Visual Editor.

## Trigger Conditions
- Code committed to the repository (automated trigger).
- Manual request to run the full CI/CD suite.
- User request: `/cicd-pipeline`.

**Trigger Examples:**
- "Run the CI/CD pipeline for the current branch."
- "Execute the build and deploy suite."

## Phases

### 1. Build & Dependency Management
- **Goal**: Install dependencies and compile the source code.
- **Agents**: `project-operations-specialist`
- **Skills**: cicd-pipeline
- **Tools**: npm, maven, gradle
- **Agents**: `project-operations-specialist`
- **Actions**:
- Install dependencies and build artifacts.

### 2. Automated Testing
- **Goal**: Execute unit and integration tests to ensure code quality.
- **Agents**: `workflow-quality-specialist`
- **Skills**: testing-agents
- **Tools**: jest, pytest, junit
- **Agents**: `workflow-quality-specialist`
- **Actions**:
- Run the test suite and verify coverage.

### 3. Security & Quality Scans
- **Goal**: Perform static analysis and dependency scanning.
- **Agents**: `workflow-quality-specialist`
- **Skills**: securing-ai-systems, verifying-artifact-structures
- **Tools**: sonarqube, snyk
- **Agents**: `workflow-quality-specialist`
- **Actions**:
- Execute SAST and dependency vulnerability scans.

### 4. Staging Deployment & Verification
- **Goal**: Deploy to staging and perform smoke tests.
- **Agents**: `project-operations-specialist`
- **Skills**: committing-releases
- **Tools**: kubectl, cf-push
- **Agents**: `project-operations-specialist`
- **Actions**:
- Deploy to the staging environment and verify health.

### 5. Production Release
- **Goal**: Deploy to production after approval and verify.
- **Agents**: `project-operations-specialist`
- **Skills**: committing-releases, logging-and-monitoring
- **Tools**: safety-gate, grafana
- **Agents**: `project-operations-specialist`
- **Actions**:
- Execute production deployment and logging-and-monitoring post-release.
- Is the requirement clear?
- Are the tests passing?
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
