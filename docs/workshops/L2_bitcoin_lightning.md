# Bitcoin and Lightning Network Fundamentals

> **Stack:** Bitcoin + Lightning | **Level:** Fundamentals | **Duration:** 2.5 hours

## Overview

**Workshop ID:** `L2_bitcoin_lightning`

**Technology:** Script/TypeScript with Bitcoin + Lightning (Bitcoin Core)

## Prerequisites

**Required Knowledge:**
- Basic understanding of blockchain concepts
- Cryptography basics (hash functions, digital signatures)
- JavaScript/TypeScript for Lightning development
- Command-line proficiency

**Required Tools:**
- Node.js 18+ installed
- Bitcoin Core (or testnet node access)
- Lightning node software (LND, CLN, or similar)
- Code editor (VS Code recommended)

## Learning Objectives

By the end of this workshop, you will be able to:

1. **Understand the UTXO (Unspent Transaction Output) model and how it differs from Ethereum's account model** (Understand)
2. **Learn Bitcoin Script basics and common script patterns (P2PKH, P2SH, multisig)** (Understand)
3. **Understand Bitcoin transaction structure: inputs, outputs, scripts, and signatures** (Understand)
4. **Learn Lightning Network payment channels and how they enable instant, low-cost transactions** (Understand)
5. **Understand HTLC (Hashed Time Lock Contract) mechanics for Lightning payments** (Understand)

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

### Concept: UTXO Model and Bitcoin Script

*Deep dive into Bitcoin's unique transaction model*

**Topics Covered:**
- UTXO model vs Account model comparison
- Transaction structure: inputs, outputs, scripts, signatures
- Bitcoin Script: stack-based language, opcodes
- Common script patterns: P2PKH, P2SH, P2WPKH, multisig
- Transaction lifecycle: creation, signing, broadcasting, confirmation
- Fee calculation and transaction prioritization

**Key Points:**
- Bitcoin uses UTXOs, not account balances
- Each UTXO can only be spent once (double-spend prevention)
- Scripts define spending conditions
- Transactions consume inputs and create outputs
- Fees are the difference between input and output values

### Demo: Building a Multisig Transaction

*Live demonstration of creating and signing a multisig transaction*

**Topics Covered:**
- Setting up Bitcoin testnet environment
- Creating a 2-of-3 multisig address
- Building a transaction with multiple inputs
- Signing transaction with multiple keys
- Broadcasting and verifying transaction
- Using Bitcoin libraries (bitcoinjs-lib)

**Key Points:**
- Multisig requires M-of-N signatures
- Redeem script defines the multisig conditions
- Each signer must provide their signature
- Transaction must be fully signed before broadcasting

### Exercise: Creating Bitcoin Transactions

*Practice building and signing Bitcoin transactions*

**Topics Covered:**
- Create a simple P2PKH transaction
- Calculate transaction fees
- Sign transaction with private key
- Verify transaction before broadcasting

### Exercise: Lightning Network Basics

*Work with Lightning Network APIs*

**Topics Covered:**
- Open a payment channel
- Create Lightning invoices
- Send payments through channels
- Query channel status

### Challenge: Lightning Invoice Flow

*Build a complete Lightning payment flow*

**Topics Covered:**
- Create Lightning invoice with proper metadata
- Implement payment sending with retry logic
- Handle payment status updates
- Verify payment completion
- Handle payment failures gracefully

### Reflection: Key Takeaways and Bitcoin Philosophy

*Consolidate learning and understand Bitcoin's design philosophy*

**Topics Covered:**
- Summary of UTXO model advantages
- Bitcoin Script's security through simplicity
- Lightning Network's role in scaling
- Bitcoin's emphasis on decentralization and security
- Resources for continued learning

**Key Points:**
- UTXO model provides strong privacy and parallel processing
- Bitcoin Script is intentionally limited for security
- Lightning enables instant, low-cost payments
- Always verify transactions before broadcasting
- Understand fees and confirmation requirements

## Hands-On Exercises

### Exercise: Create Bitcoin Transaction

Build and sign a Bitcoin transaction using bitcoinjs-lib

**Difficulty:** Medium | **Duration:** 25 minutes

**Hints:**
- Use bitcoinjs-lib's PSBT (Partially Signed Bitcoin Transaction) for modern transaction building
- Remember to include a change output if your input value exceeds send amount + fee
- Testnet addresses start with 'm' or 'n' (P2PKH) or '2' (P2SH)
- Always verify signatures before finalizing
- Use testnet faucets to get testnet Bitcoin

**Common Mistakes to Avoid:**
- Forgetting to include change output
- Incorrect fee calculation
- Using mainnet network instead of testnet
- Not verifying signatures before finalizing
- Incorrect UTXO scriptPubKey format

### Exercise: Lightning Invoice Creation

Create and work with Lightning Network invoices

**Difficulty:** Medium | **Duration:** 20 minutes

**Common Mistakes to Avoid:**
- Incorrect LND connection parameters
- Not handling async/await properly
- Forgetting to set invoice expiry
- Not checking invoice status after creation
- Using wrong invoice ID format

## Challenges

### Challenge: Complete Lightning Payment Flow

Build a complete Lightning payment application

**Requirements:**
- Create Lightning invoice with proper metadata
- Implement payment sending with retry logic
- Handle payment status updates (pending, completed, failed)
- Verify payment completion
- Handle payment failures with proper error messages
- Add logging for debugging

**Evaluation Criteria:**
- Invoice creation works correctly
- Payment sending handles retries
- Status updates are accurate
- Error handling is comprehensive
- Code is well-structured and documented

**Stretch Goals:**
- Add webhook support for payment notifications
- Implement payment splitting across multiple channels
- Add payment analytics and reporting
- Create a simple web UI for the payment flow

## Resources

**Official Documentation:**
- https://bitcoin.org/en/developer-documentation
- https://lightning.network/
- https://github.com/lightningnetwork/lnd
- https://bitcoinjs.org/

**Tutorials:**
- Bitcoin Developer Guide
- Lightning Network Developer Resources
- Mastering Bitcoin by Andreas Antonopoulos

**Videos:**
- Bitcoin Core YouTube channel
- Lightning Network tutorials

## Self-Assessment

Ask yourself these questions:

- [ ] Can I explain the UTXO model and how transactions work?
- [ ] Do I understand Bitcoin Script basics and common patterns?
- [ ] Can I build and sign a Bitcoin transaction?
- [ ] Do I understand how Lightning payment channels work?
- [ ] Can I explain HTLC mechanics for payment routing?

## Next Steps

**Next Workshop:** `L3_bitcoin_advanced`

**Practice Projects:**
- Bitcoin wallet with HD key derivation
- Lightning payment processor
- Multisig transaction builder
- Bitcoin transaction fee estimator

**Deeper Learning:**
- Advanced Bitcoin Script patterns
- Lightning Network protocol details
- Bitcoin privacy techniques (CoinJoin, etc.)
- Bitcoin Core development

## Related Knowledge Files

- `bitcoin-patterns.json`

---

*Part of the Antigravity Agent Factory Learning Workshop Ecosystem*

**Workshop Definition:** `patterns/workshops/L2_bitcoin_lightning.json`