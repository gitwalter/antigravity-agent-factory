---
name: securing-ai-systems
description: Web3 workflow for designing, implementing, and auditing smart contracts
  on EVM chains.
version: 1.0.0
type: iterative
domain: blockchain
agents:
- blockchain-guru-specialist
blueprints:
- defi-protocol
steps:
- name: Architecture Design
  description: Define contract logic, state variables, and access controls.
- name: Implementation
  description: Write Solidity code following security best practices.
- name: Unit Testing
  description: Develop comprehensive test suite using Foundry or Hardhat.
- name: Static Analysis
  description: Run Slither, Mythril, or other static analysis tools.
- name: Gas Optimization
  description: Refactor code to minimize gas consumption.
- name: Formal Verification
  description: Perform formal verification for critical logic components.
- name: Deployment Plan
  description: Prepare migration scripts and deployment configuration.
- name: Security Audit
  description: Conduct internal and third-party security audits.
- name: Testnet Deployment
  description: Deploy to Rinkeby, Goerli, or Sepolia for integration testing-agents.
- name: Mainnet Release
  description: Final deployment to Ethereum, Polygon, or other mainnets.
tags:
- smart
- contract
- development
- standardized
---


# Smart Contract Development Workflow

**Version:** 1.0.0

**Goal:** Secure and efficient implementation of decentralized logic on EVM-compatible blockchains.

## Trigger Conditions
- New DeFi protocol or smart contract requirement.
- Security patch or upgrade needed for existing contracts.
- Preparation for a new mainnet deployment.

**Trigger Examples:**
- "Design a new AMM pool contract following Uniswap V2 patterns."
- "Implement an ERC-20 token with governance capabilities."
- "Run security analysis using Slither on the staking contract."
- "Deploy the audited contracts to Sepolia testnet."

## Phases

### Phase 1: Architecture & Security Design
- **Goal**: Define the contract logic, state variables, and access controls for secure decentralized logic.
- **Agents**: `blockchain-guru-specialist`
- **Skills**: securing-ai-systems, designing-ai-systems
- **Tools**: mcp_memory_search_nodes
- **Actions**:
    - Map out state variables and access control lists (ACL).

### Phase 2: Implementation & Unit Testing
- **Goal**: Implement Solidity contracts and verify logic in isolation with high coverage.
- **Agents**: `blockchain-guru-specialist`
- **Skills**: securing-ai-systems, testing-agents
- **Tools**: write_to_file, foundry-cli, hardhat-cli
- **Actions**:
    - Implement Solidity contracts.
    - Write and execute unit tests using Foundry or Hardhat.

### Phase 3: Static Analysis & Gas Optimization
- **Goal**: Minimize operational costs and identify common vulnerabilities using automated tools.
- **Agents**: `workflow-quality-specialist`
- **Skills**: securing-ai-systems, securing-ai-systems
- **Tools**: slither-cli, mythril-cli
- **Actions**:
    - Run static analysis (Slither/Mythril).
    - Perform gas benchmarking and optimization refactoring.

### Phase 4: Auditing & Testnet Deployment
- **Goal**: Final security verification and integration testing-agents on public testnets.
- **Agents**: `blockchain-guru-specialist`, `workflow-quality-specialist`
- **Skills**: securing-ai-systems, deployment-workflow
- **Tools**: foundry-cli, gnosis-safe-ui
- **Actions**:
    - Conduct internal security audit.
    - Deploy to Sepolia/Goerli for integration testing-agents.

## Best Practices
- **Security-First**: Always use OpenZeppelin contracts for standard functionality.
- **Testing**: Maintain 100% branch coverage for critical financial logic.
- **Upgradability**: Carefully design for upgradability using proxy patterns if necessary.

## Related Workflows
- `deployment-workflow.md` - Handles the cross-chain deployment logic.
- `security-audit-workflow.md` - Deep dive into security verification.


## Trigger Examples
- "Execute securing-ai-systems.md"
