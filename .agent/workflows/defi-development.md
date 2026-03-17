---
agents:
- blockchain-guru-specialist
- system-architecture-specialist
- workflow-quality-specialist
- project-operations-specialist
blueprints:
- universal
description: Antigravity workflow for defi-development. Standardized for IDX Visual
  Editor.
domain: universal
name: defi-development
steps:
- actions:
  - '**Agents**: `blockchain-guru-specialist`, `system-architecture-specialist`'
  - '**Actions**:'
  - Design mechanisms and model economic risks/oracles.
  agents:
  - blockchain-guru-specialist
  - system-architecture-specialist
  goal: Define logical mechanisms (AMM, Lending) and risk management parameters.
  name: Mechanism & Risk Design
  skills:
  - defi-development
  - designing-ai-systems
  tools:
  - mcp_memory_search_nodes
  - python-interpreter
- actions:
  - '**Agents**: `blockchain-guru-specialist`'
  - '**Actions**:'
  - Implement core logic and oracle integrations.
  agents:
  - blockchain-guru-specialist
  goal: Implement core financial logic and integrated external services (Oracles).
  name: Core Logic Implementation
  skills:
  - defi-development
  - securing-ai-systems
  tools:
  - write_to_file
  - foundry-cli
- actions:
  - '**Agents**: `blockchain-guru-specialist`, `workflow-quality-specialist`'
  - '**Actions**:'
  - Execute economic simulations and verify logic through tests.
  agents:
  - blockchain-guru-specialist
  - workflow-quality-specialist
  goal: Run economic simulations and comprehensive unit/integration tests.
  name: Simulation & Testing
  skills:
  - testing-agents
  - defi-development
  tools:
  - echidna-cli
  - foundry-cli
- actions:
  - '**Agents**: `blockchain-guru-specialist`, `project-operations-specialist`'
  - '**Actions**:'
  - Prepare audit artifacts and initialize governance protocols.
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
  goal: Prepare for security audits and set up governance structures.
  name: Audit & Launch Governance
  skills:
  - securing-ai-systems
  - committing-releases
  tools:
  - gnosis-safe-ui
  - multi-sig-controller
tags: []
type: sequential
version: 2.0.0
---
# DeFi Development

**Version:** 1.0.0

## Overview
Antigravity workflow for decentralized finance (DeFi) development. Standardized for IDX Visual Editor.

## Trigger Conditions
- Strategic decision to build or upgrade a DeFi protocol component.
- Economic risk modeling or smart contract implementation required.
- User request: `/defi-development`.

**Trigger Examples:**
- "Design a new AMM pool for the protocol."
- "Implement the lending logic for the 'Flash Loan' feature."

## Phases

### 1. Mechanism & Risk Design
- **Goal**: Define logical mechanisms (AMM, Lending) and risk management parameters.
- **Agents**: `blockchain-guru-specialist`, `system-architecture-specialist`
- **Skills**: defi-development, designing-ai-systems
- **Tools**: mcp_memory_search_nodes, python-interpreter
- **Agents**: `blockchain-guru-specialist`, `system-architecture-specialist`
- **Actions**:
- Design mechanisms and model economic risks/oracles.

### 2. Core Logic Implementation
- **Goal**: Implement core financial logic and integrated external services (Oracles).
- **Agents**: `blockchain-guru-specialist`
- **Skills**: defi-development, securing-ai-systems
- **Tools**: write_to_file, foundry-cli
- **Agents**: `blockchain-guru-specialist`
- **Actions**:
- Implement core logic and oracle integrations.

### 3. Simulation & Testing
- **Goal**: Run economic simulations and comprehensive unit/integration tests.
- **Agents**: `blockchain-guru-specialist`, `workflow-quality-specialist`
- **Skills**: testing-agents, defi-development
- **Tools**: echidna-cli, foundry-cli
- **Agents**: `blockchain-guru-specialist`, `workflow-quality-specialist`
- **Actions**:
- Execute economic simulations and verify logic through tests.

### 4. Audit & Launch Governance
- **Goal**: Prepare for security audits and set up governance structures.
- **Agents**: `blockchain-guru-specialist`, `project-operations-specialist`
- **Skills**: securing-ai-systems, committing-releases
- **Tools**: gnosis-safe-ui, multi-sig-controller
- **Agents**: `blockchain-guru-specialist`, `project-operations-specialist`
- **Actions**:
- Prepare audit artifacts and initialize governance protocols.
- Is the requirement clear?
- Are the tests passing?
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
