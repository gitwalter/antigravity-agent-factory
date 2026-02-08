---
name: verified-communication
description: Enable verified, axiom-compliant communication between Factory agents
type: skill
pattern: patterns/skills/verified-communication.json
axioms: [A0-SDG, A1-Love, A2-Truth, A3-Beauty, A4-Guardian, A5-Memory]
---

# Verified Communication Skill

Enable Factory agents to communicate through cryptographically signed, axiom-verified channels. Every message is validated against foundational axioms before delivery.

## Core Principle

> **Agent communication should be as trustworthy as the axioms that govern it. Every message is signed, every action is verified, every interaction builds or breaks reputation.**

## How It Works

```
┌─────────────────┐                           ┌─────────────────┐
│  Sender Agent   │                           │ Receiver Agent  │
│                 │                           │                 │
│ AgentSociety    │                           │ AgentSociety    │
│ Bridge          │                           │ Bridge          │
└────────┬────────┘                           └────────┬────────┘
         │                                             │
         ▼                                             │
┌─────────────────────────────────────────────────────┐
│              SocietyContext                         │
│  ┌─────────────┐  ┌────────────┐  ┌──────────────┐ │
│  │ EventStore  │  │ Axiom      │  │ Contract     │ │
│  │ (immutable) │  │ Monitor    │  │ Verifier     │ │
│  └─────────────┘  └────────────┘  └──────────────┘ │
│  ┌─────────────┐  ┌────────────┐  ┌──────────────┐ │
│  │ Trust Graph │  │ Reputation │  │ Message      │ │
│  │             │  │ System     │  │ Router       │ │
│  └─────────────┘  └────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────┘
         │                                             │
         ▼                                             ▼
    ✓ Signed                                     ✓ Delivered
    ✓ Verified                                   ✓ Handled
    ✓ Recorded                                   ✓ Responded
```

## Quick Start

### 1. Initialize Society Context

```python
from lib.society import SocietyContext

# Create shared verification context
context = SocietyContext.create_default("Factory Agent Society")
```

### 2. Create Agent Bridges

```python
from lib.society import AgentSocietyBridge

# Each agent gets a bridge to the verified society
orchestrator = AgentSocietyBridge(
    agent_id="orchestrator",
    agent_type="conductor",
    context=context,
    name="Orchestrator Agent"
)

worker = AgentSocietyBridge(
    agent_id="worker-1",
    agent_type="executor",
    context=context,
    name="Worker Agent"
)
```

### 3. Enable Message Routing

```python
from lib.society import MessageRouter

# Create router for verified message delivery
router = MessageRouter(context)
router.register(orchestrator)
router.register(worker)
```

### 4. Send Verified Messages

```python
from lib.society import MessageType

# Messages are automatically signed and verified
result = orchestrator.send_message(
    target="worker-1",
    message_type=MessageType.REQUEST,
    payload={"task": "analyze_code", "file": "main.py"},
    justification="Delegating code analysis for user request",
    axiom_alignment=["A1", "A2"]  # Love, Truth
)

if result.verified:
    print(f"Message verified and recorded: {result.event_id}")
else:
    print(f"Violations detected: {result.violations}")
```

## Key Components

### SocietyContext

Shared infrastructure for all verified agents:

| Component | Purpose |
|-----------|---------|
| `EventStore` | Immutable, hash-chained event log |
| `AxiomComplianceMonitor` | Verifies events against A0-A5 axioms |
| `ContractVerifier` | Enforces agent contracts and capabilities |
| `ReputationSystem` | Tracks agent trustworthiness |
| `TrustGraph` | Manages trust delegations between agents |
| `IdentityRegistry` | Cryptographic identity management |

### AgentSocietyBridge

Per-agent interface to the verified society:

| Method | Purpose |
|--------|---------|
| `send_message(target, type, payload)` | Send verified message to another agent |
| `send_decision(description, payload)` | Record a decision for audit trail |
| `sign_contract(contract)` | Commit to a formal agent contract |
| `create_contract_with(partner)` | Establish verified collaboration |
| `add_message_handler(callback)` | Handle incoming verified messages |
| `get_status()` | Get current verification status |

### MessageRouter

Routes verified messages between agents:

