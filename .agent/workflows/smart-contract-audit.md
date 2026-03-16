---
description: Comprehensive security audit workflow for smart contracts covering static
  analysis, vulnerability scanning, gas optim...
version: 1.0.0
tags:
- smart
- contract
- audit
- standardized
---


# Smart Contract Audit

Comprehensive security audit workflow for smart contracts covering static analysis, vulnerability scanning, gas optimization, and business logic review. Designed for Ethereum/Solidity and Solana/Rust ecosystems.

**Version:** 1.0.0
**Created:** 2026-02-02
**Applies To:** solidity-ethereum, solana-rust, defi-protocols

## Trigger Conditions

This workflow is activated when:

- Pre-deployment security review required
- Smart contract PR needs review
- Audit requested for DeFi protocol
- Security concern raised

**Trigger Examples:**
- "Audit the token contract"
- "Security review for the DEX"
- "Check the lending protocol for vulnerabilities"
- "Pre-mainnet audit"

## Phases

### Phase 1: Scope Definition & Environment Setup
- **Goal**: Define audit scope and prepare the detection environment.
- **Agents**: `workflow-quality-specialist`
- **Skills**: securing-ai-systems, securing-ai-systems
- **Tools**: slither-cli, mythril-cli
- **Actions**:
    - Identify target contracts and run initial security scanners.

### Phase 2: Access Control & Business Logic Review
- **Goal**: Manually verify access control lists and complex financial logic.
- **Agents**: `blockchain-guru-specialist`
- **Skills**: securing-ai-systems
- **Tools**: mcp_memory_search_nodes
- **Actions**:
    - Review ACLs and external integrations for logic flaws.

### Phase 3: Gas Profiling & Test Suite Analysis
- **Goal**: Analyze gas efficiency and test coverage for critical logic.
- **Agents**: `workflow-quality-specialist`
- **Skills**: securing-ai-systems, testing-agents
- **Tools**: foundry-cli, echidna-cli
- **Actions**:
    - Conduct gas profiling and analyze test coverage/branch targets.

### Phase 4: Report Generation & Remediation
- **Goal**: Compile findings into a high-fidelity audit report and verify fixes.
- **Agents**: `workflow-quality-specialist`, `knowledge-operations-specialist`
- **Skills**: generating-documentation, securing-ai-systems
- **Tools**: pdf-generator, write_to_file
- **Actions**:
    - Generate audit report and verify remediation findings.


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
