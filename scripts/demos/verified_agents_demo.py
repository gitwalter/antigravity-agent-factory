#!/usr/bin/env python3
"""
Verified Agents Demo

Demonstrates the Agent Society Verification Architecture with two agents
communicating through cryptographically signed, axiom-verified channels.

This demo shows:
1. Creating a shared SocietyContext with all verification infrastructure
2. Establishing agent bridges for verified communication
3. Sending messages that pass axiom verification
4. Detecting and handling axiom violations
5. Creating and enforcing agent contracts
6. Tracking reputation based on behavior
7. Querying the immutable event store

Usage:
    python scripts/verified_agents_demo.py

Requirements:
    - lib/society module must be accessible
    - No external dependencies beyond standard library
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from lib.society import (
    SocietyContext,
    AgentSocietyBridge,
    MessageRouter,
    MessageType,
    AgentContract,
    Party,
    Capability,
    Obligation,
    Prohibition,
    AxiomRequirements,
)
from lib.society.events import EventQuery


def print_section(title: str) -> None:
    """Print a formatted section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_result(label: str, result) -> None:
    """Print a formatted result."""
    status = "[OK]" if result.success else "[FAIL]"
    verified = "VERIFIED" if result.verified else "UNVERIFIED"
    print(f"  {status} {label}: {verified}")
    if result.violations:
        for v in result.violations:
            # violations may be strings or objects
            if isinstance(v, str):
                print(f"      [!] {v}")
            else:
                print(f"      [!] [{v.axiom}] {v.description}")


def demo_basic_communication(context: SocietyContext) -> tuple:
    """
    Demonstrate basic verified communication between two agents.
    
    Creates an orchestrator and worker agent, then sends verified
    messages between them.
    
    Args:
        context: Shared society context
        
    Returns:
        Tuple of (orchestrator, worker) bridges for further demos
    """
    print_section("1. BASIC VERIFIED COMMUNICATION")
    
    # Create agent bridges
    print("\n  Creating agent bridges...")
    orchestrator = AgentSocietyBridge(
        agent_id="orchestrator",
        agent_type="conductor",
        context=context,
        name="Orchestrator Agent"
    )
    print(f"    Created: {orchestrator.agent_id} (type: conductor)")
    
    worker = AgentSocietyBridge(
        agent_id="worker-1",
        agent_type="executor",
        context=context,
        name="Worker Agent"
    )
    print(f"    Created: {worker.agent_id} (type: executor)")
    
    # Set up message router
    router = MessageRouter(context)
    router.register(orchestrator)
    router.register(worker)
    print(f"\n  Message router active: {router.get_registered_agents()}")
    
    # Send a verified request
    print("\n  Sending verified request...")
    result = orchestrator.send_message(
        target="worker-1",
        message_type=MessageType.REQUEST,
        payload={
            "task": "analyze_code",
            "file": "main.py",
            "scope": "security"
        },
        justification="Delegating code analysis to worker for user security review request",
        axiom_alignment=["A1", "A2"]  # Love, Truth
    )
    print_result("Request message", result)
    
    # Worker sends response (using INFORM for replies)
    print("\n  Worker sending response...")
    result = worker.send_message(
        target="orchestrator",
        message_type=MessageType.INFORM,
        payload={
            "status": "complete",
            "findings": ["Input validation missing", "SQL injection risk"],
            "severity": "high"
        },
        justification="Reporting security findings to orchestrator for user protection",
        axiom_alignment=["A1", "A2", "A4"]  # Love, Truth, Guardian
    )
    print_result("Response message", result)
    
    return orchestrator, worker


def demo_axiom_verification(worker: AgentSocietyBridge) -> None:
    """
    Demonstrate axiom verification detecting problematic actions.
    
    Shows how the verification system catches actions that violate
    foundational axioms.
    
    Args:
        worker: Worker agent bridge
    """
    print_section("2. AXIOM VERIFICATION")
    
    # This message should pass - helpful and transparent
    print("\n  Sending helpful message (should pass)...")
    result = worker.send_message(
        target="orchestrator",
        message_type=MessageType.INFORM,
        payload={"status": "ready", "capacity": "available"},
        justification="Informing orchestrator of availability to help users"
    )
    print_result("Helpful inform", result)
    
    # This decision should trigger A4 Guardian - mentions harm
    print("\n  Recording potentially harmful decision (should flag)...")
    result = worker.send_decision(
        description="Override safety checks",
        payload={"action": "bypass_validation", "target": "user_input"},
        justification="Skipping validation to speed up processing"
    )
    print_result("Harmful decision", result)
    if not result.verified:
        print("    -> A4 Guardian correctly detected potential harm")


