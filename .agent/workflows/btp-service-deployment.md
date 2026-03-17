---
agents:
- workflow-quality-specialist
- project-operations-specialist
blueprints:
- universal
description: Antigravity workflow for btp-service-deployment. Standardized for IDX
  Visual Editor.
domain: universal
name: btp-service-deployment
steps:
- actions:
  - '**Agents**: `project-operations-specialist`'
  - '**Actions**:'
  - Check entitlements and space configuration.
  agents:
  - project-operations-specialist
  goal: Verify BTP subaccount settings, entitlements, and cloud foundry/kyma space.
  name: Environment Readiness
  skills:
  - deploying-to-btp
  tools:
  - cf-cli
  - btp-cli
- actions:
  - '**Agents**: `project-operations-specialist`'
  - '**Actions**:'
  - Run MTA build and package service artifacts.
  agents:
  - project-operations-specialist
  goal: Build the application artifacts and package them for deployment.
  name: Build & Packaging
  skills:
  - deploying-to-btp
  tools:
  - mta-tool
  - npm
- actions:
  - '**Agents**: `project-operations-specialist`'
  - '**Actions**:'
  - Deploy MTA or Helm charts to BTP.
  agents:
  - project-operations-specialist
  goal: Deploy the packaged artifacts to the BTP environment.
  name: Deployment Execution
  skills:
  - deploying-to-btp
  tools:
  - cf-deploy
  - helm
- actions:
  - '**Agents**: `workflow-quality-specialist`, `project-operations-specialist`'
  - '**Actions**:'
  - Verify app status and configure destinations.
  - Is the requirement clear?
  - Are the tests passing?
  - '"Execute this workflow."'
  - '**Axiomatic Alignment**: Ensure Truth, Beauty, and Love.'
  - '**Memory First**: Check context before execution.'
  - '**Verifiability**: Document every step.'
  - '[workflow-standard.md](file:///.agent/rules/workflow-standard.md)'
  agents:
  - workflow-quality-specialist
  - project-operations-specialist
  goal: Verify service health and establish connectivity (Destination, Cloud Connector).
  name: Verification & Connectivity
  skills:
  - verifying-artifact-structures
  - deploying-to-btp
  tools:
  - cf-apps
  - sap-connectivity-service
tags: []
type: sequential
version: 2.0.0
---
# BTP Service Deployment

**Version:** 1.0.0

## Overview
Antigravity workflow for BTP service deployment. Standardized for IDX Visual Editor.

## Trigger Conditions
- Application code ready for deployment to SAP Business Technology Platform.
- Infrastructure or connectivity changes requiring redeployment.
- User request: `/btp-service-deployment`.

**Trigger Examples:**
- "Deploy the CAP service to BTP."
- "Package and push the MTA to the dev subaccount."

## Phases

### 1. Environment Readiness
- **Goal**: Verify BTP subaccount settings, entitlements, and cloud foundry/kyma space.
- **Agents**: `project-operations-specialist`
- **Skills**: deploying-to-btp
- **Tools**: cf-cli, btp-cli
- **Agents**: `project-operations-specialist`
- **Actions**:
- Check entitlements and space configuration.

### 2. Build & Packaging
- **Goal**: Build the application artifacts and package them for deployment.
- **Agents**: `project-operations-specialist`
- **Skills**: deploying-to-btp
- **Tools**: mta-tool, npm
- **Agents**: `project-operations-specialist`
- **Actions**:
- Run MTA build and package service artifacts.

### 3. Deployment Execution
- **Goal**: Deploy the packaged artifacts to the BTP environment.
- **Agents**: `project-operations-specialist`
- **Skills**: deploying-to-btp
- **Tools**: cf-deploy, helm
- **Agents**: `project-operations-specialist`
- **Actions**:
- Deploy MTA or Helm charts to BTP.

### 4. Verification & Connectivity
- **Goal**: Verify service health and establish connectivity (Destination, Cloud Connector).
- **Agents**: `workflow-quality-specialist`, `project-operations-specialist`
- **Skills**: verifying-artifact-structures, deploying-to-btp
- **Tools**: cf-apps, sap-connectivity-service
- **Agents**: `workflow-quality-specialist`, `project-operations-specialist`
- **Actions**:
- Verify app status and configure destinations.
- Is the requirement clear?
- Are the tests passing?
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
