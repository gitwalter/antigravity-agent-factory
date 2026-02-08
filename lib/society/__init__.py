"""
Agent Society Verification Library

Dynamic verification for multi-agent systems with:
- Event sourcing with cryptographic hash chains
- Agent contracts with capability/obligation verification
- Axiom compliance monitoring (A0-A5)
- Trust and reputation systems
- Society organizational patterns
- Optional blockchain integration for trustless verification

SDG - Love - Truth - Beauty
"""

# Core components - imported for easy access
from lib.society.events import AgentEvent, EventStore, HashChain
from lib.society.verification import (
    AxiomComplianceMonitor,
    VerificationResult,
    create_default_monitor,
)
from lib.society.contracts import (
    AgentContract,
    ContractRegistry,
    ContractVerifier,
    Party,
    Capability,
    Obligation,
    Prohibition,
    AxiomRequirements,
)
from lib.society.trust import (
    AgentIdentity,
    ReputationSystem,
    TrustGraph,
)
from lib.society.society import (
    SocietyPattern,
    create_society,
    GovernanceModel,
)
from lib.society.blockchain import (
    MerkleTree,
    AnchorService,
    LocalAnchor,
    AttestationRegistry,
)
from lib.society.hybrid import (
    HybridVerificationSystem,
    EscalationManager,
    SystemConfig,
)
from lib.society.integration import (
    SocietyContext,
    AgentSocietyBridge,
    MessageRouter,
)
from lib.society.integration.agent_bridge import MessageType

# Simple API (new)
from lib.society.simple import (
    create_agent_society,
    SimpleSociety,
    SocietyPreset,
    SendResult,
    quick_send,
)

__version__ = "1.2.0"

__all__ = [
    # Simple API (recommended)
    "create_agent_society",
    "SimpleSociety",
    "SocietyPreset",
    "SendResult",
    "quick_send",
    # Events
    "AgentEvent",
    "EventStore",
    "HashChain",
    # Verification
    "AxiomComplianceMonitor",
    "VerificationResult",
    "create_default_monitor",
    # Contracts
    "AgentContract",
    "ContractRegistry",
    "ContractVerifier",
    "Party",
    "Capability",
    "Obligation",
    "Prohibition",
    "AxiomRequirements",
    # Trust
    "AgentIdentity",
    "ReputationSystem",
    "TrustGraph",
    # Society
    "SocietyPattern",
    "create_society",
    "GovernanceModel",
    # Blockchain
    "MerkleTree",
    "AnchorService",
    "LocalAnchor",
    "AttestationRegistry",
    # Hybrid
    "HybridVerificationSystem",
    "EscalationManager",
    "SystemConfig",
    # Integration
    "SocietyContext",
    "AgentSocietyBridge",
    "MessageRouter",
    "MessageType",
]
