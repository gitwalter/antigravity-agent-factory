---
name: smart-contract-development
description: Web3 workflow for designing, implementing, and auditing smart contracts on EVM chains.
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
    description: Deploy to Rinkeby, Goerli, or Sepolia for integration testing.
  - name: Mainnet Release
    description: Final deployment to Ethereum, Polygon, or other mainnets.
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

### 1. Architecture & Security Design
Define the contract's economic and logic model.
- **Agent**: `blockchain-guru-specialist`
- **Action**: Map out state variables and access control lists.

### 2. Implementation & Unit Testing
Write code and verify logic in isolation.
- **Action**: Implement Solidity contracts and write tests using Foundry.

### 3. Analysis & Optimization
Minimize risk and operational costs.
- **Action**: Run static analysis and perform gas benchmarking.

### 4. Auditing & Release
Final security verification and mainnet launch.
- **Action**: Conduct security audits and deploy to testnet before mainnet.

## Best Practices
- **Security-First**: Always use OpenZeppelin contracts for standard functionality.
- **Testing**: Maintain 100% branch coverage for critical financial logic.
- **Upgradability**: Carefully design for upgradability using proxy patterns if necessary.

## Related Workflows
- `deployment-workflow.md` - Handles the cross-chain deployment logic.
- `security-audit-workflow.md` - Deep dive into security verification.
