---
agents:
- blockchain-guru-specialist
- workflow-quality-specialist
- knowledge-operations-specialist
blueprints:
- universal
description: Antigravity workflow for solana-development. Standardized for IDX Visual
  Editor.
domain: universal
name: solana-development
steps:
- actions:
  - '**Agents**: `blockchain-guru-specialist`'
  - '**Actions**:'
  - Map instructions and design account layout for PDAs.
  agents:
  - blockchain-guru-specialist
  goal: Define program instructions and state account structures for Solana.
  name: Program Instruction & Account Design
  skills:
  - solana-development
  - designing-ai-systems
  tools:
  - mcp_memory_search_nodes
- actions:
  - '**Agents**: `blockchain-guru-specialist`'
  - '**Actions**:'
  - Scaffold program and implement Anchor-based instructions.
  - Apply security constraints and validations.
  agents:
  - blockchain-guru-specialist
  goal: Scaffold program with Anchor and implement secure logic.
  name: Implementation & Security Validation
  skills:
  - solana-development
  tools:
  - anchor-cli
  - cargo
- actions:
  - '**Agents**: `blockchain-guru-specialist`, `workflow-quality-specialist`'
  - '**Actions**:'
  - Run unit and integration tests.
  - Deploy to Solana Devnet.
  agents:
  - blockchain-guru-specialist
  - workflow-quality-specialist
  goal: Execute unit/integration tests and deploy to devnet for verification.
  name: Testing & Devnet Deployment
  skills:
  - testing-agents
  - solana-development
  tools:
  - anchor-test
  - solana-cli
- actions:
  - '**Agents**: `blockchain-guru-specialist`, `knowledge-operations-specialist`'
  - '**Actions**:'
  - Generate TypeScript client and update documentation.
  - Is the requirement clear?
  - Are the tests passing?
  - '"Execute this workflow."'
  - '**Axiomatic Alignment**: Ensure Truth, Beauty, and Love.'
  - '**Memory First**: Check context before execution.'
  - '**Verifiability**: Document every step.'
  - '[workflow-standard.md](file:///.agent/rules/workflow-standard.md)'
  agents:
  - blockchain-guru-specialist
  - knowledge-operations-specialist
  goal: Generate client-side libraries and document program usage.
  name: Client & Documentation
  skills:
  - generating-documentation
  - solana-development
  tools:
  - anchor-build-ts
  - write_to_file
tags: []
type: sequential
version: 1.0.0
---

# Solana Program Development

**Version:** 1.0.0

## Overview
Antigravity workflow for developing secure Solana programs (smart contracts) using the Anchor framework. Standardized for IDX Visual Editor.

## Trigger Conditions
- Requirement for building decentralized applications (dApps) on the Solana blockchain.
- Need to implement new program instructions or account layouts.
- User request: `/solana-development`.

**Trigger Examples:**
- "Develop a Solana program for an 'On-Chain Voting System' using Anchor."
- "Implement a PDAs-based account structure for the 'Asset Vault' program."

## Phases

### 1. Program Instruction & Account Design
- **Goal**: Define program instructions and state account structures for Solana.
- **Agents**: `blockchain-guru-specialist`
- **Skills**: solana-development, designing-ai-systems
- **Tools**: mcp_memory_search_nodes
- **Agents**: `blockchain-guru-specialist`
- **Actions**:
- Map instructions and design account layout for PDAs.

### 2. Implementation & Security Validation
- **Goal**: Scaffold program with Anchor and implement secure logic.
- **Agents**: `blockchain-guru-specialist`
- **Skills**: solana-development
- **Tools**: anchor-cli, cargo
- **Agents**: `blockchain-guru-specialist`
- **Actions**:
- Scaffold program and implement Anchor-based instructions.
- Apply security constraints and validations.

### 3. Testing & Devnet Deployment
- **Goal**: Execute unit/integration tests and deploy to devnet for verification.
- **Agents**: `blockchain-guru-specialist`, `workflow-quality-specialist`
- **Skills**: testing-agents, solana-development
- **Tools**: anchor-test, solana-cli
- **Agents**: `blockchain-guru-specialist`, `workflow-quality-specialist`
- **Actions**:
- Run unit and integration tests.
- Deploy to Solana Devnet.

### 4. Client & Documentation
- **Goal**: Generate client-side libraries and document program usage.
- **Agents**: `blockchain-guru-specialist`, `knowledge-operations-specialist`
- **Skills**: generating-documentation, solana-development
- **Tools**: anchor-build-ts, write_to_file
- **Agents**: `blockchain-guru-specialist`, `knowledge-operations-specialist`
- **Actions**:
- Generate TypeScript client and update documentation.
- Is the requirement clear?
- Are the tests passing?
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
