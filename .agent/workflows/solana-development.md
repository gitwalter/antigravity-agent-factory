---
description: Solana program development with Anchor framework. Covers program design,
  instruction implementation, testing-agents, and dep...
version: 1.0.0
tags:
- solana
- development
- standardized
---


# Solana Development

Solana program development with Anchor framework. Covers program design, instruction implementation, testing-agents, and deployment to devnet/mainnet.

**Version:** 1.0.0
**Created:** 2026-02-10
**Applies To:** solana-rust, anchor

## Trigger Conditions

This workflow is activated when:

- Solana program development needed
- Anchor program requested
- SPL-compatible program
- On-chain program for Solana

**Trigger Examples:**
- "Build a Solana program with Anchor"
- "Create an Anchor program for token staking"
- "Develop a Solana NFT program"
- "Implement a Solana DEX program"

## Phases

### Phase 1: Program Instruction & Account Design
- **Goal**: Define program instructions and state account structures for Solana.
- **Agents**: `blockchain-guru-specialist`
- **Skills**: solana-development, designing-ai-systems
- **Tools**: mcp_memory_search_nodes
- **Actions**:
    - Map instructions and design account layout for PDAs.

### Phase 2: Implementation & Security Validation
- **Goal**: Scaffold program with Anchor and implement secure logic.
- **Agents**: `blockchain-guru-specialist`
- **Skills**: solana-development
- **Tools**: anchor-cli, cargo
- **Actions**:
    - Scaffold program and implement Anchor-based instructions.
    - Apply security constraints and validations.

### Phase 3: Testing & Devnet Deployment
- **Goal**: Execute unit/integration tests and deploy to devnet for verification.
- **Agents**: `blockchain-guru-specialist`, `workflow-quality-specialist`
- **Skills**: testing-agents, solana-development
- **Tools**: anchor-test, solana-cli
- **Actions**:
    - Run unit and integration tests.
    - Deploy to Solana Devnet.

### Phase 4: Client & Documentation
- **Goal**: Generate client-side libraries and document program usage.
- **Agents**: `blockchain-guru-specialist`, `knowledge-operations-specialist`
- **Skills**: generating-documentation, solana-development
- **Tools**: anchor-build-ts, write_to_file
- **Actions**:
    - Generate TypeScript client and update documentation.


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
