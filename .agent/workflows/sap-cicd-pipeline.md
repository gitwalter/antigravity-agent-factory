---
description: End-to-end workflow for setting up CI/CD pipelines for SAP applications.
  Covers build automation, testing-agents, transport ...
version: 1.0.0
tags:
- sap
- cicd
- pipeline
- standardized
---


# Sap Cicd Pipeline

End-to-end workflow for setting up CI/CD pipelines for SAP applications. Covers build automation, testing-agents, transport management, and deployment to SAP systems.

**Version:** 1.0.0
**Created:** 2026-02-09
**Applies To:** sap-systems-specialist, btp-deployment

## Trigger Conditions

This workflow is activated when:

- Setting up CI/CD for SAP applications
- Automating build and deployment
- Configuring transport management
- Setting up automated testing-agents

**Trigger Examples:**
- "Set up CI/CD pipeline for my CAP application"
- "Automate deployment to BTP"
- "Configure transport automation"
- "Set up automated testing-agents pipeline"

## Phases

### Phase 1: Build & Test Configuration
- **Goal**: Establish automated build scripts and testing-agents suites for SAP applications.
- **Agents**: `project-operations-specialist`, `workflow-quality-specialist`
- **Skills**: cicd-pipeline, verifying-artifact-structures
- **Tools**: write_to_file
- **Actions**:
    - Configure build scripts and MTA build.
    - Configure unit, integration, and E2E tests.

### Phase 2: Pipeline Implementation
- **Goal**: Implement the CI/CD pipeline using GitHub Actions, Jenkins, or SAP CI/CD service.
- **Agents**: `project-operations-specialist`
- **Skills**: github-actions-ci
- **Tools**: write_to_file
- **Actions**:
    - Configure GitHub Actions (or alternative service).

### Phase 3: Transport & Deployment Management
- **Goal**: Orchestrate transports and deployment to SAP BTP or On-Premise systems.
- **Agents**: `project-operations-specialist`
- **Skills**: committing-releases
- **Tools**: sap-transport-management-service
- **Actions**:
    - Configure transport requests and validation.
    - Configure BTP or On-Premise deployment.

### Phase 4: Notification & Monitoring
- **Goal**: Establish feedback loops with notifications and performance logging-and-monitoring.
- **Agents**: `project-operations-specialist`
- **Skills**: logging-and-monitoring
- **Tools**: slack-webhooks, prometheus
- **Actions**:
    - Configure pipeline notifications and deployment logging-and-monitoring.


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
