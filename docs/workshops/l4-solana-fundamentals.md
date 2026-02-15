# Solana Program Development Fundamentals

> **Stack:** Solana + Anchor | **Level:** Fundamentals | **Duration:** 2.5 hours

## Overview

**Workshop ID:** `L4_solana_fundamentals`

**Technology:** Rust with Solana + Anchor (Anchor 0.30+)

## Prerequisites

**Required Knowledge:**
- Basic Rust syntax (ownership, borrowing, structs, enums)
- Understanding of blockchain concepts (transactions, accounts)
- Command-line proficiency

**Required Tools:**
- Rust and Cargo installed
- Solana CLI installed
- Anchor CLI installed
- Node.js 18+ for testing

## Learning Objectives

By the end of this workshop, you will be able to:

1. **Understand Solana's account model and how it differs from Ethereum's state model** (Understand)
2. **Create a basic Anchor program with initialization and update instructions** (Apply)
3. **Implement proper account validation using Anchor constraints** (Apply)
4. **Write and run TypeScript tests for Solana programs** (Apply)
5. **Identify common security vulnerabilities in Solana programs** (Analyze)

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

### Concept: Solana Architecture Deep Dive

*Understand the fundamental architecture that makes Solana unique*

**Topics Covered:**
- Account Model vs State Model
- Programs are stateless - all state in accounts
- Account structure: owner, data, lamports, rent
- Program Derived Addresses (PDAs)
- Cross-Program Invocation (CPI)
- Sealevel parallel execution

**Key Points:**
- Programs don't store data - accounts do
- Every account has an owner program
- PDAs are addresses without private keys
- Transactions declare all accounts upfront for parallel execution

### Demo: Building a Counter Program

*Live coding a simple Anchor program from scratch*

**Topics Covered:**
- Anchor project structure
- #[program] and #[account] macros
- Account constraints (init, mut, signer)
- Error handling with custom errors
- TypeScript client generation

**Key Points:**
- Anchor generates boilerplate for account validation
- The IDL enables type-safe clients
- Constraints are checked at runtime automatically

### Exercise: Your First Solana Program

*Build a simple note-taking program*

**Topics Covered:**
- Create NoteAccount with content and author
- Implement create_note instruction
- Add update_note with authority check
- Deploy to localnet

### Exercise: Testing Your Program

*Write comprehensive tests*

**Topics Covered:**
- Setting up Anchor test environment
- Testing happy path
- Testing error conditions
- Verifying account state

### Challenge: Secure Voting System

*Apply all concepts to build a secure voting program*

**Topics Covered:**
- Create Poll and Vote accounts
- Implement voting with one-vote-per-user (PDA)
- Add security: prevent double voting, verify authority
- Bonus: add time-locked voting period

### Reflection: Key Takeaways and Next Steps

*Consolidate learning and plan continued growth*

**Topics Covered:**
- Summary of Solana's account model
- Anchor's role in simplifying development
- Security considerations
- Resources for continued learning

**Key Points:**
- Always validate account ownership
- Store bump seeds for PDAs
- Use checked arithmetic
- Test both success and failure paths

## Hands-On Exercises

### Exercise: Note-Taking Program

Create a program to store personal notes on-chain

**Difficulty:** Easy | **Duration:** 25 minutes

**Hints:**
- Use seeds with author's public key for per-user notes
- Include bump in account data for efficient re-derivation
- has_one constraint validates author matches

**Common Mistakes to Avoid:**
- Forgetting system_program in CreateNote
- Wrong space calculation for String
- Missing #[account(mut)] on payer

### Exercise: Testing the Note Program

Write tests for the note program

**Difficulty:** Medium | **Duration:** 20 minutes

**Common Mistakes to Avoid:**
- Not deriving PDA correctly in test
- Forgetting to catch expected errors
- Not verifying account state after operations

## Challenges

### Challenge: Secure Voting System

Build a decentralized voting system with security guarantees

**Requirements:**
- Poll account: title, options (array), vote counts, creator, end_time
- Vote PDA per user per poll: prevents double voting
- Only poll creator can close polling
- Votes only counted before end_time

**Evaluation Criteria:**
- Program compiles and deploys
- One vote per user enforced via PDA
- Authority checks on admin functions
- Time-based constraints work correctly

**Stretch Goals:**
- Add weighted voting based on token holdings
- Implement vote delegation
- Add vote result verification

## Resources

**Official Documentation:**
- https://solana.com/docs
- https://www.anchor-lang.com/docs

**Tutorials:**
- https://solana.com/developers/guides
- https://www.rareskills.io/solana-tutorial

## Self-Assessment

Ask yourself these questions:

- [ ] Can I explain how accounts, programs, and PDAs work together?
- [ ] Do I understand why Anchor constraints are important for security?
- [ ] Can I write tests that verify both success and failure paths?

## Next Steps

**Next Workshop:** `L5_solana_tokens_nfts`

**Practice Projects:**
- Escrow program with PDA vaults
- Simple DEX with token swaps
- NFT minting program

**Deeper Learning:**
- Solana security audit checklist
- Token-2022 program features
- Cross-program invocation patterns

## Related Knowledge Files

- `solana-patterns.json`
- `anchor-patterns.json`
- `solana-security.json`

---

*Part of the Antigravity Agent Factory Learning Workshop Ecosystem*

**Workshop Definition:** `.agent/patterns/workshops/L4_solana_fundamentals.json`