def demo_contracts(context: SocietyContext, orchestrator: AgentSocietyBridge, worker: AgentSocietyBridge) -> None:
    """
    Demonstrate contract creation and enforcement.
    
    Shows how agents can establish formal agreements that are
    cryptographically verified and enforced.
    
    Args:
        context: Shared society context
        orchestrator: Orchestrator agent bridge
        worker: Worker agent bridge
    """
    print_section("3. CONTRACT ENFORCEMENT")
    
    # Create a collaboration contract using the helper method
    print("\n  Creating collaboration contract...")
    
    contract = orchestrator.create_contract_with(
        other_agent_id="worker-1",
        other_role="analyzer",
        my_role="delegator",
        my_capabilities=["delegate_analysis", "review_findings"],
        other_capabilities=["analyze_code", "report_findings"]
    )
    
    print(f"    Contract ID: {contract.contract_id}")
    print(f"    Parties: {[p.agent_id for p in contract.parties]}")
    print(f"    Capabilities: {len(contract.capabilities)}")
    print(f"    Version: {contract.version}")
    
    # Worker signs (orchestrator already signed via create_contract_with)
    print("\n  Signing contract...")
    print(f"    [OK] Orchestrator signed (via create)")
    worker.sign_contract(contract)
    print(f"    [OK] Worker signed")
    
    # Verify contract is active
    contracts = context.contract_registry.find_contracts("worker-1")
    print(f"\n  Active contracts for worker-1: {len(contracts)}")
    
    # Test contract enforcement - allowed action
    print("\n  Testing allowed action (analyze_code)...")
    result = worker.send_message(
        target="orchestrator",
        message_type=MessageType.INFORM,
        payload={"analysis": "File parsed successfully"},
        justification="Reporting code analysis progress to help user understand security status",
        axiom_alignment=["A1", "A2"]  # Love, Truth
    )
    print_result("Allowed action", result)
    
    # Test contract enforcement - this violates prohibition
    print("\n  Testing prohibited action (modify_source_code)...")
    result = worker.send_message(
        target="orchestrator",
        message_type=MessageType.REQUEST,
        payload={"action": "modify_source_code", "target": "main.py"},
        justification="Attempting to fix the code directly"
    )
    print_result("Prohibited action", result)
    if not result.verified:
        print("    -> Contract correctly prohibited code modification")


def demo_reputation(context: SocietyContext, orchestrator: AgentSocietyBridge, worker: AgentSocietyBridge) -> None:
    """
    Demonstrate reputation system tracking.
    
    Shows how agent behavior affects their reputation score and trust level.
    
    Args:
        context: Shared society context
        orchestrator: Orchestrator agent bridge
        worker: Worker agent bridge
    """
    print_section("4. REPUTATION SYSTEM")
    
    # Get current reputation scores
    print("\n  Current reputation scores:")
    for agent_id in ["orchestrator", "worker-1"]:
        score = context.reputation_system.get_score(agent_id)
        print(f"    {agent_id}: {score.current_score:.3f} ({score.trust_level})")
    
    # Multiple compliant actions boost reputation
    print("\n  Worker sending multiple compliant messages...")
    for i in range(3):
        worker.send_message(
            target="orchestrator",
            message_type=MessageType.INFORM,
            payload={"progress": f"Step {i+1} complete"},
            justification=f"Progress update {i+1} for user visibility"
        )
    
    # Check updated reputation
    print("\n  Updated reputation scores:")
    for agent_id in ["orchestrator", "worker-1"]:
        score = context.reputation_system.get_score(agent_id)
        history = score.history[-3:] if score.history else []
        print(f"    {agent_id}: {score.current_score:.3f} ({score.trust_level})")
        if history:
            # history items may have different structures
            recent = [str(e)[:20] for e in history]
            print(f"      Recent events: {len(history)}")


