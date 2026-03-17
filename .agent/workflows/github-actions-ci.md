---
agents:
- workflow-quality-specialist
- project-operations-specialist
blueprints:
- universal
description: Antigravity workflow for github-actions-ci. Standardized for IDX Visual
  Editor.
domain: universal
name: github-actions-ci
steps:
- actions:
  - '**Agents**: `project-operations-specialist`'
  - '**Actions**:'
  - Define stages and set up repository secrets.
  agents:
  - project-operations-specialist
  goal: Define CI/CD stages and configure environment secrets.
  name: Workflow Design & Setup
  skills:
  - github-actions-ci
  tools:
  - gh-cli
- actions:
  - '**Agents**: `project-operations-specialist`'
  - '**Actions**:'
  - Create `.github/workflows/*.yml` files.
  - Define jobs for build, test, and deploy.
  agents:
  - project-operations-specialist
  goal: Create YAML workflow files and add necessary jobs.
  name: Workflow Implementation
  skills:
  - github-actions-ci
  tools:
  - write_to_file
- actions:
  - '**Agents**: `project-operations-specialist`, `workflow-quality-specialist`'
  - '**Actions**:'
  - Trigger workflow and debug errors.
  agents:
  - project-operations-specialist
  - workflow-quality-specialist
  goal: Trigger the workflow and resolve any execution failures.
  name: Trigger & Debugging
  skills:
  - debug-pipeline
  tools:
  - gh-run-view
  - gh-run-rerun
- actions:
  - '**Agents**: `project-operations-specialist`'
  - '**Actions**:'
  - Add logging-and-monitoring and document maintenance procedures.
  - Is the requirement clear?
  - Are the tests passing?
  - '"Execute this workflow."'
  - '**Axiomatic Alignment**: Ensure Truth, Beauty, and Love.'
  - '**Memory First**: Check context before execution.'
  - '**Verifiability**: Document every step.'
  - '[workflow-standard.md](file:///.agent/rules/workflow-standard.md)'
  agents:
  - project-operations-specialist
  goal: Set up logging-and-monitoring for pipeline health and perform maintenance.
  name: Monitoring & Maintenance
  skills:
  - logging-and-monitoring
  - github-actions-ci
  tools:
  - github-dashboard
tags: []
type: sequential
version: 2.0.0
---
# GitHub Actions CI

**Version:** 1.0.0

## Overview
Antigravity workflow for GitHub Actions CI pipeline setup and maintenance. Standardized for IDX Visual Editor.

## Trigger Conditions
- New repository setup requiring CI/CD automation.
- Requirement for automated build, test, or deployment workflows.
- User request: `/github-actions-ci`.

**Trigger Examples:**
- "Set up a GitHub Action to run tests on every pull request."
- "Implement a deployment workflow for the 'Staging' environment."

## Phases

### 1. Workflow Design & Setup
- **Goal**: Define CI/CD stages and configure environment secrets.
- **Agents**: `project-operations-specialist`
- **Skills**: github-actions-ci
- **Tools**: gh-cli
- **Agents**: `project-operations-specialist`
- **Actions**:
- Define stages and set up repository secrets.

### 2. Workflow Implementation
- **Goal**: Create YAML workflow files and add necessary jobs.
- **Agents**: `project-operations-specialist`
- **Skills**: github-actions-ci
- **Tools**: write_to_file
- **Agents**: `project-operations-specialist`
- **Actions**:
- Create `.github/workflows/*.yml` files.
- Define jobs for build, test, and deploy.

### 3. Trigger & Debugging
- **Goal**: Trigger the workflow and resolve any execution failures.
- **Agents**: `project-operations-specialist`, `workflow-quality-specialist`
- **Skills**: debug-pipeline
- **Tools**: gh-run-view, gh-run-rerun
- **Agents**: `project-operations-specialist`, `workflow-quality-specialist`
- **Actions**:
- Trigger workflow and debug errors.

### 4. Monitoring & Maintenance
- **Goal**: Set up logging-and-monitoring for pipeline health and perform maintenance.
- **Agents**: `project-operations-specialist`
- **Skills**: logging-and-monitoring, github-actions-ci
- **Tools**: github-dashboard
- **Agents**: `project-operations-specialist`
- **Actions**:
- Add logging-and-monitoring and document maintenance procedures.
- Is the requirement clear?
- Are the tests passing?
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
