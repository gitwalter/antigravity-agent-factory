# Smart Contract Audit Workflow

## Overview

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

### Phase 1: Initial Review

**Description:** Understand contract purpose and architecture.

**Entry Criteria:** Contract code available  
**Exit Criteria:** Contract understood

#### Step 1.1: Scope Definition

**Actions:**
- Identify contracts to audit
- Document contract purposes
- Map contract interactions
- Note external dependencies

**Outputs:**
- Contract inventory
- Architecture diagram
- Dependency map

**Is Mandatory:** Yes

---

### Phase 2: Static Analysis

**Description:** Automated vulnerability scanning.

**Entry Criteria:** Scope defined  
**Exit Criteria:** Static analysis complete

#### Step 2.1: Run Security Scanners

**Actions:**
- Run Slither (Solidity)
- Run Mythril (Solidity)
- Run Aderyn (Solidity)
- Run Anchor verify (Solana)

**Skills:**
- `smart-contract-audit`: Analysis patterns

**Vulnerability Categories:**

| Category | Severity |
|----------|----------|
| Reentrancy | Critical |
| Access Control | Critical |
| Integer Overflow | High |
| Front-running | High |
| Oracle Manipulation | High |
| DoS | Medium |
| Gas Griefing | Medium |

**Outputs:**
- Scanner reports
- Vulnerability list

**Is Mandatory:** Yes

---

### Phase 3: Manual Review

**Description:** Human analysis of business logic and edge cases.

**Entry Criteria:** Static analysis complete  
**Exit Criteria:** Manual review complete

#### Step 3.1: Access Control Review

**Actions:**
- Check owner privileges
- Verify permission modifiers
- Test privilege escalation
- Review admin functions

#### Step 3.2: Business Logic Review

**Actions:**
- Trace value flows
- Verify invariants
- Check edge cases
- Validate calculations

#### Step 3.3: External Integration Review

**Actions:**
- Check oracle usage
- Verify token standards
- Test composability
- Review callbacks

**Outputs:**
- Manual findings
- Logic flow documentation

**Is Mandatory:** Yes

---

### Phase 4: Gas Analysis

**Description:** Optimize gas usage and prevent gas griefing.

**Entry Criteria:** Manual review complete  
**Exit Criteria:** Gas optimized

#### Step 4.1: Gas Profiling

**Actions:**
- Profile function gas costs
- Identify expensive operations
- Check storage patterns
- Analyze loops

**Skills:**
- `gas-optimization`: Optimization patterns

**Optimization Targets:**

| Pattern | Saving |
|---------|--------|
| Storage packing | 20-50% |
| Calldata vs memory | 10-30% |
| Unchecked math | 5-15% |
| Short-circuit | Variable |

**Outputs:**
- Gas report
- Optimization recommendations

**Is Mandatory:** Yes

---

### Phase 5: Test Coverage

**Description:** Verify test coverage and quality.

**Entry Criteria:** Gas analysis complete  
**Exit Criteria:** Coverage verified

#### Step 5.1: Analyze Test Suite

**Actions:**
- Check line coverage
- Check branch coverage
- Identify untested paths
- Review fuzz tests

**Skills:**
- `smart-contract-testing`: Testing patterns

**Coverage Requirements:**

| Metric | Minimum | Target |
|--------|---------|--------|
| Line Coverage | 90% | 98% |
| Branch Coverage | 85% | 95% |
| Fuzz Tests | Key functions | All external |

**Outputs:**
- Coverage report
- Test recommendations

**Is Mandatory:** Yes

---

### Phase 6: Report Generation

**Description:** Compile comprehensive audit report.

**Entry Criteria:** All reviews complete  
**Exit Criteria:** Report delivered

#### Step 6.1: Generate Audit Report

**Actions:**
- Classify all findings
- Prioritize by severity
- Provide remediation
- Calculate risk score

**Severity Classification:**

| Severity | Criteria | Fix Timeline |
|----------|----------|--------------|
| Critical | Direct fund loss possible | Pre-deployment |
| High | Significant impact, exploitable | Pre-deployment |
| Medium | Conditional impact | Pre-mainnet |
| Low | Minor issues | Optional |
| Informational | Best practices | Advisory |

**Outputs:**
- Audit report
- Risk assessment

**Is Mandatory:** Yes

---

## Decision Points

### Decision: Deployment Readiness

| Condition | Decision |
|-----------|----------|
| No critical/high | Safe to deploy |
| High severity | Fix required |
| Critical severity | Block deployment |

---

## Fallback Procedures

| Condition | Action |
|-----------|--------|
| Scanner not available | Use alternative scanner |
| Contract too complex | Split into modules |
| No test suite | Request tests before audit |
| External dependencies | Audit separately |
| Incomplete documentation | Request specs |

---

## Example Session

```
User: Audit the lending protocol contracts

Agent:
━━━ PHASE 1: Initial Review ━━━
Contracts identified:
- LendingPool.sol (main logic)
- InterestRate.sol (rate calculations)
- Liquidation.sol (liquidation logic)

━━━ PHASE 2: Static Analysis ━━━
Running Slither...
⚠️ 3 findings (1 high, 2 medium)

Running Mythril...
⚠️ 1 finding (reentrancy risk)

━━━ PHASE 3: Manual Review ━━━
❌ CRITICAL: Reentrancy in withdraw()
   No reentrancy guard on external call
   
⚠️ HIGH: Oracle staleness not checked
   Price feed can be stale

━━━ PHASE 4: Gas Analysis ━━━
Optimization opportunities:
- Pack structs: 15% savings
- Use calldata: 10% savings

━━━ PHASE 5: Test Coverage ━━━
Coverage: 87% (below 90% requirement)
Missing: Liquidation edge cases

━━━ PHASE 6: Report ━━━

# Audit Report: Lending Protocol

## Summary
- Critical: 1
- High: 1
- Medium: 3
- Low: 2

## Status: NOT READY FOR DEPLOYMENT

Critical issues must be fixed before mainnet.

✨ Audit complete!
```

---

## Related Artifacts

- **Skills**: `patterns/skills/smart-contract-audit.json`, `patterns/skills/gas-optimization.json`
- **Knowledge**: `knowledge/security-checklist.json`