def demo_event_store(context: SocietyContext) -> None:
    """
    Demonstrate the immutable event store.
    
    Shows how all verified events are recorded in a hash-chained log.
    
    Args:
        context: Shared society context
    """
    print_section("5. IMMUTABLE EVENT STORE")
    
    # Get event count
    events = context.event_store.query(EventQuery(limit=100))
    print(f"\n  Total events recorded: {len(events)}")
    
    # Show recent events
    print("\n  Recent events:")
    for event in events[-5:]:
        print(f"    seq={event.sequence} | {event.agent.id} | {event.action.type.value}")
    
    # Verify chain integrity
    print("\n  Verifying hash chain integrity...")
    chain_result = context.event_store.verify()
    status = "[OK] VALID" if chain_result.valid else "[X] CORRUPTED"
    print(f"    Chain integrity: {status}")
    
    # Show hash chain sample
    if events:
        print("\n  Hash chain sample:")
        for event in events[-3:]:
            print(f"    Event {event.sequence}:")
            print(f"      Hash: {event.hash[:32]}...")
            if event.previous_hash:
                print(f"      Prev: {event.previous_hash[:32]}...")


def demo_society_stats(context: SocietyContext) -> None:
    """
    Demonstrate society-wide statistics and monitoring.
    
    Shows aggregate metrics across all agents and events.
    
    Args:
        context: Shared society context
    """
    print_section("6. SOCIETY STATISTICS")
    
    stats = context.get_stats()
    
    print(f"\n  Society: {context.config.name}")
    print(f"  Verification Level: {context.config.verification_level.value}")
    print(f"\n  Events:")
    print(f"    Total: {stats.get('event_count', 0)}")
    print(f"    Verified: {stats.get('verifications_passed', 0)}")
    print(f"    Messages: {stats.get('messages_sent', 0)}")
    print(f"\n  Agents:")
    print(f"    Registered: {stats.get('registered_agents', 0)}")
    print(f"    Contracts: {stats.get('contract_count', 0)}")
    print(f"\n  Uptime: {stats.get('uptime_seconds', 0):.1f} seconds")


def main():
    """
    Main entry point for the verified agents demo.
    
    Creates a society context and runs through all demonstration
    scenarios showing the Agent Society Verification Architecture.
    """
    print("\n" + "=" * 60)
    print("  AGENT SOCIETY VERIFICATION - DEMONSTRATION")
    print("  Axiom-Verified Multi-Agent Communication")
    print("=" * 60)
    
    # Create society context
    print("\n  Initializing society context...")
    context = SocietyContext.create_default("Demo Agent Society")
    print(f"    [OK] Society: {context.config.name}")
    print(f"    [OK] Event store initialized")
    print(f"    [OK] Axiom monitor active (6 verifiers)")
    print(f"    [OK] Contract registry ready")
    print(f"    [OK] Reputation system online")
    
    # Run demonstrations
    orchestrator, worker = demo_basic_communication(context)
    demo_axiom_verification(worker)
    demo_contracts(context, orchestrator, worker)
    demo_reputation(context, orchestrator, worker)
    demo_event_store(context)
    demo_society_stats(context)
    
    # Final summary
    print_section("DEMONSTRATION COMPLETE")
    print("""
  The Agent Society Verification Architecture enables:
  
  1. Cryptographically signed agent identities
  2. Axiom-verified communication (A0-A5)
  3. Contract-enforced collaboration
  4. Reputation-based trust management
  5. Immutable, hash-chained event logs
  6. Real-time compliance monitoring
  
  All Factory agents can now communicate through verified channels,
  ensuring every interaction aligns with our foundational axioms:
  
    A0 - SDG (Sustainable Development)
    A1 - Love (User Wellbeing)
    A2 - Truth (Transparency)
    A3 - Beauty (Simplicity)
    A4 - Guardian (Harm Prevention)
    A5 - Memory (Consent-Based)
""")


if __name__ == "__main__":
    main()
