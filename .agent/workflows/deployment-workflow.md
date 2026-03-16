---
description: Blockchain deployment workflow from testnet through mainnet. Covers build
  verification, testnet deployment, mainnet p...
version: 1.0.0
tags:
- deployment
- workflow
- standardized
---


# Deployment Workflow

Blockchain deployment workflow from testnet through mainnet. Covers build verification, testnet deployment, mainnet preparation, and post-deployment verification.

**Version:** 1.0.0
**Created:** 2026-02-10
**Applies To:** solidity-ethereum, solana-rust, defi-protocols

## Trigger Conditions

This workflow is activated when:

- Deployment to testnet requested
- Mainnet deployment planned
- Post-audit deployment
- Contract upgrade

**Trigger Examples:**
- "Deploy to Goerli"
- "Deploy to Solana devnet"
- "Prepare for mainnet deployment"
- "Upgrade the contract"

## Phases

### Phase 1: Build & Environment Verification
- **Goal**: Verify build artifacts and ensure environment variables are correctly configured.
- **Agents**: `project-operations-specialist`
- **Skills**: deployment-workflow, cicd-pipeline
- **Tools**: cargo, foundry-cli, shell-execute
- **Actions**:
    - Run build commands and verify metadata integrity.

### Phase 2: Testnet Deployment & smoke Testing
- **Goal**: Deploy artifacts to testnet/devnet and execute smoke tests.
- **Agents**: `blockchain-guru-specialist`
- **Skills**: deployment-workflow, testing-agents
- **Tools**: foundry-cli, solana-cli, anchor-cli
- **Actions**:
    - Deploy to Goerli/Sepolia or Solana Devnet.
    - Run post-deployment smoke tests.

### Phase 3: Governance & Sign-off
- **Goal**: Finalize governance requirements and obtain multi-sig sign-offs.
- **Agents**: `system-architecture-specialist`, `project-operations-specialist`
- **Skills**: committing-releases, deployment-workflow
- **Tools**: gnosis-safe-ui, multi-sig-controller
- **Actions**:
    - Manage governance signatures and finalize sign-off.

### Phase 4: Mainnet Execution & Monitoring
- **Goal**: Execute mainnet deployment and initialize real-time logging-and-monitoring.
- **Agents**: `blockchain-guru-specialist`, `project-operations-specialist`
- **Skills**: deployment-workflow, logging-and-monitoring
- **Tools**: foundry-cli, etherscan-api, datadog-agent
- **Actions**:
    - Execute mainnet deployment.
    - Verify block explorer status and logging-and-monitoring alerts.


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