| Method | Purpose |
|--------|---------|
| `register(bridge)` | Add agent to routing |
| `unregister(agent_id)` | Remove agent from routing |
| `route(event, sender, recipient)` | Deliver verified message |
| `broadcast(event, sender)` | Send to all registered agents |
| `get_queue_size(agent_id)` | Check pending messages |

## Message Types

| Type | Purpose | Example |
|------|---------|---------|
| `REQUEST` | Ask agent to perform action | "Please analyze this file" |
| `RESPONSE` | Reply to a request | "Analysis complete, found 3 issues" |
| `INFORM` | Share information | "User preferences updated" |
| `PROPOSE` | Suggest action/agreement | "Propose contract for collaboration" |
| `CONFIRM` | Accept proposal | "Contract accepted" |
| `REJECT` | Decline proposal | "Cannot commit to this obligation" |
| `QUERY` | Request information | "What is your current capacity?" |

## Axiom Verification

Every message is verified against foundational axioms:

| Axiom | Checks For |
|-------|------------|
| **A0 (SDG)** | Sustainable, non-wasteful actions |
| **A1 (Love)** | User wellbeing, non-manipulation |
| **A2 (Truth)** | Transparency, no deception |
| **A3 (Beauty)** | Simplicity, clarity, elegance |
| **A4 (Guardian)** | Harm prevention, escalation when needed |
| **A5 (Memory)** | Proper consent for memory operations |

### Handling Violations

```python
result = agent.send_message(
    target="other-agent",
    message_type=MessageType.INFORM,
    payload={"data": "something"},
    justification="Informing about status"
)

if not result.verified:
    for violation in result.violations:
        print(f"[{violation.axiom}] {violation.severity}: {violation.description}")
        if violation.requires_escalation:
            # Notify human or guardian agent
            escalate_to_guardian(violation)
```

## Contract-Based Communication

Establish formal agreements between agents:

```python
from lib.society import (
    AgentContract, Party, Capability, Obligation, Prohibition
)

# Define contract
contract = AgentContract(
    contract_id="collab-001",
    name="Code Analysis Collaboration",
    parties=[
        Party("orchestrator", "delegator"),
        Party("worker-1", "analyzer")
    ],
    capabilities=[
        Capability("orchestrator", "delegate_analysis"),
        Capability("worker-1", "analyze_code"),
        Capability("worker-1", "report_findings")
    ],
    obligations=[
        Obligation("worker-1", "respond_within_timeout", {"timeout": 60}),
        Obligation("orchestrator", "provide_context")
    ],
    prohibitions=[
        Prohibition("worker-1", "modify_code"),
        Prohibition("worker-1", "access_secrets")
    ]
)

# Both parties sign
orchestrator.sign_contract(contract)
worker.sign_contract(contract)
```

## Trust and Reputation

### Trust Levels

| Level | Score Range | Meaning |
|-------|-------------|---------|
| `TRUSTED` | 0.8 - 1.0 | Fully trusted, minimal verification |
| `VERIFIED` | 0.6 - 0.8 | Mostly trusted, standard verification |
| `NEUTRAL` | 0.4 - 0.6 | No track record, full verification |
| `PROBATIONARY` | 0.2 - 0.4 | Previous issues, enhanced verification |
| `UNTRUSTED` | 0.0 - 0.2 | Major violations, restricted access |

### Reputation Events

| Event | Impact | Description |
|-------|--------|-------------|
| Axiom compliance | +5 | Action passed all axiom checks |
| Contract fulfilled | +10 | Completed obligation |
| Axiom violation | -10 to -50 | Severity-dependent penalty |
| Contract breach | -20 | Failed obligation |
| Endorsement | +15 | Trusted agent vouched |

## Event Sourcing

All verified actions are immutably recorded:

```python
# Query agent history
events = context.event_store.query(agent_id="worker-1", limit=10)

for event in events:
    print(f"{event.timestamp}: {event.action.action_type}")
    print(f"  Verified: {event.verified}")
    print(f"  Hash: {event.event_hash}")
```

### Hash Chain Integrity

```
Event 1      Event 2      Event 3
┌───────┐    ┌───────┐    ┌───────┐
│ hash1 │───▶│ hash2 │───▶│ hash3 │
│       │    │ prev: │    │ prev: │
│       │    │ hash1 │    │ hash2 │
└───────┘    └───────┘    └───────┘

# Verify chain integrity
is_valid = context.event_store.verify_chain_integrity()
```

