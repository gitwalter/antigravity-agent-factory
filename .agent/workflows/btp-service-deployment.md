---
description: End-to-end workflow for deploying SAP applications to SAP Business Technology
  Platform (BTP). Covers build configurat...
version: 1.0.0
tags:
- btp
- service
- deployment
- standardized
---


# Btp Service Deployment

End-to-end workflow for deploying SAP applications to SAP Business Technology Platform (BTP). Covers build configuration, service bindings, Cloud Foundry/Kyma deployment, and logging-and-monitoring setup.

**Version:** 1.0.0
**Created:** 2026-02-09
**Applies To:** sap-systems-specialist, btp-deployment

## Trigger Conditions

This workflow is activated when:

- Deploying CAP application to BTP
- Deploying RAP extension to BTP ABAP
- Setting up BTP services and bindings
- Configuring CI/CD for BTP

**Trigger Examples:**
- "Deploy my CAP application to BTP Cloud Foundry"
- "Set up XSUAA for my application"
- "Configure destination service for on-premise connectivity"
- "Deploy to BTP Kyma runtime"

## Phases

### Phase 1: Environment Readiness
- **Goal**: Verify BTP subaccount settings, entitlements, and cloud foundry/kyma space.
- **Agents**: `project-operations-specialist`
- **Skills**: deploying-to-btp
- **Tools**: cf-cli, btp-cli
- **Actions**:
    - Check entitlements and space configuration.

### Phase 2: Build & Packaging
- **Goal**: Build the application artifacts and package them for deployment.
- **Agents**: `project-operations-specialist`
- **Skills**: deploying-to-btp
- **Tools**: mta-tool, npm
- **Actions**:
    - Run MTA build and package service artifacts.

### Phase 3: Deployment Execution
- **Goal**: Deploy the packaged artifacts to the BTP environment.
- **Agents**: `project-operations-specialist`
- **Skills**: deploying-to-btp
- **Tools**: cf-deploy, helm
- **Actions**:
    - Deploy MTA or Helm charts to BTP.

### Phase 4: Verification & Connectivity
- **Goal**: Verify service health and establish connectivity (Destination, Cloud Connector).
- **Agents**: `workflow-quality-specialist`, `project-operations-specialist`
- **Skills**: verifying-artifact-structures, deploying-to-btp
- **Tools**: cf-apps, sap-connectivity-service
- **Actions**:
    - Verify app status and configure destinations.


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
