"""
Society Module

Organizational patterns and communication protocols for agent societies.

Components:
- SocietyPattern: Abstract base for governance models
- FlatDemocracy, Meritocracy, Hierarchy, Federation, DAO: Governance patterns
- CommunicationProtocol: Abstract base for messaging
- DirectProtocol, BroadcastProtocol, ConsensusProtocol: Communication patterns
- MessageRouter: Unified message routing
"""

from lib.society.society.patterns import (
    GovernanceModel,
    DecisionType,
    Role,
    Proposal,
    SocietyPattern,
    FlatDemocracy,
    Meritocracy,
    Hierarchy,
    Federation,
    DAOSociety,
    create_society,
)
from lib.society.society.protocols import (
    MessageType,
    MessagePriority,
    Message,
    CommunicationProtocol,
    DirectProtocol,
    BroadcastProtocol,
    ConsensusProtocol,
    MessageRouter,
    create_message,
)

__all__ = [
    # Patterns
    "GovernanceModel",
    "DecisionType",
    "Role",
    "Proposal",
    "SocietyPattern",
    "FlatDemocracy",
    "Meritocracy",
    "Hierarchy",
    "Federation",
    "DAOSociety",
    "create_society",
    # Protocols
    "MessageType",
    "MessagePriority",
    "Message",
    "CommunicationProtocol",
    "DirectProtocol",
    "BroadcastProtocol",
    "ConsensusProtocol",
    "MessageRouter",
    "create_message",
]
