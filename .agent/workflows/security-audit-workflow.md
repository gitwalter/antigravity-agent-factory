---
description: Smart contract security audit workflow covering scope definition, static
  analysis, manual review, penetration testing-agents...
version: 1.0.0
tags:
- security
- audit
- workflow
- standardized
---


# Security Audit Workflow

Smart contract security audit workflow covering scope definition, static analysis, manual review, penetration testing-agents, and reporting. Supports Ethereum/Solidity and Solana/Rust.

**Version:** 1.0.0
**Created:** 2026-02-10
**Applies To:** solidity-ethereum, solana-rust, defi-protocols

## Trigger Conditions

This workflow is activated when:

- Pre-deployment audit required
- Security review requested
- Post-audit remediation verification
- Critical vulnerability suspected

**Trigger Examples:**
- "Audit the smart contracts"
- "Security review before mainnet"
- "Verify audit findings are fixed"
- "Penetration test the protocol"

## Phases

### Phase 1: Scope & Discovery
- **Goal**: Define audit scope and prepare the detection environment.
- **Agents**: `workflow-quality-specialist`
- **Skills**: securing-ai-systems, securing-ai-systems
- **Tools**: mcp_memory_search_nodes, slither-cli
- **Actions**:
    - Define scope and discover environmental dependencies.

### Phase 2: Vulnerability Hunting & Triage
- **Goal**: Execute automated scanners and triage identified findings based on severity.
- **Agents**: `workflow-quality-specialist`
- **Skills**: securing-ai-systems
- **Tools**: slither-cli, mythril-cli
- **Actions**:
    - Run scanners and triage findings into high/medium/low severity.

### Phase 3: Manual Logic & Access Control Review
- **Goal**: Deep dive into manual review of access controls and business logic.
- **Agents**: `blockchain-guru-specialist`, `workflow-quality-specialist`
- **Skills**: securing-ai-systems, securing-ai-systems
- **Tools**: mcp_memory_search_nodes
- **Actions**:
    - Manually verify ACLs and logical flows for "rug-pull" or "re-entrancy" vectors.

### Phase 4: Reporting & Verification
- **Goal**: Generate high-fidelity audit reports and verify remediation.
- **Agents**: `workflow-quality-specialist`, `knowledge-operations-specialist`
- **Skills**: generating-documentation, committing-releases
- **Tools**: pdf-generator, safety-gate
- **Actions**:
    - Compile audit report and verify remediation findings before release.


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
