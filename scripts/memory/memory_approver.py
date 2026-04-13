"""
Memory Approver CLI
Phase 7 of the Automated Cognitive Memory System.
Provides a Human-In-The-Loop (HITL) interface for approving, rejecting, or editing
newly induced knowledge before it enters production collections.
"""

import argparse
import sys
import os
import logging
from typing import List, Optional

# Ensure the root directory is in PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from scripts.memory.induction_engine import get_induction_engine, MemoryProposal
from scripts.memory.memory_config import (
    COLLECTION_SEMANTIC,
    COLLECTION_PROCEDURAL,
    COLLECTION_TOOLBOX,
    COLLECTION_ENTITY,
)

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("memory_approver")


def format_proposal_brief(proposal: MemoryProposal) -> str:
    """Format a proposal for a one-line list view."""
    content_preview = (
        proposal.content[:60] + "..."
        if len(proposal.content) > 60
        else proposal.content
    )
    return f"[{proposal.id[:8]}] {proposal.source:15} | {proposal.confidence*100:3.0f}% | {content_preview}"


def cmd_list(args):
    engine = get_induction_engine()
    proposals = engine.get_pending_proposals()

    if not proposals:
        print("No pending memory proposals found.")
        return

    print("\n--- Pending Memory Proposals ---")
    print(f"{'ID':10} | {'Source':15} | {'Conf':4} | {'Content'}")
    print("-" * 80)
    for p in proposals:
        print(format_proposal_brief(p))
    print("-" * 80)
    print(f"Total: {len(proposals)} items pending.")


def cmd_show(args):
    engine = get_induction_engine()
    proposals = engine.get_pending_proposals()
    proposal = next((p for p in proposals if p.id.startswith(args.id)), None)

    if not proposal:
        print(f"Error: Proposal with ID starting with '{args.id}' not found.")
        return

    print("\n--- Memory Proposal Details ---")
    print(f"ID:         {proposal.id}")
    print(f"Source:     {proposal.source}")
    print(f"Scope:      {proposal.scope}")
    print(f"Confidence: {proposal.confidence*100:.1f}%")
    print(f"Target:     {proposal.target_collection}")
    print(f"Timestamp:  {proposal.timestamp}")
    print("-" * 40)
    print(f"Content:\n{proposal.content}")
    if proposal.context:
        print("-" * 40)
        print(f"Context:\n{proposal.context}")
    print("-" * 40)


def cmd_approve(args):
    engine = get_induction_engine()
    proposals = engine.get_pending_proposals()
    proposal = next((p for p in proposals if p.id.startswith(args.id)), None)

    if not proposal:
        print(f"Error: Proposal ID '{args.id}' not found.")
        return

    target = args.target or proposal.target_collection

    print(f"Approving proposal {proposal.id[:8]}...")
    try:
        # Note: induction_engine.accept_proposal needs target_collection support
        # We'll use the memory store directly if needed or assume engine is updated
        memory = engine.memory.accept_proposal(
            proposal_id=proposal.id, edited_content=args.edit, target_collection=target
        )
        print(f"Success! Knowledge promoted to '{target}' as memory {memory.id[:8]}.")
    except Exception as e:
        print(f"Error during approval: {e}")


def cmd_reject(args):
    engine = get_induction_engine()
    proposals = engine.get_pending_proposals()
    proposal = next((p for p in proposals if p.id.startswith(args.id)), None)

    if not proposal:
        print(f"Error: Proposal ID '{args.id}' not found.")
        return

    print(f"Rejecting proposal {proposal.id[:8]}...")
    engine.reject_proposal(proposal.id)
    print("Rejected. Similar observations will be ignored in the future.")


def main():
    parser = argparse.ArgumentParser(description="Antigravity Memory Approver CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # List
    subparsers.add_parser("list", help="List all pending proposals")

    # Show
    parser_show = subparsers.add_parser("show", help="Show full details of a proposal")
    parser_show.add_argument("id", help="Proposal ID (or prefix)")

    # Approve
    parser_app = subparsers.add_parser("approve", help="Approve and promote a proposal")
    parser_app.add_argument("id", help="Proposal ID (or prefix)")
    parser_app.add_argument(
        "--target",
        "-t",
        choices=[
            COLLECTION_SEMANTIC,
            COLLECTION_PROCEDURAL,
            COLLECTION_TOOLBOX,
            COLLECTION_ENTITY,
        ],
        help="Override target collection",
    )
    parser_app.add_argument("--edit", "-e", help="Edit the content before approving")

    # Reject
    parser_rej = subparsers.add_parser("reject", help="Reject a proposal")
    parser_rej.add_argument("id", help="Proposal ID (or prefix)")

    args = parser.parse_args()

    # Execute commands
    commands = {
        "list": cmd_list,
        "show": cmd_show,
        "approve": cmd_approve,
        "reject": cmd_reject,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
