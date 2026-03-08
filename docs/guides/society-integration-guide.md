# Agent Society Protocol (ASP) Integration Guide

The **Agent Society Protocol (ASP)** defines a verified, high-fidelity communication framework for multi-agent collaboration. It ensures that agents interact within a secure, trust-aware environment.

## 1. Overview
ASP provides the infrastructure for:
- **Identity Management**: Cryptographically verified agent identities.
- **Contract Enforcement**: Enforcing capabilities and obligations between agents.
- **Reputation Tracking**: Monitoring agent behavior and performance.
- **Audit Trails**: Immutable event logs for every interaction.

## 2. Core Concepts
### The Society
A `Society` is a container for agents. It manages the lifecycle of agents and facilitates their communication.

### Contracts
Agents within a society interact through **Contracts**. A contract defines:
- **Parties**: The agents involved.
- **Capabilities**: What the agents are allowed to do.
- **Obligations**: What the agents are required to do.

## 3. Integration Patterns
### Simple Society Setup
The easiest way to start is using the `simple` API:
```python
from lib.society.simple import create_agent_society

# Create a society with two agents
society = create_agent_society("MySociety", agents=["sender", "receiver"])

# Send a verified message
result = society.send("sender", "receiver", {"payload": "data"})
```

### Advanced Blueprint Integration
For production systems, society configuration is managed via **Blueprints**:
- `multi-agent-systems`: Full society with complex coordination patterns.
- `ai-agent-development`: Focused on agent creation within a society.

## 4. Trust Tiers
Every interaction in a society is assigned a **Trust Tier**. See the [Trust Tier Selection Guide](trust-tier-selection.md) for more details.

---
*Antigravity Agent Factory v1.6.0*