## Monitoring and Observability

### Get Society Statistics

```python
stats = context.get_stats()
print(f"Total events: {stats['total_events']}")
print(f"Verified events: {stats['verified_events']}")
print(f"Violations: {stats['total_violations']}")
print(f"Registered agents: {stats['registered_agents']}")
```

### Get Agent Status

```python
status = orchestrator.get_status()
print(f"Agent: {status['agent_id']}")
print(f"Reputation: {status['reputation_score']}")
print(f"Trust level: {status['trust_level']}")
print(f"Messages sent: {status['total_messages']}")
```

### Export for Audit

```python
# Export full society state
audit_data = context.export()

# Includes:
# - All events with hash chain
# - All contracts
# - Reputation scores
# - Trust delegations
# - Violation history
```

## Integration Patterns

### Pattern 1: Orchestrator-Worker

```python
# Orchestrator delegates verified tasks
result = orchestrator.send_message(
    target="worker-1",
    message_type=MessageType.REQUEST,
    payload={"task": "process_data", "input": data},
    justification="Delegating data processing task"
)

# Worker handles and responds
def handle_request(message):
    result = process(message.payload["input"])
    worker.send_message(
        target=message.sender,
        message_type=MessageType.RESPONSE,
        payload={"result": result},
        justification="Responding with processed data"
    )

worker.add_message_handler(handle_request)
```

### Pattern 2: Consensus Decision

```python
# Propose decision
orchestrator.send_decision(
    description="Approved code deployment",
    payload={"commit": "abc123", "environment": "staging"},
    justification="All tests passed, proceeding with deployment"
)

# Query recent decisions
decisions = context.event_store.query(
    agent_id="orchestrator",
    action_type="decision"
)
```

### Pattern 3: Trust Delegation

```python
from lib.society import TrustLevel

# Senior agent vouches for junior
context.trust_graph.delegate_trust(
    from_agent="senior-agent",
    to_agent="junior-agent",
    level=TrustLevel.VERIFIED,
    scope=["code_analysis"],
    justification="Demonstrated competence in code review"
)
```

## Error Handling

### BridgeResult States

| State | Meaning | Action |
|-------|---------|--------|
| `success=True, verified=True` | Message sent and verified | Proceed |
| `success=True, verified=False` | Message sent but violations | Review violations |
| `success=False` | Send failed | Check error, retry |

### Common Errors

```python
try:
    result = agent.send_message(...)
except Exception as e:
    if "not registered" in str(e):
        # Agent not in society
        router.register(agent)
    elif "contract violation" in str(e):
        # Action prohibited by contract
        handle_contract_violation(e)
```

## Best Practices

1. **Always provide justification**: Helps with axiom verification and audit
2. **Align with relevant axioms**: Explicitly state which axioms apply
3. **Handle violations gracefully**: Don't ignore verification failures
4. **Monitor reputation**: Track agent trustworthiness over time
5. **Use contracts for critical interactions**: Formal agreements prevent disputes
6. **Export regularly**: Maintain audit trails for compliance

## Related Components

| Component | Relationship |
|-----------|--------------|
| `lib/society/events/` | Event storage and hash chains |
| `lib/society/verification/` | Axiom verifiers and compliance monitor |
| `lib/society/contracts/` | Contract schema and verification |
| `lib/society/trust/` | Identity, reputation, and trust graph |
| `lib/society/hybrid/` | Full hybrid verification system |

## Axiom Alignment

| Axiom | How This Skill Applies |
|-------|------------------------|
| A0 (SDG) | Sustainable agent society, efficient resource use |
| A1 (Love) | Agent actions serve user wellbeing |
| A2 (Truth) | Transparent, cryptographically verified communication |
| A3 (Beauty) | Clean API, simple integration patterns |
| A4 (Guardian) | Automatic violation detection and escalation |
| A5 (Memory) | Immutable event store with proper consent |

## References

- `lib/society/` - Core verification infrastructure
- `docs/design/AGENT_SOCIETY_VERIFICATION.md` - Design document
- `tests/lib/society/test_integration.py` - Integration tests
- `examples/verified_agents_demo.py` - Working demonstration
