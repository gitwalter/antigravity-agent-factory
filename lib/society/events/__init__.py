"""
Event Sourcing Module

Provides immutable, cryptographically signed event streams for
tracking agent actions with tamper-evident hash chaining.
"""

from lib.society.events.schema import (
    Agent,
    AgentType,
    Action,
    ActionType,
    AgentEvent,
    AxiomContext,
)
from lib.society.events.store import EventStore, EventQuery
from lib.society.events.chain import HashChain, ChainValidationResult, verify_chain_integrity

__all__ = [
    "Agent",
    "AgentType",
    "Action",
    "ActionType",
    "AgentEvent",
    "AxiomContext",
    "EventStore",
    "EventQuery",
    "HashChain",
    "ChainValidationResult",
    "verify_chain_integrity",
]
