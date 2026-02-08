#!/usr/bin/env python3
"""
Society Verification Dashboard

CLI tool for monitoring agent society verification status, viewing events,
checking agent reputation, and inspecting contracts.

Usage:
    python cli/society_dashboard.py status
    python cli/society_dashboard.py events [--agent AGENT_ID] [--limit N]
    python cli/society_dashboard.py agents [--agent AGENT_ID]
    python cli/society_dashboard.py contracts [--agent AGENT_ID]
    python cli/society_dashboard.py verify
    python cli/society_dashboard.py violations [--limit N]

Examples:
    # Show overall status
    python cli/society_dashboard.py status
    
    # List recent events
    python cli/society_dashboard.py events --limit 20
    
    # Check specific agent
    python cli/society_dashboard.py agents --agent orchestrator
    
    # View active contracts
    python cli/society_dashboard.py contracts
    
    # Verify chain integrity
    python cli/society_dashboard.py verify
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from lib.society import (
    SocietyContext,
    AgentContract,
)
from lib.society.events import EventQuery


def create_context(persist_path: Optional[str] = None) -> SocietyContext:
    """
    Create or load a society context.
    
    Args:
        persist_path: Optional path for persistence.
        
    Returns:
        SocietyContext instance.
    """
    return SocietyContext.create_default(
        name="Factory Agent Society",
        persist_path=persist_path
    )


def cmd_status(args: argparse.Namespace) -> int:
    """
    Show overall society status.
    
    Args:
        args: Parsed command line arguments.
        
    Returns:
        Exit code (0 for success).
    """
    context = create_context(args.persist)
    stats = context.get_stats()
    
    print("\n=== SOCIETY VERIFICATION DASHBOARD ===\n")
    print(f"Society: {context.config.name}")
    print(f"Verification Level: {context.config.verification_level.value}")
    print(f"Created: {stats.get('created_at', 'N/A')}")
    print(f"Uptime: {stats.get('uptime_seconds', 0):.1f}s")
    
    print("\n--- Events ---")
    print(f"  Total Events: {stats.get('event_count', 0)}")
    print(f"  Verified: {stats.get('verifications_passed', 0)}")
    print(f"  Failed: {stats.get('verifications_failed', 0)}")
    print(f"  Messages: {stats.get('messages_sent', 0)} sent, {stats.get('messages_received', 0)} received")
    
    print("\n--- Agents ---")
    print(f"  Registered: {stats.get('registered_agents', 0)}")
    print(f"  Trusted: {stats.get('trusted_agents', 0)}")
    
    print("\n--- Contracts ---")
    print(f"  Total: {stats.get('contract_count', 0)}")
    
    # Chain integrity
    chain_result = context.event_store.verify()
    chain_status = "[OK]" if chain_result.valid else "[CORRUPTED]"
    print(f"\n--- Chain Integrity ---")
    print(f"  Status: {chain_status}")
    if not chain_result.valid and chain_result.error_message:
        print(f"  Error: {chain_result.error_message}")
    
    print()
    return 0


def cmd_events(args: argparse.Namespace) -> int:
    """
    List recent events.
    
    Args:
        args: Parsed command line arguments.
        
    Returns:
        Exit code (0 for success).
    """
    context = create_context(args.persist)
    
    query = EventQuery(
        agent_id=args.agent if hasattr(args, 'agent') and args.agent else None,
        limit=args.limit
    )
    events = context.event_store.query(query)
    
    print(f"\n=== EVENTS ({len(events)} found) ===\n")
    
    if not events:
        print("  No events found.")
        return 0
    
    print(f"{'Seq':<6} {'Agent':<20} {'Type':<12} {'Target':<15} {'Timestamp'}")
    print("-" * 80)
    
    for event in events:
        target = event.action.target or "-"
        timestamp = event.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        print(f"{event.sequence:<6} {event.agent.id:<20} {event.action.type.value:<12} {target:<15} {timestamp}")
    
    print()
    return 0


def cmd_agents(args: argparse.Namespace) -> int:
    """
    List registered agents or show specific agent details.
    
    Args:
        args: Parsed command line arguments.
        
    Returns:
        Exit code (0 for success).
    """
    context = create_context(args.persist)
    
    agents = context.identity_registry.list_agents()
    
    if hasattr(args, 'agent') and args.agent:
        # Show specific agent
        if args.agent not in agents:
            print(f"\nAgent '{args.agent}' not found.")
            return 1
        
        status = context.get_agent_status(args.agent)
        reputation = context.reputation_system.get_score(args.agent)
        
        print(f"\n=== AGENT: {args.agent} ===\n")
        print(f"  Registered: {status.get('is_registered', False)}")
        print(f"  Reputation: {reputation.current_score:.3f} ({reputation.trust_level})")
        print(f"  Events: {status.get('event_count', 0)}")
        print(f"  Contracts: {status.get('contract_count', 0)}")
        
        if reputation.history:
            print(f"\n  Recent Reputation Events:")
            for entry in reputation.history[-5:]:
                print(f"    - {entry}")
        
    else:
        # List all agents
        print(f"\n=== REGISTERED AGENTS ({len(agents)}) ===\n")
        
        if not agents:
            print("  No agents registered.")
            return 0
        
        print(f"{'Agent ID':<25} {'Reputation':<12} {'Trust Level':<15} {'Events'}")
        print("-" * 70)
        
        for agent_id in agents:
            reputation = context.reputation_system.get_score(agent_id)
            status = context.get_agent_status(agent_id)
            event_count = status.get('event_count', 0)
            print(f"{agent_id:<25} {reputation.current_score:<12.3f} {reputation.trust_level:<15} {event_count}")
    
    print()
    return 0


def cmd_contracts(args: argparse.Namespace) -> int:
    """
    List contracts.
    
    Args:
        args: Parsed command line arguments.
        
    Returns:
        Exit code (0 for success).
    """
    context = create_context(args.persist)
    
    if hasattr(args, 'agent') and args.agent:
        contracts = context.contract_registry.find_contracts(args.agent)
    else:
        contracts = context.contract_registry.contracts
    
    print(f"\n=== CONTRACTS ({len(contracts)}) ===\n")
    
    if not contracts:
        print("  No contracts found.")
        return 0
    
    for contract in contracts:
        parties = ", ".join([p.agent_id for p in contract.parties])
        status = "[ACTIVE]" if contract.is_active else "[PENDING]"
        signatures = len(contract.signatures)
        required = len(contract.parties)
        
        print(f"  {contract.contract_id[:8]}...")
        print(f"    Parties: {parties}")
        print(f"    Status: {status}")
        print(f"    Signatures: {signatures}/{required}")
        print(f"    Version: {contract.version}")
        print(f"    Capabilities: {len(contract.capabilities)} roles")
        print()
    
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    """
    Verify chain integrity.
    
    Args:
        args: Parsed command line arguments.
        
    Returns:
        Exit code (0 for success, 1 for integrity failure).
    """
    context = create_context(args.persist)
    
    print("\n=== CHAIN VERIFICATION ===\n")
    
    result = context.event_store.verify()
    
    if result.valid:
        print(f"  [OK] Chain integrity verified")
        print(f"  Events validated: {result.events_validated}")
    else:
        print(f"  [FAIL] Chain integrity compromised")
        print(f"  Error: {result.error_message}")
        if result.error_index is not None:
            print(f"  Failed at event index: {result.error_index}")
        return 1
    
    print()
    return 0


def cmd_violations(args: argparse.Namespace) -> int:
    """
    List recent axiom violations.
    
    Args:
        args: Parsed command line arguments.
        
    Returns:
        Exit code (0 for success).
    """
    context = create_context(args.persist)
    
    # Get violations from the axiom monitor
    violations = context.axiom_monitor.get_violation_history()
    
    if hasattr(args, 'limit') and args.limit:
        violations = violations[-args.limit:]
    
    print(f"\n=== AXIOM VIOLATIONS ({len(violations)}) ===\n")
    
    if not violations:
        print("  No violations recorded.")
        return 0
    
    for v in violations:
        print(f"  [{v.get('axiom', 'Unknown')}] {v.get('severity', 'UNKNOWN')}")
        print(f"    Agent: {v.get('agent_id', 'Unknown')}")
        print(f"    Reason: {v.get('reason', 'N/A')}")
        print(f"    Time: {v.get('timestamp', 'N/A')}")
        print()
    
    return 0


def main():
    """
    Main entry point for the dashboard CLI.
    
    Parses arguments and dispatches to the appropriate command handler.
    """
    parser = argparse.ArgumentParser(
        description="Society Verification Dashboard",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        "--persist", "-p",
        help="Path to persistence directory",
        default=None
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Status command
    status_parser = subparsers.add_parser("status", help="Show overall status")
    status_parser.set_defaults(func=cmd_status)
    
    # Events command
    events_parser = subparsers.add_parser("events", help="List events")
    events_parser.add_argument("--agent", "-a", help="Filter by agent ID")
    events_parser.add_argument("--limit", "-n", type=int, default=20, help="Limit results")
    events_parser.set_defaults(func=cmd_events)
    
    # Agents command
    agents_parser = subparsers.add_parser("agents", help="List or show agents")
    agents_parser.add_argument("--agent", "-a", help="Show specific agent")
    agents_parser.set_defaults(func=cmd_agents)
    
    # Contracts command
    contracts_parser = subparsers.add_parser("contracts", help="List contracts")
    contracts_parser.add_argument("--agent", "-a", help="Filter by agent ID")
    contracts_parser.set_defaults(func=cmd_contracts)
    
    # Verify command
    verify_parser = subparsers.add_parser("verify", help="Verify chain integrity")
    verify_parser.set_defaults(func=cmd_verify)
    
    # Violations command
    violations_parser = subparsers.add_parser("violations", help="List violations")
    violations_parser.add_argument("--limit", "-n", type=int, default=10, help="Limit results")
    violations_parser.set_defaults(func=cmd_violations)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
