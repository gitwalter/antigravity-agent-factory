"""
Trust and Reputation Module

Cryptographic identity, reputation scoring, and trust delegation.

Components:
- AgentIdentity: Cryptographic identity with Ed25519 keys
- ReputationSystem: Score tracking based on axiom compliance
- TrustGraph: Trust delegation and transitive trust computation
"""

from lib.society.trust.identity import KeyPair, AgentIdentity, IdentityRegistry
from lib.society.trust.reputation import (
    ReputationType,
    ReputationEvent,
    ReputationScore,
    ReputationSystem,
)
from lib.society.trust.delegation import TrustDelegation, TrustGraph

__all__ = [
    # Identity
    "KeyPair",
    "AgentIdentity",
    "IdentityRegistry",
    # Reputation
    "ReputationType",
    "ReputationEvent",
    "ReputationScore",
    "ReputationSystem",
    # Delegation
    "TrustDelegation",
    "TrustGraph",
]
