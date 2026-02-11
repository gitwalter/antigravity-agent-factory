# Ethereum Smart Contract Development

> **Stack:** Ethereum + Hardhat | **Level:** Fundamentals | **Duration:** 2.5 hours

## Overview

**Workshop ID:** `L1_ethereum_fundamentals`

**Technology:** Solidity with Ethereum + Hardhat (Solidity 0.8+)

## Prerequisites

**Required Knowledge:**
- Basic programming concepts (variables, functions, control flow)
- Understanding of blockchain basics (blocks, transactions, consensus)
- JavaScript/TypeScript familiarity for testing

**Required Tools:**
- Node.js 18+ installed
- npm or yarn package manager
- Code editor (VS Code recommended)
- Git for version control

## Learning Objectives

By the end of this workshop, you will be able to:

1. **Understand the Ethereum Virtual Machine (EVM) architecture, storage model, and gas mechanism** (Understand)
2. **Write basic Solidity smart contracts with state variables, functions, and events** (Apply)
3. **Use Hardhat framework for development, testing, and deployment** (Apply)
4. **Implement common token patterns including ERC20 fungible tokens and ERC721 non-fungible tokens** (Apply)
5. **Identify and apply security best practices to prevent common vulnerabilities** (Analyze)

## Workshop Timeline

| Phase | Duration |
|-------|----------|
| Concept | 30 min |
| Demo | 30 min |
| Exercise | 45 min |
| Challenge | 30 min |
| Reflection | 15 min |
| **Total** | **2.5 hours** |

## Workshop Phases

### Concept: EVM Architecture and Solidity Fundamentals

*Deep dive into how Ethereum works under the hood*

**Topics Covered:**
- EVM architecture: bytecode execution, stack machine model
- Storage model: storage slots, memory, calldata, stack
- Gas mechanism: computation costs, storage costs, gas optimization
- Account model: EOA vs Contract accounts
- Transaction lifecycle: creation, validation, execution
- Solidity basics: data types, visibility modifiers, inheritance

**Key Points:**
- Storage is persistent but expensive (20,000 gas per write)
- Memory is temporary and cheaper
- Every operation costs gas - optimization matters
- Contracts are immutable once deployed
- State changes persist across transactions

### Demo: Building an ERC20 Token

*Live coding a complete ERC20 token contract from scratch*

**Topics Covered:**
- Hardhat project setup and structure
- ERC20 standard interface
- Implementing transfer, approve, transferFrom
- Events: Transfer, Approval
- Testing with Hardhat and ethers.js
- Deploying to local network

**Key Points:**
- ERC20 is a standard interface, not an implementation
- Always emit events for state changes
- Use SafeMath or Solidity 0.8+ overflow protection
- Test both success and failure paths

### Exercise: Guided Contract Development

*Build a simple voting contract with guided steps*

**Topics Covered:**
- Create Voting contract with proposals and votes
- Implement vote casting with duplicate prevention
- Add access control for admin functions
- Write comprehensive tests

### Exercise: Testing and Debugging

*Practice writing tests and debugging failed transactions*

**Topics Covered:**
- Writing test cases with ethers.js
- Testing edge cases and error conditions
- Using Hardhat console.log for debugging
- Reading transaction receipts and events

### Challenge: Build a Mini-NFT Contract

*Apply all concepts to build a basic NFT contract*

**Topics Covered:**
- Implement ERC721 standard (mint, transfer, ownerOf)
- Add metadata URI storage
- Implement minting with unique token IDs
- Add basic access control
- Write tests for minting and transfers

### Reflection: Key Takeaways and Security Awareness

*Consolidate learning and emphasize security mindset*

**Topics Covered:**
- Summary of EVM and gas optimization
- Importance of following standards (ERC20, ERC721)
- Security best practices and common pitfalls
- Resources for continued learning and auditing

**Key Points:**
- Always validate inputs and check access controls
- Use reentrancy guards for external calls
- Prefer pull over push patterns for payments
- Test thoroughly before mainnet deployment
- Consider gas costs in contract design

## Hands-On Exercises

### Exercise: Voting Contract

Create a simple voting contract where users can vote on proposals

**Difficulty:** Medium | **Duration:** 30 minutes

**Hints:**
- Use a struct to group proposal data together
- Use mapping(address => bool) to track who has voted
- Create a modifier for admin-only functions
- Always emit events for important state changes
- Validate proposalId to prevent out-of-bounds access

**Common Mistakes to Avoid:**
- Forgetting to check if user already voted
- Not validating proposalId bounds
- Missing access control on addProposal
- Not emitting events
- Using storage instead of memory in view functions

### Exercise: Testing the Voting Contract

Write comprehensive tests for the voting contract

**Difficulty:** Medium | **Duration:** 15 minutes

**Common Mistakes to Avoid:**
- Not using connect() to test from different addresses
- Forgetting to await async calls
- Not testing error conditions
- Incorrect event assertions
- Not resetting state between tests

## Challenges

### Challenge: Build a Mini-NFT Contract

Create a basic ERC721 non-fungible token contract

**Requirements:**
- Implement ERC721 interface: mint, transfer, ownerOf, balanceOf
- Store token metadata URI for each token
- Mint function that assigns unique token IDs
- Only contract owner can mint
- Emit Transfer events on mint and transfer
- Write tests covering minting, transfers, and ownership queries

**Evaluation Criteria:**
- Contract compiles without errors
- Can mint NFTs with unique IDs
- Transfer function works correctly
- ownerOf returns correct addresses
- Access control prevents unauthorized minting
- All tests pass

**Stretch Goals:**
- Add tokenURI function that returns metadata
- Implement burn functionality
- Add approval mechanism for transfers
- Create a simple frontend to display NFTs

## Resources

**Official Documentation:**
- https://docs.soliditylang.org/
- https://hardhat.org/docs
- https://ethereum.org/en/developers/docs/

**Tutorials:**
- https://ethereum.org/en/developers/tutorials/
- https://hardhat.org/tutorial
- https://docs.openzeppelin.com/contracts

**Videos:**
- Ethereum Foundation YouTube channel
- Dapp University Solidity tutorials

## Self-Assessment

Ask yourself these questions:

- [ ] Can I explain how the EVM executes smart contracts?
- [ ] Do I understand when to use storage vs memory vs calldata?
- [ ] Can I write tests that cover both success and failure cases?
- [ ] Am I aware of common security vulnerabilities in Solidity?
- [ ] Can I estimate and optimize gas costs?

## Next Steps

**Next Workshop:** `L3_ethereum_defi`

**Practice Projects:**
- Multi-signature wallet contract
- Decentralized exchange (DEX) with liquidity pools
- Staking contract with rewards
- Governance token with voting

**Deeper Learning:**
- Advanced Solidity patterns (proxy, factory, diamond)
- Gas optimization techniques
- Security auditing and formal verification
- DeFi protocol development

## Related Knowledge Files

- `solidity-patterns.json`
- `ethereum-security.json`

---

*Part of the Antigravity Agent Factory Learning Workshop Ecosystem*

**Workshop Definition:** `patterns/workshops/L1_ethereum_fundamentals.json`