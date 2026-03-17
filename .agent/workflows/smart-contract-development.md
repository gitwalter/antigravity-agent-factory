---
agents:
- blockchain-guru-specialist
- workflow-quality-specialist
blueprints:
- universal
description: Antigravity workflow for smart-contract-development. Standardized for
  IDX Visual Editor.
domain: universal
name: smart-contract-development
steps:
- actions:
  - '**Agents**: `blockchain-guru-specialist`'
  - '**Actions**:'
  - Map out state variables and access control lists (ACL).
  agents:
  - blockchain-guru-specialist
  goal: Define the contract logic, state variables, and access controls for secure
    decentralized logic.
  name: Architecture & Security Design
  skills:
  - securing-ai-systems
  - designing-ai-systems
  tools:
  - mcp_memory_search_nodes
- actions:
  - '**Agents**: `blockchain-guru-specialist`'
  - '**Actions**:'
  - Implement Solidity contracts.
  - Write and execute unit tests using Foundry or Hardhat.
  agents:
  - blockchain-guru-specialist
  goal: Implement Solidity contracts and verify logic in isolation with high coverage.
  name: Implementation & Unit Testing
  skills:
  - securing-ai-systems
  - testing-agents
  tools:
  - write_to_file
  - foundry-cli
  - hardhat-cli
- actions:
  - '**Agents**: `workflow-quality-specialist`'
  - '**Actions**:'
  - Run static analysis (Slither/Mythril).
  - Perform gas benchmarking and optimization refactoring.
  agents:
  - workflow-quality-specialist
  goal: Minimize operational costs and identify common vulnerabilities using automated
    tools.
  name: Static Analysis & Gas Optimization
  skills:
  - securing-ai-systems
  - securing-ai-systems
  tools:
  - slither-cli
  - mythril-cli
- actions:
  - '**Agents**: `blockchain-guru-specialist`, `workflow-quality-specialist`'
  - '**Actions**:'
  - Conduct internal security audit.
  - Deploy to Sepolia/Goerli for integration testing-agents.
  - '**Security-First**: Always use OpenZeppelin contracts for standard functionality.'
  - '**Testing**: Maintain 100% branch coverage for critical financial logic.'
  - '**Upgradability**: Carefully design for upgradability using proxy patterns if
    necessary.'
  - '`deployment-workflow.md` - Handles the cross-chain deployment logic.'
  - '`security-audit-workflow.md` - Deep dive into security verification.'
  - '"Execute securing-ai-systems.md"'
  agents:
  - blockchain-guru-specialist
  - workflow-quality-specialist
  goal: Final security verification and integration testing-agents on public testnets.
  name: Auditing & Testnet Deployment
  skills:
  - securing-ai-systems
  - deployment-workflow
  tools:
  - foundry-cli
  - gnosis-safe-ui
tags: []
type: sequential
version: 2.0.0
---
# Smart Contract Development Workflow

**Version:** 1.0.0

## Overview
Antigravity workflow for secure development of blockchain smart contracts using modern toolchains. Standardized for IDX Visual Editor.

## Trigger Conditions
- New requirement for decentralized business logic on EVM-compatible chains.
- Need to implement new smart contract features with security-first principles.
- User request: `/smart-contract-development`.

**Trigger Examples:**
- "Develop a new 'Multi-Sig Wallet' smart contract following the architecture design phase."
- "Implement a 'Liquidity Provider' contract with Foundry unit tests."

## Phases

### 1. Architecture & Security Design
- **Goal**: Define the contract logic, state variables, and access controls for secure decentralized logic.
- **Agents**: `blockchain-guru-specialist`
- **Skills**: securing-ai-systems, designing-ai-systems
- **Tools**: mcp_memory_search_nodes
- **Agents**: `blockchain-guru-specialist`
- **Actions**:
- Map out state variables and access control lists (ACL).

### 2. Implementation & Unit Testing
- **Goal**: Implement Solidity contracts and verify logic in isolation with high coverage.
- **Agents**: `blockchain-guru-specialist`
- **Skills**: securing-ai-systems, testing-agents
- **Tools**: write_to_file, foundry-cli, hardhat-cli
- **Agents**: `blockchain-guru-specialist`
- **Actions**:
- Implement Solidity contracts.
- Write and execute unit tests using Foundry or Hardhat.

### 3. Static Analysis & Gas Optimization
- **Goal**: Minimize operational costs and identify common vulnerabilities using automated tools.
- **Agents**: `workflow-quality-specialist`
- **Skills**: securing-ai-systems, securing-ai-systems
- **Tools**: slither-cli, mythril-cli
- **Agents**: `workflow-quality-specialist`
- **Actions**:
- Run static analysis (Slither/Mythril).
- Perform gas benchmarking and optimization refactoring.

### 4. Auditing & Testnet Deployment
- **Goal**: Final security verification and integration testing-agents on public testnets.
- **Agents**: `blockchain-guru-specialist`, `workflow-quality-specialist`
- **Skills**: securing-ai-systems, deployment-workflow
- **Tools**: foundry-cli, gnosis-safe-ui
- **Agents**: `blockchain-guru-specialist`, `workflow-quality-specialist`
- **Actions**:
- Conduct internal security audit.
- Deploy to Sepolia/Goerli for integration testing-agents.
- **Security-First**: Always use OpenZeppelin contracts for standard functionality.
- **Testing**: Maintain 100% branch coverage for critical financial logic.
- **Upgradability**: Carefully design for upgradability using proxy patterns if necessary.
- `deployment-workflow.md` - Handles the cross-chain deployment logic.
- `security-audit-workflow.md` - Deep dive into security verification.
- "Execute securing-ai-systems.md"
