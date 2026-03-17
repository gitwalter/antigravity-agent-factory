---
agents:
- blockchain-guru-specialist
- system-architecture-specialist
- project-operations-specialist
blueprints:
- universal
description: Antigravity workflow for deployment-workflow. Standardized for IDX Visual
  Editor.
domain: universal
name: deployment-workflow
steps:
- actions:
  - '**Agents**: `project-operations-specialist`'
  - '**Actions**:'
  - Run build commands and verify metadata integrity.
  agents:
  - project-operations-specialist
  goal: Verify build artifacts and ensure environment variables are correctly configured.
  name: Build & Environment Verification
  skills:
  - deployment-workflow
  - cicd-pipeline
  tools:
  - cargo
  - foundry-cli
  - shell-execute
- actions:
  - '**Agents**: `blockchain-guru-specialist`'
  - '**Actions**:'
  - Deploy to Goerli/Sepolia or Solana Devnet.
  - Run post-deployment smoke tests.
  agents:
  - blockchain-guru-specialist
  goal: Deploy artifacts to testnet/devnet and execute smoke tests.
  name: Testnet Deployment & smoke Testing
  skills:
  - deployment-workflow
  - testing-agents
  tools:
  - foundry-cli
  - solana-cli
  - anchor-cli
- actions:
  - '**Agents**: `system-architecture-specialist`, `project-operations-specialist`'
  - '**Actions**:'
  - Manage governance signatures and finalize sign-off.
  agents:
  - system-architecture-specialist
  - project-operations-specialist
  goal: Finalize governance requirements and obtain multi-sig sign-offs.
  name: Governance & Sign-off
  skills:
  - committing-releases
  - deployment-workflow
  tools:
  - gnosis-safe-ui
  - multi-sig-controller
- actions:
  - '**Agents**: `blockchain-guru-specialist`, `project-operations-specialist`'
  - '**Actions**:'
  - Execute mainnet deployment.
  - Verify block explorer status and logging-and-monitoring alerts.
  - Is the requirement clear?
  - Are the tests passing?
  - '"Execute this workflow."'
  - '**Axiomatic Alignment**: Ensure Truth, Beauty, and Love.'
  - '**Memory First**: Check context before execution.'
  - '**Verifiability**: Document every step.'
  - '[workflow-standard.md](file:///.agent/rules/workflow-standard.md)'
  agents:
  - blockchain-guru-specialist
  - project-operations-specialist
  goal: Execute mainnet deployment and initialize real-time logging-and-monitoring.
  name: Mainnet Execution & Monitoring
  skills:
  - deployment-workflow
  - logging-and-monitoring
  tools:
  - foundry-cli
  - etherscan-api
  - datadog-agent
tags: []
type: sequential
version: 2.0.0
---
# Deployment Workflow

**Version:** 1.0.0

## Overview
Antigravity workflow for deployment-workflow across testnet and mainnet environments. Standardized for IDX Visual Editor.

## Trigger Conditions
- Successful completion of the CI/CD pipeline.
- Governance sign-off obtained for protocol deployment.
- User request: `/deployment-workflow`.

**Trigger Examples:**
- "Deploy the latest build to the Goerli testnet."
- "Execute the mainnet deployment for the v1.2 version."

## Phases

### 1. Build & Environment Verification
- **Goal**: Verify build artifacts and ensure environment variables are correctly configured.
- **Agents**: `project-operations-specialist`
- **Skills**: deployment-workflow, cicd-pipeline
- **Tools**: cargo, foundry-cli, shell-execute
- **Agents**: `project-operations-specialist`
- **Actions**:
- Run build commands and verify metadata integrity.

### 2. Testnet Deployment & smoke Testing
- **Goal**: Deploy artifacts to testnet/devnet and execute smoke tests.
- **Agents**: `blockchain-guru-specialist`
- **Skills**: deployment-workflow, testing-agents
- **Tools**: foundry-cli, solana-cli, anchor-cli
- **Agents**: `blockchain-guru-specialist`
- **Actions**:
- Deploy to Goerli/Sepolia or Solana Devnet.
- Run post-deployment smoke tests.

### 3. Governance & Sign-off
- **Goal**: Finalize governance requirements and obtain multi-sig sign-offs.
- **Agents**: `system-architecture-specialist`, `project-operations-specialist`
- **Skills**: committing-releases, deployment-workflow
- **Tools**: gnosis-safe-ui, multi-sig-controller
- **Agents**: `system-architecture-specialist`, `project-operations-specialist`
- **Actions**:
- Manage governance signatures and finalize sign-off.

### 4. Mainnet Execution & Monitoring
- **Goal**: Execute mainnet deployment and initialize real-time logging-and-monitoring.
- **Agents**: `blockchain-guru-specialist`, `project-operations-specialist`
- **Skills**: deployment-workflow, logging-and-monitoring
- **Tools**: foundry-cli, etherscan-api, datadog-agent
- **Agents**: `blockchain-guru-specialist`, `project-operations-specialist`
- **Actions**:
- Execute mainnet deployment.
- Verify block explorer status and logging-and-monitoring alerts.
- Is the requirement clear?
- Are the tests passing?
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
