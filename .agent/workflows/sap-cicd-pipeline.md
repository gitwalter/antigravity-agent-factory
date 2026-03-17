---
agents:
- workflow-quality-specialist
- project-operations-specialist
blueprints:
- universal
description: Antigravity workflow for sap-cicd-pipeline. Standardized for IDX Visual
  Editor.
domain: universal
name: sap-cicd-pipeline
steps:
- actions:
  - '**Agents**: `project-operations-specialist`, `workflow-quality-specialist`'
  - '**Actions**:'
  - Configure build scripts and MTA build.
  - Configure unit, integration, and E2E tests.
  agents:
  - project-operations-specialist
  - workflow-quality-specialist
  goal: Establish automated build scripts and testing-agents suites for SAP applications.
  name: Build & Test Configuration
  skills:
  - cicd-pipeline
  - verifying-artifact-structures
  tools:
  - write_to_file
- actions:
  - '**Agents**: `project-operations-specialist`'
  - '**Actions**:'
  - Configure GitHub Actions (or alternative service).
  agents:
  - project-operations-specialist
  goal: Implement the CI/CD pipeline using GitHub Actions, Jenkins, or SAP CI/CD service.
  name: Pipeline Implementation
  skills:
  - github-actions-ci
  tools:
  - write_to_file
- actions:
  - '**Agents**: `project-operations-specialist`'
  - '**Actions**:'
  - Configure transport requests and validation.
  - Configure BTP or On-Premise deployment.
  agents:
  - project-operations-specialist
  goal: Orchestrate transports and deployment to SAP BTP or On-Premise systems.
  name: Transport & Deployment Management
  skills:
  - committing-releases
  tools:
  - sap-transport-management-service
- actions:
  - '**Agents**: `project-operations-specialist`'
  - '**Actions**:'
  - Configure pipeline notifications and deployment logging-and-monitoring.
  - Is the requirement clear?
  - Are the tests passing?
  - '"Execute this workflow."'
  - '**Axiomatic Alignment**: Ensure Truth, Beauty, and Love.'
  - '**Memory First**: Check context before execution.'
  - '**Verifiability**: Document every step.'
  - '[workflow-standard.md](file:///.agent/rules/workflow-standard.md)'
  agents:
  - project-operations-specialist
  goal: Establish feedback loops with notifications and performance logging-and-monitoring.
  name: Notification & Monitoring
  skills:
  - logging-and-monitoring
  tools:
  - slack-webhooks
  - prometheus
tags: []
type: sequential
version: 2.0.0
---
# SAP CI/CD Pipeline Configuration

**Version:** 1.0.0

## Overview
Antigravity workflow for configuring and managing CI/CD pipelines for SAP applications. Standardized for IDX Visual Editor.

## Trigger Conditions
- Need to set up a new CI/CD pipeline for an SAP project.
- Requirement for automating builds, tests, and deployments in the SAP ecosystem.
- User request: `/sap-cicd-pipeline`.

**Trigger Examples:**
- "Setup a GitHub Actions pipeline for the 'Production Management' SAP backend."
- "Configure the CI/CD pipeline for our MTA-based Fiori application."

## Phases

### 1. Build & Test Configuration
- **Goal**: Establish automated build scripts and testing-agents suites for SAP applications.
- **Agents**: `project-operations-specialist`, `workflow-quality-specialist`
- **Skills**: cicd-pipeline, verifying-artifact-structures
- **Tools**: write_to_file
- **Agents**: `project-operations-specialist`, `workflow-quality-specialist`
- **Actions**:
- Configure build scripts and MTA build.
- Configure unit, integration, and E2E tests.

### 2. Pipeline Implementation
- **Goal**: Implement the CI/CD pipeline using GitHub Actions, Jenkins, or SAP CI/CD service.
- **Agents**: `project-operations-specialist`
- **Skills**: github-actions-ci
- **Tools**: write_to_file
- **Agents**: `project-operations-specialist`
- **Actions**:
- Configure GitHub Actions (or alternative service).

### 3. Transport & Deployment Management
- **Goal**: Orchestrate transports and deployment to SAP BTP or On-Premise systems.
- **Agents**: `project-operations-specialist`
- **Skills**: committing-releases
- **Tools**: sap-transport-management-service
- **Agents**: `project-operations-specialist`
- **Actions**:
- Configure transport requests and validation.
- Configure BTP or On-Premise deployment.

### 4. Notification & Monitoring
- **Goal**: Establish feedback loops with notifications and performance logging-and-monitoring.
- **Agents**: `project-operations-specialist`
- **Skills**: logging-and-monitoring
- **Tools**: slack-webhooks, prometheus
- **Agents**: `project-operations-specialist`
- **Actions**:
- Configure pipeline notifications and deployment logging-and-monitoring.
- Is the requirement clear?
- Are the tests passing?
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
