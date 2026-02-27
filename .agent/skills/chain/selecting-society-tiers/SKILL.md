---
agents:
- none
category: chain
description: Interactive guidance for selecting appropriate trust verification tier
knowledge:
- none
name: selecting-society-tiers
related_skills:
- none
templates:
- none
tools:
- none
type: skill
version: 1.0.0
---
# Society Tier Selection

Interactive guidance for selecting appropriate trust verification tier

Select the optimal trust verification tier for multi-agent interactions based on stakes, context, and requirements.

## Process

See the detailed interactive selection process below with decision trees and tier reference.

## Best Practices

- Match verification cost to interaction stakes
- Start with lower tiers and escalate only when needed
- Use presets for common scenarios (DEVELOPMENT, PRODUCTION, ENTERPRISE)
- Document tier selection rationale for future reference
- Monitor escalation triggers and adjust accordingly
- Consider de-escalation after compliance periods

## Core Principle

> **Match verification cost to interaction stakes. Don't pay for blockchain when signatures suffice.**

## Quick Decision Tree

```
START: What is the economic value at risk?

Less than $100?
  └─► L0 Local (free, <10ms)
      Unless: Cross-organization OR audit required
              └─► L1 Attested ($0.0001, minutes)

$100 - $10,000?
  └─► L1 Attested (audit trail)
      Unless: Automated enforcement needed
              └─► L2 Contracted ($0.10, seconds)

$10,000 - $100,000?
  └─► L2 Contracted (smart contracts)
      Unless: Multi-party agreement required
              └─► L3 Consensus ($1-5, minutes)

Over $100,000?
  └─► L3 Consensus OR L4 Economic
      L4 if: Long-term partnership with stake commitment
```

## Tier Reference

| Tier | Mechanism | Latency | Cost | Best For |
|------|-----------|---------|------|----------|
| **L0 Local** | Ed25519 signatures | <10ms | Free | Internal agents, development |
| **L1 Attested** | Merkle anchoring | Minutes | $0.0001 | Cross-org, audit trails |
| **L2 Contracted** | Smart contracts | Seconds | $0.10 | Payments, SLAs |
| **L3 Consensus** | Multi-party BFT | Minutes | $1-5 | Critical decisions |
| **L4 Economic** | Stake + slashing | Variable | Stake | Long-term partnerships |

## Interactive Selection

When asked to select a tier, gather these inputs:

### 1. Economic Value

**Ask:** What is the approximate economic value at risk?

- Less than $100 → Start with L0
- $100-$10K → Start with L1
- $10K-$100K → Start with L2
- Over $100K → Start with L3/L4

### 2. Organizational Boundary

**Ask:** Is this interaction within the same organization or cross-organization?

- Same org → No change
- Cross-org → Increase tier by 1

### 3. Audit Requirements

**Ask:** Is an audit trail required for compliance or legal reasons?

- No → No change
- Yes → Minimum L1

### 4. Enforcement Needs

**Ask:** Do you need automated enforcement (penalties, refunds)?

- No → No change
- Yes → Minimum L2

### 5. Decision Authority

**Ask:** Does this require multi-party consensus?

- No → No change
- Yes → Minimum L3

### 6. Relationship Duration

**Ask:** Is this a long-term relationship requiring ongoing trust?

- No → Use tier from previous steps
- Yes → Consider L4 with stake

## Selection Output Format

After gathering inputs, provide:

```markdown

## Recommended Trust Tier: L{tier_number} {tier_name}

### Rationale
- Economic value: {value}
- Cross-organization: {yes/no}
- Audit required: {yes/no}
- Automated enforcement: {yes/no}
- Multi-party consensus: {yes/no}
- Long-term relationship: {yes/no}

### Tier Details
- **Mechanism**: {mechanism}
- **Latency**: {latency}
- **Cost**: {cost}
- **Guarantees**: {guarantees}

### Implementation
```python
from lib.society.simple import create_agent_society, SocietyPreset

# For L{tier_number}, use {preset} preset
society = create_agent_society(
    "YourProject",
    agents=["agent1", "agent2"],
    preset=SocietyPreset.{preset}
)
```

### Escalation Triggers
The system will automatically escalate to a higher tier if:
- {escalation_trigger_1}
- {escalation_trigger_2}
```

## Common Scenarios

### Development & Testing
**Recommendation:** L0 Local (DEVELOPMENT preset)
```python
society = create_agent_society("MyProject", preset=SocietyPreset.DEVELOPMENT)
```

### Production Internal
**Recommendation:** L1 Attested (PRODUCTION preset)
```python
society = create_agent_society("MyProject", preset=SocietyPreset.PRODUCTION)
```

### Cross-Organization API
**Recommendation:** L2 Contracted (ENTERPRISE preset)
```python
society = create_agent_society("MyProject", preset=SocietyPreset.ENTERPRISE)
```

### Financial Transactions
**Recommendation:** L2 or L3 depending on value
```python
# Configure for contracted trust
from lib.society.presets import SocietyBuilder, TrustTier

society = (SocietyBuilder("FinanceProject")
    .with_trust_tier(TrustTier.L2_CONTRACTED)
    .with_contract_enforcement(True)
    .with_agents(["payment_agent", "verification_agent"])
    .build())
```

## Cost-Benefit Analysis

| Tier | Setup Cost | Operational Cost | Security Level |
|------|------------|------------------|----------------|
| L0 | Minimal | Free | Good for trusted environments |
| L1 | Low | $0.10-$1/month | Audit-ready |
| L2 | Medium | $10-$100/month | Enterprise-grade |
| L3 | High | $100-$1000/month | Critical infrastructure |
| L4 | Very high | Stake opportunity cost | Maximum security |

## Escalation and De-escalation

### Automatic Escalation Triggers
- 3+ violations in 24 hours → +1 tier
- Dispute open >48 hours → +1 tier
- Multi-party conflict → Jump to L3
- Critical axiom violation → Jump to L3

### De-escalation
- 7 days compliance with no violations → -1 tier (minimum L0)

## References

- [Trust Tier Decision Matrix](../../knowledge/trust-tier-decision-matrix.json)
- **ASP Value Proposition**
- [Verified Communication Skill](../verified-communication/SKILL.md)

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.
