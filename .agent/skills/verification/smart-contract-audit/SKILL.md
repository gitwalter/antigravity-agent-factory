---
name: smart-contract-audit
version: 1.0.0
type: skill
description: Skills for performing security audits and gas optimization checks on smart contracts.
category: verification
agents:
- blockchain-guru-specialist
knowledge:
- solidity-patterns.json
tools:
- name: run_audit
  type: factory
  description: Runs automated security audit tools (e.g., Slither) on a smart contract.
---

# Smart Contract Audit Skill

## When to Use
Use this skill before deploying any smart contract to a testnet or mainnet, focusing on security vulnerabilities and gas optimization.

## Prerequisites
- Compiled smart contract artifacts (e.g., ABI, Bytecode).
- Validated `solidity-patterns.json` Knowledge Item.
- Static analysis tools (like Slither or Mythril) installed in the environment.

## Process
1. **Static Analysis**: Run automated scanners using the `run_audit` tool.
2. **Manual Review**: Critically examine logic involving value transfers and state changes.
3. **Gas Optimization**: Identify areas to reduce computational cost.
4. **Report Generation**: Compile all findings into a structured audit artifact.

## Best Practices
- **Security-First**: Prioritize resolving reentrancy and arithmetic overflow vulnerabilities.
- **Layered Auditing**: Combine automated tools with manual specialized review.
- **Immutable Path**: Never deploy a contract that hasn't cleared the audit gate.
