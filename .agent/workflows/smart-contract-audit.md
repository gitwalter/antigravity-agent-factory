---
agents:
- blockchain-guru-specialist
- workflow-quality-specialist
- knowledge-operations-specialist
blueprints:
- universal
description: Antigravity workflow for smart-contract-audit. Standardized for IDX Visual
  Editor.
domain: universal
name: smart-contract-audit
steps:
- actions:
  - '**Agents**: `workflow-quality-specialist`'
  - '**Actions**:'
  - Identify target contracts and run initial security scanners.
  agents:
  - workflow-quality-specialist
  goal: Define audit scope and prepare the detection environment.
  name: Scope Definition & Environment Setup
  skills:
  - securing-ai-systems
  - securing-ai-systems
  tools:
  - slither-cli
  - mythril-cli
- actions:
  - '**Agents**: `blockchain-guru-specialist`'
  - '**Actions**:'
  - Review ACLs and external integrations for logic flaws.
  agents:
  - blockchain-guru-specialist
  goal: Manually verify access control lists and complex financial logic.
  name: Access Control & Business Logic Review
  skills:
  - securing-ai-systems
  tools:
  - mcp_memory_search_nodes
- actions:
  - '**Agents**: `workflow-quality-specialist`'
  - '**Actions**:'
  - Conduct gas profiling and analyze test coverage/branch targets.
  agents:
  - workflow-quality-specialist
  goal: Analyze gas efficiency and test coverage for critical logic.
  name: Gas Profiling & Test Suite Analysis
  skills:
  - securing-ai-systems
  - testing-agents
  tools:
  - foundry-cli
  - echidna-cli
- actions:
  - '**Agents**: `workflow-quality-specialist`, `knowledge-operations-specialist`'
  - '**Actions**:'
  - Generate audit report and verify remediation findings.
  - Is the requirement clear?
  - Are the tests passing?
  - '"Execute this workflow."'
  - '**Axiomatic Alignment**: Ensure Truth, Beauty, and Love.'
  - '**Memory First**: Check context before execution.'
  - '**Verifiability**: Document every step.'
  - '[workflow-standard.md](file:///.agent/rules/workflow-standard.md)'
  agents:
  - workflow-quality-specialist
  - knowledge-operations-specialist
  goal: Compile findings into a high-fidelity audit report and verify fixes.
  name: Report Generation & Remediation
  skills:
  - generating-documentation
  - securing-ai-systems
  tools:
  - pdf-generator
  - write_to_file
tags: []
type: sequential
version: 2.0.0
---
# Smart Contract Audit

**Version:** 1.0.0

## Overview
Antigravity workflow specifically tailored for deep auditing of blockchain smart contracts. Standardized for IDX Visual Editor.

## Trigger Conditions
- Release of a new smart contract to mainnet or public testnet.
- Requirement for Gas optimization and vulnerability hunting in Solidity code.
- User request: `/smart-contract-audit`.

**Trigger Examples:**
- "Perform a gas profiling audit on the 'NFT Marketplace' contracts."
- "Execute a smart contract audit with focus on re-entrancy protection."

## Phases

### 1. Scope Definition & Environment Setup
- **Goal**: Define audit scope and prepare the detection environment.
- **Agents**: `workflow-quality-specialist`
- **Skills**: securing-ai-systems, securing-ai-systems
- **Tools**: slither-cli, mythril-cli
- **Agents**: `workflow-quality-specialist`
- **Actions**:
- Identify target contracts and run initial security scanners.

### 2. Access Control & Business Logic Review
- **Goal**: Manually verify access control lists and complex financial logic.
- **Agents**: `blockchain-guru-specialist`
- **Skills**: securing-ai-systems
- **Tools**: mcp_memory_search_nodes
- **Agents**: `blockchain-guru-specialist`
- **Actions**:
- Review ACLs and external integrations for logic flaws.

### 3. Gas Profiling & Test Suite Analysis
- **Goal**: Analyze gas efficiency and test coverage for critical logic.
- **Agents**: `workflow-quality-specialist`
- **Skills**: securing-ai-systems, testing-agents
- **Tools**: foundry-cli, echidna-cli
- **Agents**: `workflow-quality-specialist`
- **Actions**:
- Conduct gas profiling and analyze test coverage/branch targets.

### 4. Report Generation & Remediation
- **Goal**: Compile findings into a high-fidelity audit report and verify fixes.
- **Agents**: `workflow-quality-specialist`, `knowledge-operations-specialist`
- **Skills**: generating-documentation, securing-ai-systems
- **Tools**: pdf-generator, write_to_file
- **Agents**: `workflow-quality-specialist`, `knowledge-operations-specialist`
- **Actions**:
- Generate audit report and verify remediation findings.
- Is the requirement clear?
- Are the tests passing?
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
